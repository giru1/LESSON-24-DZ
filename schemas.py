from marshmallow import Schema, fields
from enum import Enum, StrEnum


class CmdEnums(StrEnum):
    filter = 'filter'
    map = 'map'
    unique = 'unique'
    sort = 'sort'
    limit = 'limit'
    regex = 'regex'


class RequestArgs(Schema):
    uery = fields.Str(required=False)
    cmd1 = fields.Enum(CmdEnums, required=False)
    cmd2 = fields.Enum(CmdEnums, required=False)
    value1 = fields.Str(required=False)
    value2 = fields.Str(required=False)
    file_name = fields.Str(required=True)


class CMD:
    name = fields.Str()


