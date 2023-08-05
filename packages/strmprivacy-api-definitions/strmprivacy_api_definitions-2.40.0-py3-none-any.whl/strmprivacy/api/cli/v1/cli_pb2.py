# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: strmprivacy/api/cli/v1/cli.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n strmprivacy/api/cli/v1/cli.proto\x12\x16strmprivacy.api.cli.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1fgoogle/protobuf/timestamp.proto\")\n\x11GetReleaseRequest\x12\x14\n\x07version\x18\x01 \x01(\tB\x03\xe0\x41\x01\"N\n\x12GetReleaseResponse\x12\x38\n\x07release\x18\x01 \x01(\x0b\x32\".strmprivacy.api.cli.v1.CliReleaseB\x03\xe0\x41\x03\"\x8e\x01\n\nCliRelease\x12\x14\n\x07version\x18\x01 \x01(\tB\x03\xe0\x41\x03\x12\x35\n\x0crelease_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x03\xe0\x41\x03\x12\x17\n\nsource_uri\x18\x03 \x01(\tB\x03\xe0\x41\x03\x12\x1a\n\rrelease_notes\x18\x04 \x01(\tB\x03\xe0\x41\x03\x32q\n\nCliService\x12\x63\n\nGetRelease\x12).strmprivacy.api.cli.v1.GetReleaseRequest\x1a*.strmprivacy.api.cli.v1.GetReleaseResponseBZ\n\x19io.strmprivacy.api.cli.v1P\x01Z;github.com/strmprivacy/api-definitions-go/v2/api/cli/v1;clib\x06proto3')



_GETRELEASEREQUEST = DESCRIPTOR.message_types_by_name['GetReleaseRequest']
_GETRELEASERESPONSE = DESCRIPTOR.message_types_by_name['GetReleaseResponse']
_CLIRELEASE = DESCRIPTOR.message_types_by_name['CliRelease']
GetReleaseRequest = _reflection.GeneratedProtocolMessageType('GetReleaseRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETRELEASEREQUEST,
  '__module__' : 'strmprivacy.api.cli.v1.cli_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.cli.v1.GetReleaseRequest)
  })
_sym_db.RegisterMessage(GetReleaseRequest)

GetReleaseResponse = _reflection.GeneratedProtocolMessageType('GetReleaseResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETRELEASERESPONSE,
  '__module__' : 'strmprivacy.api.cli.v1.cli_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.cli.v1.GetReleaseResponse)
  })
_sym_db.RegisterMessage(GetReleaseResponse)

CliRelease = _reflection.GeneratedProtocolMessageType('CliRelease', (_message.Message,), {
  'DESCRIPTOR' : _CLIRELEASE,
  '__module__' : 'strmprivacy.api.cli.v1.cli_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.cli.v1.CliRelease)
  })
_sym_db.RegisterMessage(CliRelease)

_CLISERVICE = DESCRIPTOR.services_by_name['CliService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031io.strmprivacy.api.cli.v1P\001Z;github.com/strmprivacy/api-definitions-go/v2/api/cli/v1;cli'
  _GETRELEASEREQUEST.fields_by_name['version']._options = None
  _GETRELEASEREQUEST.fields_by_name['version']._serialized_options = b'\340A\001'
  _GETRELEASERESPONSE.fields_by_name['release']._options = None
  _GETRELEASERESPONSE.fields_by_name['release']._serialized_options = b'\340A\003'
  _CLIRELEASE.fields_by_name['version']._options = None
  _CLIRELEASE.fields_by_name['version']._serialized_options = b'\340A\003'
  _CLIRELEASE.fields_by_name['release_time']._options = None
  _CLIRELEASE.fields_by_name['release_time']._serialized_options = b'\340A\003'
  _CLIRELEASE.fields_by_name['source_uri']._options = None
  _CLIRELEASE.fields_by_name['source_uri']._serialized_options = b'\340A\003'
  _CLIRELEASE.fields_by_name['release_notes']._options = None
  _CLIRELEASE.fields_by_name['release_notes']._serialized_options = b'\340A\003'
  _GETRELEASEREQUEST._serialized_start=126
  _GETRELEASEREQUEST._serialized_end=167
  _GETRELEASERESPONSE._serialized_start=169
  _GETRELEASERESPONSE._serialized_end=247
  _CLIRELEASE._serialized_start=250
  _CLIRELEASE._serialized_end=392
  _CLISERVICE._serialized_start=394
  _CLISERVICE._serialized_end=507
# @@protoc_insertion_point(module_scope)
