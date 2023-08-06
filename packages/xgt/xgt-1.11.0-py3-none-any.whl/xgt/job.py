# -*- coding: utf-8 -*- --------------------------------------------------===#
#
#  Copyright 2018-2022 Trovares Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#===----------------------------------------------------------------------===#

from datetime import datetime
import logging
import json

from . import ErrorMessages_pb2 as err_proto
from . import JobService_pb2 as job_proto
from . import SchemaMessages_pb2 as sch_proto
from .common import (XgtError, XgtInternalError, XgtNotImplemented,
                     _create_flight_ticket, _get_data_python_from_table,
                     _get_data_arrow, _code_error_map)

log = logging.getLogger(__name__)

class _QueryPlan(object):
  class _QueryPlanSingleFrame(object):
    def __init__(self, query_element_message):
      self._label = query_element_message.source_label
      self._frame = query_element_message.source_frame

    @property
    def name(self):
      return self._label + ":" + self._frame;

    def __str__(self):
      return "(" + self._label + ":" + self._frame + ")"

  class _QueryPlanEdge(object):
    def __init__(self, query_edge_message):
      if query_edge_message.edge_direction == \
         sch_proto.QueryEdgeDirection.Value('FORWARD'):
        self.forward_edge = True
      else:
        self.forward_edge = False
      self._source_label = query_edge_message.source_label
      self._source_frame = query_edge_message.source_frame
      self._edge_label = query_edge_message.edge_label
      self._edge_frame = query_edge_message.edge_frame
      self._target_label = query_edge_message.target_label
      self._target_frame = query_edge_message.target_frame

    @property
    def name(self):
      return self._edge_label + ":" + self._edge_frame;

    @property
    def edge_name(self):
      return self._edge_label + ":" + self._edge_frame;

    @property
    def source_name(self):
      return self._source_label + ":" + self._source_frame;

    @property
    def target_name(self):
      return self._target_label + ":" + self._target_frame;

    # The string representation of a _QueryPlanEdge object is a tuple
    # of the source vertex, edge, and target vertex. The direction
    # of the edge is always forward.
    def __str__(self):
      if self.forward_edge:
        vertex1 = self.source_name
        vertex2 = self.target_name
      else:
        vertex2 = self.source_name
        vertex1 = self.target_name
      return "(" + vertex1 + ", " + self.edge_name + ", " + vertex2 + ")"

  def __init__(self, query_plan_response):
    # The _plan member is a list of lists. Each list represents a query
    # that starts with MATCH in cypher and contains elements representing
    # edges or (if only a single frame was matched), a vertex or table.
    self._plan = []
    for query in query_plan_response.plan_as_edge_list:
      query_representation = []
      plan_score = None
      for element in query.edges:
        if element.edge_direction == \
           sch_proto.QueryEdgeDirection.Value('NOT_EDGE'):
          query_representation.append(self._QueryPlanSingleFrame(element))
        else:
          query_representation.append(self._QueryPlanEdge(element))
      if (query.HasField("plan_score")):
        plan_score = query.plan_score
      self._plan.append((query_representation, plan_score))

  def __str__(self):
    as_string = ""
    for (idx, query) in enumerate(self._plan):
      if idx > 0:
        as_string += "\n"
      as_string += "QUERY:"
      for element in query[0]:
        as_string += "\n" + str(element)
    return as_string

  def to_cypher(self):
    cypher = ""
    for query, score in self._plan:
      # The corresponding query section had no MATCH portion. It won't be
      # included in the cypher representation currently used as only
      # the structure of the MATCH portions is shown.
      if len(query) == 0:
        continue
      if len(cypher) > 0:
        cypher += "\n"
      cypher += "MATCH\n"
      last_target_name = ""

      # Write the first element of the query. This must be a vertex or table
      # frame.
      if isinstance(query[0], self._QueryPlanEdge):
        cypher += "(" + query[0].source_name + ")"
      else:
        cypher += "(" + query[0].name + ")"

      for (element_idx, element) in enumerate(query):
        if isinstance(element, self._QueryPlanEdge):
          if last_target_name != element.source_name and element_idx > 0:
            # This edge starts a new path in the query. We must write the
            # source.
            cypher += ",\n(" + element.source_name + ")"
          if not element.forward_edge:
            cypher += "<"
          cypher += "-[" + element.edge_name + "]-"
          if element.forward_edge:
            cypher += ">"
          cypher += "(" + element.target_name + ")"
          last_target_name = element.target_name
        elif element_idx > 0:
          # This is not an edge element. It is a vertex or table frame.
          # If it was the first in this query then it has already been
          # written. Otherwise, it starts a new path in the query and
          # must be written.
          cypher += ",\n(" + element.name + ")"
    return cypher

  def get_scores(self):
    return [score for query, score in self._plan]

class Job(object):
  """
  Represents a user-scheduled Job.

  An instance of this object is created by job-scheduling functions like
  `xgt.Connection.run_job` and `xgt.Connection.schedule_job`.

  A `Job` is used as a proxy for a job in the server and allows the user
  to monitor its execution, possibly cancel it, and learn about its status
  during and after execution.

  The conn parameter represents a previously established connection to the xGT
  server.

  The job_response parameter is a single element of the array returned by the
  output of a job creation gRPC call.  Each individual element in the array will
  be constructed as a separate `Job` object.

  """
  def __init__(self, conn, job_response = None, python_results = None,
               python_errors = None):
    """
    Constructor for Job. Called when Job is created.
    """
    self._conn = conn
    if job_response is not None:
      self._id = job_response.job_id
      self._user = job_response.user
      self._data = self._parse_job_data(job_response)
    else:
      self._id = 0
      self._user = ""
      self._data = { 'status' : 'completed', 'total_rows' : 0 }
    if python_results is not None:
      self._data['python_rows'] = python_results
      self._data['total_rows'] += len(python_results)
    if python_errors is not None:
      if 'ingest_errors' in self._data.keys():
        self._data['ingest_errors'] += python_errors
        self._data['total_ingest_errors'] += len(python_errors)
      else:
        if len(python_errors) > 0:
          self._data['ingest_errors'] = python_errors
        self._data['total_ingest_errors'] = len(python_errors)
    self._arrow_table = None

  def _parse_job_data(self, job_response):
    job_data = {
      'jobid': job_response.job_id,
      'user': job_response.user,
      'status': sch_proto.JobStatusEnum.Name(job_response.status).lower(),
      'start_time': job_response.start_time.ToDatetime().isoformat(),
      'end_time': job_response.end_time.ToDatetime().isoformat(),
      'error_type': None,
      'visited_edges': job_response.visited_edges,
      'timing': job_response.timing,
      'description': job_response.description,
      'total_rows' : job_response.total_rows,
      'total_ingest_errors' : job_response.total_ingest_errors,
    }
    # Optional fields.
    if (job_response.HasField('schema')):
      job_data['schema'] = [[prop.name,
                             sch_proto.UvalTypeEnum.Name(prop.data_type).lower()]
                            for prop in job_response.schema.property]
    if job_response.ingest_error and len(job_response.ingest_error):
      job_data['ingest_errors'] = [data for data in job_response.ingest_error]
    if job_response.error and len(job_response.error) > 0:
        error_code_name = err_proto.ErrorCodeEnum.Name(job_response.error[0].code)
        job_data['error_type'] = _code_error_map[error_code_name]
        job_data['error'] = ', '.join([e.message for e in job_response.error])
        job_data['trace'] = ', '.join([e.detail for e in job_response.error])
    if job_response.HasField('query_plan'):
      job_data['query_plan'] =  _QueryPlan(job_response.query_plan)

    return job_data

  def _get_job_data(self):
    request = job_proto.GetJobsRequest()
    request.job_id.extend([self._id])
    responses = self._conn._call(request, self._conn._job_svc.GetJobs)
    job_data = None
    resp_cnt = 0
    for response in responses: # Expect only one response.
      job_data = self._parse_job_data(response.job_status) # Retrieve the job status.
      resp_cnt += 1

    if (resp_cnt > 1):
      raise XgtInternalError("Expected a single job in response")

    # If the status is unknown, only update the status, not other fields as
    # they will be invalid.
    returned_status = job_data['status']
    if returned_status == 'unknown_job_status':
      self._data['status'] = returned_status
      return job_data

    # Cache the response from the server.
    self._data = job_data

    if log.getEffectiveLevel() >= logging.DEBUG:
      job_id = job_data['jobid']
      job_status = job_data['status']
      user = job_data['user']
      if 'error' in job_data:
        error = job_data['error']
      else:
        error = ''
      if 'trace' in job_data:
        trace = job_data['trace']
      else:
        trace = ''
      msg = 'Job: {0} User: {1} Status: {2}'.format(str(job_id),
                                                    user,
                                                    job_status)
      if error != '':
        msg = msg + "\nError: \n" + error
      if trace != '':
        msg = msg + "\nTrace: \n" + trace
      log.debug(msg)

    return job_data

  def _is_status_final(self):
    if 'status' in self._data:
      curr_status = self._data['status']

      if ((curr_status == 'completed') or (curr_status == 'canceled') or
          (curr_status == 'failed') or (curr_status == 'rollback') or
          (curr_status == 'unknown_job_status')):
        return True

    return False

  def _get_data_helper(self, offset, length, as_pandas):
    if isinstance(offset, str):
      offset = int(offset)
    if isinstance(length, str):
      length = int(length)
    if isinstance(offset, int):
      if offset < 0:
        raise ValueError('offset is negative')
    if isinstance(length, int):
      if length < 0:
        raise ValueError('length is negative')
    if 'rows' in self._data and not as_pandas:
      total_length = len(self._data['rows'])
      if length is None:
        length = total_length
      elif not isinstance(length, int):
        raise ValueError('length must be a non-negative integer')

      rows = self._data['rows']
      startpos = min(offset, total_length)
      endpos = min(offset + length, total_length)
      return rows[startpos:endpos]
    elif 'python_rows' in self._data and not as_pandas:
      return self._data['python_rows']
    if 'pandas' in self._data and as_pandas:
      if length is None:
        total_length = len(self._data['pandas'].index)
        length = total_length
      startpos = min(offset, total_length)
      endpos = min(offset + length + 1, total_length)
      return self._data['pandas'][startpos:endpos]
    else:
      return None

  def _load_data_helper(self, as_pandas):
    if self._is_status_final():
      curr_status = self._data['status']

      if curr_status != 'completed':
        return

      # Skip getting the Arrow table if there are no results.
      # The schema was not set for jobs without immediate results.
      if 'schema' not in self._data:
        return

      if self._arrow_table is None:
        ticket = _create_flight_ticket('xgt__Job_History', offset = 0,
                                       length = None, include_row_labels = False,
                                       job_id = self._id)
        # Cache the results in an Arrow table to be able to return them to
        # the user in both Python and Pandas formats.
        self._arrow_table = _get_data_arrow(self._conn, ticket)
      if not as_pandas:
        self._data['rows'] = _get_data_python_from_table(self._arrow_table)
      else:
        self._data['pandas'] = self._arrow_table.to_pandas()

  @property
  def id(self):
    """
    int: Identifier of the job.

    A 64-bit integer value that uniquely identifies a job. It is
    automatically incremented for each scheduled job over the lifetime of
    the xGT server process.

    """
    return self._id

  @property
  def user(self):
    """
    str: User that ran the job.

    A string that identifies the user who ran the job.
    """
    return self._user

  @property
  def status(self):
    """
    str: Status of the job.

  ==================  ===============================================
        Job status
  -------------------------------------------------------------------
           Status                       Description
  ==================  ===============================================
           scheduled  The state after the job has been created, but
                      before it has started running.
             running  The job is being executed.
           completed  The job finished successfully.
            canceled  The job was canceled.
              failed  The job failed. When the job fails the `error`
                      and `trace` properties are populated.
            rollback  The job had a transactional conflict with
                      another job and was rolled back.
  unknown_job_status  The job was not found in the job history.
  ==================  ===============================================

    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'status' in self._data:
      return self._data['status']
    else:
      return ''

  @property
  def start_time(self):
    """
    str: Date and time when the job was scheduled.

    This is a formatted string that has a resolution of seconds.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'start_time' in self._data:
      if "." in self._data['start_time']:
        return datetime.strptime(self._data['start_time'], '%Y-%m-%dT%H:%M:%S.%f')
      return datetime.strptime(self._data['start_time'], '%Y-%m-%dT%H:%M:%S')
    else:
      return ''

  @property
  def end_time(self):
    """
    str: Date and time when the job finished running.

    This is a formatted string that has a resolution of seconds.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'end_time' in self._data:
      if "." in self._data['start_time']:
        return datetime.strptime(self._data['end_time'], '%Y-%m-%dT%H:%M:%S.%f')
      return datetime.strptime(self._data['end_time'], '%Y-%m-%dT%H:%M:%S')
    else:
      return ''

  @property
  def visited_edges(self):
    """
    dict: A dictionary mapping Cypher bound variable names to an integer giving
    the number of edges visited during the job for the Edge Frame referenced by
    the bound variable.

    An edge is "visited" when the query considers the edge as a match to one of
    the query path edges.  Multiple Cypher variables can refer to the same edge
    frame.

    Consider the query path
    ``()-[a:graph_edges1]->()-[b:graph_edges2]->()-[c:graph_edges1]->()`` with
    a visited_edges result of ``a -> 5, b -> 7, c -> 4``.  In performing the
    query 5 edges of type `a` were visited, and so on.  Notice that the total
    number of edges visited for the frame graph_edges1 is 9 while the number of
    edges visited for the frame graph_edges2 is 7.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    return self._data['visited_edges']

  @property
  def total_visited_edges(self):
    """
    int: The total number of edges traversed during the job. This is the sum
    of the counts for all edge labels returned in visited_edges.

    For the example given in the visited_edges documentation, the value of
    total_visited_edges would be 16.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    return sum(self._data['visited_edges'].values())

  @property
  def timing(self):
    """
    For internal use.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    return self._data['timing']

  @property
  def description(self):
    """
    str: A description supplied when the job was started.  Usually a query.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    return self._data['description']

  @property
  def error_type(self):
    """
    object: Class that belongs to the XgtError hierarchy that corresponds to
            the original exception type thrown that caused the Job to fail.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'error_type' in self._data:
      return self._data['error_type']
    else:
      return XgtError

  @property
  def error(self):
    """
    str: User-friendly error message describing the reason a job failed.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'error' in self._data:
      return self._data['error']
    else:
      return ''

  @property
  def trace(self):
    """
    str: Very detailed error message for a failed job.

    This error message contains the friendly error message and a stack
    strace for the code that participated in the error.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'trace' in self._data:
      return self._data['trace']
    else:
      return ''

  @property
  def schema(self):
    """
    list of lists: Gets the property names and types of the stored immediate
    results.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'schema' in self._data:
      return self._data['schema']
    else:
      return None

  @property
  def total_rows(self):
    """
    int: Gets the number of rows of the query results.  Note that this is >=
    than the number of rows of data extracted to the job.  To get the full
    results the query can be executed again using an INTO clause to a
    named results Table.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'total_rows' in self._data:
      return self._data['total_rows']
    else:
      return None

  @property
  def total_ingest_errors(self):
    """
    int: Get the number of errors that were thrown during ingest.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'total_ingest_errors' in self._data:
      return self._data['total_ingest_errors']
    else:
      return None

  def get_data(self, offset=0, length=None):
    """
    Returns immediate results data starting at a given offset and spanning a given
    length.

    Parameters
    ----------
    offset : int
      Position (index) of the first row to be retrieved.
      Optional. Default=0.
    length : int
      Maximum number of rows to be retrieved starting from the row
      indicated by offset. A value of 'None' means 'all rows' on and
      after the offset.
      Optional. Default=None.

    Returns
    -------
    list of lists
    If the job object represents a TQL query with no RETURN clause, this returns None.

    """
    if (not self._is_status_final()):
      self._get_job_data()

    self._load_data_helper(as_pandas = False)
    return self._get_data_helper(offset, length, as_pandas = False)

  def get_ingest_errors(self, offset=0, length=None):
    """
    Returns a table of strings giving error information from ingest.  The first
    thousand errors raised are retrievable this way.

    Parameters
    ----------
    offset : int
      Position (index) of the first row to be retrieved.
      Optional. Default=0.
    length : int
      Maximum number of rows of errors to be retieved starting from the row
      indicated by offset.  A value of 'None' means 'all rows' on and after
      the offset.
      Optional. Default-None.

    Returns
    -------
    list of strings
    If this is not an ingest job or no errors were raised, this returns None.

    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'ingest_errors' in self._data:
      if isinstance(offset, str):
        offset = int(offset)
      if isinstance(length, str):
        length = int(length)
      if isinstance(offset, str):
        if offset < 0:
          raise ValueError('offset is negative')
      if isinstance(length, int):
        if length < 0:
          raise ValueError('length is negative')
      total_length = len(self._data['ingest_errors'])
      if length is None:
        length = total_length
      elif not isinstance(length, int):
        raise ValueError('length must be a non-negative integer')

      errors = self._data['ingest_errors']
      startpos = min(offset, total_length)
      endpos = min(offset + length + 1, total_length)

      return errors[startpos:endpos]
    else:
      return None

  def get_data_pandas(self, offset=0, length=None):
    """
    Returns a Pandas DataFrame containing immediate results data starting at a
    given offset and spanning a given length.

    Parameters
    ----------
    offset : int
      Position (index) of the first row to be retrieved.
      Optional. Default=0.
    length : int
      Maximum number of rows to be retrieved starting from the row
      indicated by offset. A value of 'None' means 'all rows' on and
      after the offset.
      Optional. Default=None.

    Returns
    -------
    Pandas DataFrame

    """
    import pandas
    if (not self._is_status_final()):
      self._get_job_data()

    self._load_data_helper(as_pandas = True)
    return self._get_data_helper(offset, length, as_pandas = True)

  def __str__(self):
    txt = ('id:{0}, user:{1}, status:{2}').format(self.id, self.user, self.status)
    if len(self.error) > 0:
      txt = txt + (', nerror:{0}').format(self.error)
    return txt

  @property
  def _query_plan(self):
    """
    For internal use.

    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'query_plan' in self._data:
      return str(self._data['query_plan'])
    else:
      return ''

  @property
  def _query_plan_as_cypher(self):
    """
    For internal use.

    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'query_plan' in self._data:
      return self._data['query_plan'].to_cypher()
    else:
      return ''

  @property
  def _query_plan_scores(self):
    """
    For internal use.

    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'query_plan' in self._data:
      return self._data['query_plan'].get_scores()
    else:
      return None
