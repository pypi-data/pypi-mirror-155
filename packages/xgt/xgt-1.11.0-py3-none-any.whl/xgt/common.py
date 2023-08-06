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

import logging

import grpc

import pyarrow

from . import DataService_pb2 as data_proto
from . import ErrorMessages_pb2 as err_proto

log = logging.getLogger(__name__)

BOOLEAN = 'boolean'
INT = 'int'
FLOAT = 'float'
DATE = 'date'
TIME = 'time'
DATETIME = 'datetime'
IPADDRESS = 'ipaddress'
TEXT = 'text'
LIST = 'list'

# Send in 2MB chunks (grpc recommends 16-64 KB, but this got the best performance locally)
# FYI: by default grpc only supports up to 4MB.
MAX_PACKET_SIZE = 2097152

class XgtError(Exception):
  """
  Base exception class from which all other xgt exceptions inherit. It is
  raised in error cases that don't have a specific xgt exception type.
  """
  def __init__(self, msg, trace=''):
    self.msg = msg
    self.trace = trace

    if log.getEffectiveLevel() >= logging.DEBUG:
      if self.trace != '':
        log.debug(self.trace)
      else:
        log.debug(self.msg)
    Exception.__init__(self, self.msg)

class XgtNotImplemented(XgtError):
  """Raised for functionality with pending implementation."""
class XgtInternalError(XgtError):
  """
  Intended for internal server purposes only. This exception should not become
  visible to the user.
  """
class XgtIOError(XgtError):
  """An I/O problem occurred either on the client or server side."""
  def __init__(self, msg, trace='', job = None):
    self._job = job
    XgtError.__init__(self, msg, trace)

  @property
  def job(self):
    """Job: Job associated with the load/insert operation if available. May be None."""
    return self._job
class XgtServerMemoryError(XgtError):
  """
  The server memory usage is close to or at capacity and work could be lost.
  """
class XgtConnectionError(XgtError):
  """
  The client cannot properly connect to the server. This can include a failure
  to connect due to an xgt module version error.
  """
class XgtSyntaxError(XgtError):
  """A query was provided with incorrect syntax."""
class XgtTypeError(XgtError):
  """
  An unexpected type was supplied.

  For queries, an invalid data type was used either as an entity or as a
  property. For frames, either an edge, vertex or table frames was expected
  but the wrong frame type or some other data type was provided. For
  properties, the property declaration establishes the expected data type. A
  type error is raise if the data type used is not appropriate.
  """
class XgtValueError(XgtError):
  """An invalid or unexpected value was provided."""
class XgtNameError(XgtError):
  """
  An unexpected name was provided. Typically can occur during object retrieval
  where the object name was not found.
  """
class XgtArithmeticError(XgtError):
  """An invalid arithmetic calculation was detected and cannot be handled."""
class XgtFrameDependencyError(XgtError):
  """
  The requested action will produce an invalid graph or break a valid graph.
  """
class XgtTransactionError(XgtError):
  """A Transaction was attempted but didn't complete."""
class XgtSecurityError(XgtError):
  """A security violation occured."""

# Validation support functions

def _validated_schema(obj):
  '''Takes a user-supplied object and returns a valid schema.

  Users can supply a variety of objects as valid schemas. To simplify internal
  processing, we canonicalize these into a list of string-type pairs,
  performing validation along the way.
  '''
  # Validate the shape first
  try:
    if len(obj) < 1:
      raise XgtTypeError('A schema must not be empty.')
    for col in obj:
      assert len(col) >= 2
      if (_validated_property_type(col[1]) == "LIST"):
        assert (len(col) <= 4 and len(col) >= 3)
      else:
        assert len(col) == 2
  except:
    raise XgtTypeError('A schema must be a non-empty list of (property, type) pairs.')
  # Looks good. Return a canonical schema.
  schema_returned = []
  for col in obj:
    val_type = _validated_property_type(col[1])
    if val_type != "LIST":
      schema_returned.append((_validated_property_name(col[0]), val_type))
    else:
      leaf_type = _validated_property_type(col[2])
      if (len(col) != 4):
        schema_returned.append((_validated_property_name(col[0]),
                               val_type, leaf_type))
      else:
        schema_returned.append((_validated_property_name(col[0]),
                                val_type, leaf_type, col[3]))
  return schema_returned

def _validated_frame_name(obj):
  '''Takes a user-supplied object and returns a unicode frame name string.'''
  _assert_isstring(obj)
  name = str(obj)
  if len(name) < 1:
    raise XgtNameError('Frame names cannot be empty.')
  return name

def _validated_namespace_name(obj):
  '''Takes a user-supplied object and returns a unicode frame name string.'''
  _assert_isstring(obj)
  name = str(obj)
  if len(name) < 1:
    raise XgtNameError('Namespace names cannot be empty.')
  return name

def _validated_property_name(obj):
  '''Takes a user-supplied object and returns a unicode property name string.'''
  _assert_isstring(obj)
  return str(obj)

def _get_valid_property_types_to_create():
  return [BOOLEAN, INT, FLOAT, DATE, TIME, DATETIME, IPADDRESS, TEXT, LIST]

def _get_valid_property_types_for_return_only():
  return ['container_id', 'job_id']

def _validated_property_type(obj):
  '''Takes a user-supplied object and returns an xGT schema type.'''
  _assert_isstring(obj)
  prop_type = str(obj)
  valid_prop_types = _get_valid_property_types_to_create()
  if prop_type.lower() not in valid_prop_types:
    if prop_type.lower in _get_valid_property_types_for_return_only():
      raise XgtTypeError('Invalid property type "'+prop_type+'". This type '
                         'cannot be used when creating a frame.')
    else:
      raise XgtTypeError('Invalid property type "'+prop_type+'"')
  return prop_type.upper()

def _validate_opt_level(optlevel):
  """
  Valid optimization level values are:
    - 0: No optimization.
    - 1: General optimization.
    - 2: WHERE-clause optimization.
    - 3: Degree-cycle optimization.
    - 4: Query order optimization.
  """
  if isinstance(optlevel, int):
    if optlevel not in [0, 1, 2, 3, 4]:
      raise XgtValueError("Invalid optlevel '" + str(optlevel) +"'")
  else:
    raise XgtTypeError("optlevel must be an integer")
  return True

def _assert_noerrors(response):
  if len(response.error) > 0:
    error = response.error[0]
    try:
      error_code_name = err_proto.ErrorCodeEnum.Name(error.code)
      error_class = _code_error_map[error_code_name]
      raise error_class(error.message, error.detail)
    except XgtError:
      raise
    except Exception as ex:
      raise XgtError("Error detected while raising exception" +
                     str(ex), str(ex))

def _convert_flight_server_error_into_xgt(error):
  if len(error.extra_info) >= 8 and error.extra_info[0:6] == b"ERROR:":
    try:
      error_class = _code_error_map[err_proto.ErrorCodeEnum.Name(int(error.extra_info[6:8]))]
      return error_class(str(error), error.extra_info)
    except:
      pass
  return XgtError(str(error))

def _assert_isstring(value):
  if not isinstance(value, str):
    msg = str(value) + " is not a string"
    raise TypeError(msg)

_code_error_map = {
  'GENERIC_ERROR': XgtError,
  'NOT_IMPLEMENTED': XgtNotImplemented,
  'INTERNAL_ERROR': XgtInternalError,
  'IO_ERROR': XgtIOError,
  'SERVER_MEMORY_ERROR': XgtServerMemoryError,
  'CONNECTION_ERROR': XgtConnectionError,
  'SYNTAX_ERROR': XgtSyntaxError,
  'TYPE_ERROR': XgtTypeError,
  'VALUE_ERROR': XgtValueError,
  'NAME_ERROR': XgtNameError,
  'ARITHMETIC_ERROR': XgtArithmeticError,
  'FRAME_DEPENDENCY_ERROR': XgtFrameDependencyError,
  'TRANSACTION_ERROR': XgtTransactionError,
  'SECURITY_ERROR': XgtSecurityError,
}

def _create_flight_ticket(name, offset, length, include_row_labels,
                          row_label_column_header = None,
                          order = True, date_as_string = True,
                          job_id = None):
  if isinstance(offset, str):
    offset = int(offset)
  elif not isinstance(offset, int):
    raise ValueError("offset must be an int.")
  if offset < 0:
    raise ValueError("offset must be >= 0.")

  if length is not None:
    if isinstance(length, str):
      length = int(length)
    elif not isinstance(length, int):
      raise ValueError("length must be an int.")
    if length < 0:
      raise ValueError("length must be >= 0.")

  ticket = '`' + name + '`'

  if offset != 0:
    ticket += ".offset=" + str(offset)
  if length != None:
    ticket += ".length=" + str(length)
  if order:
    ticket += ".order=True"
  if date_as_string:
    ticket += ".dates_as_strings=True"
  if include_row_labels:
    ticket += ".egest_row_labels=True"
  if row_label_column_header is not None:
    ticket += ".label_column_header=" + row_label_column_header

  if job_id is not None:
    if isinstance(job_id, str):
      job_id = int(job_id)
    elif not isinstance(job_id, int):
      raise ValueError("job ID must be an int.")
    ticket += ".job_id=" + str(job_id)

  return ticket

def _get_data_python_from_table(arrow_table):
  # List comprehension here is simpler, but has slow performance due to the
  # access pattern being bad for the cache hits.
  return_list = [None] * arrow_table.num_rows
  for i in range(arrow_table.num_rows):
    return_list[i] = []
  for i, x in enumerate(arrow_table):
    for j, y in enumerate(x):
      return_list[j].append(y.as_py())
  return return_list

def _get_data_arrow(conn, ticket):
  try:
    res_table = conn.arrow_conn.do_get(pyarrow.flight.Ticket(ticket)).read_all()
    return res_table
  except pyarrow._flight.FlightServerError as err:
    raise _convert_flight_server_error_into_xgt(err) from err
  except pyarrow._flight.FlightUnavailableError as err:
    raise XgtConnectionError(str(err)) from err

def _get_data_python(conn, ticket):
  res_table = _get_data_arrow(conn, ticket)
  return _get_data_python_from_table(res_table)

def _get_data_pandas(conn, ticket):
  res_table = _get_data_arrow(conn, ticket)
  return res_table.to_pandas()

# Helper functions for low code.

# Convert the pyarrow type to an xgt type.
def _pyarrow_type_to_xgt_type(pyarrow_type):
  if pyarrow.types.is_boolean(pyarrow_type):
    return BOOLEAN
  elif pyarrow.types.is_timestamp(pyarrow_type) or pyarrow.types.is_date64(pyarrow_type):
    return DATETIME
  elif pyarrow.types.is_date(pyarrow_type):
    return DATE
  elif pyarrow.types.is_time(pyarrow_type):
    return TIME
  elif pyarrow.types.is_integer(pyarrow_type):
    return INT
  elif pyarrow.types.is_float32(pyarrow_type) or \
       pyarrow.types.is_float64(pyarrow_type) or \
       pyarrow.types.is_decimal(pyarrow_type):
    return FLOAT
  elif pyarrow.types.is_string(pyarrow_type):
    return TEXT
  else:
    raise XgtTypeError("Cannot convert pyarrow type " + str(pyarrow_type) + " to xGT type.")

def _infer_xgt_schema_from_pyarrow_schema(pyarrow_schema):
  return [[c.name, _pyarrow_type_to_xgt_type(c.type)] for c in pyarrow_schema]

# Get the column in the schema by name or position.
def _find_key_in_schema(key, schema):
  if isinstance(key, str):
    found_key = False
    for elem in schema:
      if elem[0] == key:
        found_key = True
        break
    if not found_key:
      raise XgtNameError("The key " + str(key) + " not found in schema.")
    return key
  elif isinstance(key, int):
    if key >= len(schema) or key < 0:
      raise XgtError("Could not locate key " + str(key) + " in schema with " + str(len(schema)) + " entries.")
    return schema[key][0]

# Modify an xgt schema based on a frame column name to data column name
# mapping. The key names of this map will become the column names of the
# new schema. The values of the map correspond to the columns of the
# initial schema.
def _apply_mapping_to_schema(initial_schema, frame_to_data_column_mapping):
  def find_data_col_name(data_col):
    if isinstance(data_col, str):
      return data_col
    elif isinstance(data_col, int):
      if data_col >= len(initial_schema) or data_col < 0:
        err("Error creating the schema. The column mapping refers to data column "
            "position " + str(data_col) + ", but only " + str(len(initial_schema)) +
            " columns were found in the data.")
        raise XgtValueError(err)
      return initial_schema[data_col][0]

  data_col_name_to_type = { elem[0] : elem[1] for elem in initial_schema }

  schema = []
  for frame_col, data_col in frame_to_data_column_mapping.items():
    data_type = data_col_name_to_type[find_data_col_name(data_col)]
    schema.append([frame_col, data_type])

  return schema

def _remove_label_columns_from_schema(initial_schema, row_label_columns):
  def find_data_col_name(data_col):
    if isinstance(data_col, str):
      return data_col
    elif isinstance(data_col, int):
      if data_col >= len(initial_schema) or data_col < 0:
        err("Error creating the schema. The row_label_columns parameter refers to data column "
            "position " + str(data_col) + ", but only " + str(len(initial_schema)) +
            " columns were found in the data.")
        raise XgtValueError(err)
      return initial_schema[data_col][0]

  data_col_name_to_type = { elem[0] : elem[1] for elem in initial_schema }

  label_columns = set([find_data_col_name(col) for col in row_label_columns])

  return [col for col in initial_schema if col[0] not in label_columns]
