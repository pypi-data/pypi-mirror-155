# Copyright (c) Mathieu Fenniak
# Copyright (c) The Contributors
# All rights reserved.
#
# https://github.com/tlocke/pg8000
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# * The name of the author may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from collections import defaultdict

import codecs
import socket
import struct
from collections import defaultdict, deque
from hashlib import md5
from io import TextIOBase
from itertools import count
from struct import Struct


from datetime import (
    date as Date,
    datetime as Datetime,
    time as Time,
    timedelta as Timedelta,
    timezone as Timezone,
)
from decimal import Decimal
from enum import Enum
from ipaddress import (
    IPv4Address,
    IPv4Network,
    IPv6Address,
    IPv6Network,
    ip_address,
    ip_network,
)
from json import dumps, loads
from uuid import UUID

class Error(Exception):
    """Generic exception that is the base exception of all other error
    exceptions.

    This exception is part of the `DBAPI 2.0 specification
    <http://www.python.org/dev/peps/pep-0249/>`_.
    """

    pass


class InterfaceError(Error):
    """Generic exception raised for errors that are related to the database
    interface rather than the database itself.  For example, if the interface
    attempts to use an SSL connection but the server refuses, an InterfaceError
    will be raised.

    This exception is part of the `DBAPI 2.0 specification
    <http://www.python.org/dev/peps/pep-0249/>`_.
    """

    pass


class DatabaseError(Error):
    """Generic exception raised for errors that are related to the database.

    This exception is part of the `DBAPI 2.0 specification
    <http://www.python.org/dev/peps/pep-0249/>`_.
    """

    pass


ANY_ARRAY = 2277
BIGINT = 20
BIGINT_ARRAY = 1016
BOOLEAN = 16
BOOLEAN_ARRAY = 1000
BYTES = 17
BYTES_ARRAY = 1001
CHAR = 1042
CHAR_ARRAY = 1014
CIDR = 650
CIDR_ARRAY = 651
CSTRING = 2275
CSTRING_ARRAY = 1263
DATE = 1082
DATE_ARRAY = 1182
FLOAT = 701
FLOAT_ARRAY = 1022
INET = 869
INET_ARRAY = 1041
INT2VECTOR = 22
INTEGER = 23
INTEGER_ARRAY = 1007
INTERVAL = 1186
INTERVAL_ARRAY = 1187
OID = 26
JSON = 114
JSON_ARRAY = 199
JSONB = 3802
JSONB_ARRAY = 3807
MACADDR = 829
MONEY = 790
MONEY_ARRAY = 791
NAME = 19
NAME_ARRAY = 1003
NUMERIC = 1700
NUMERIC_ARRAY = 1231
NULLTYPE = -1
OID = 26
POINT = 600
REAL = 700
REAL_ARRAY = 1021
SMALLINT = 21
SMALLINT_ARRAY = 1005
SMALLINT_VECTOR = 22
STRING = 1043
TEXT = 25
TEXT_ARRAY = 1009
TIME = 1083
TIME_ARRAY = 1183
TIMESTAMP = 1114
TIMESTAMP_ARRAY = 1115
TIMESTAMPTZ = 1184
TIMESTAMPTZ_ARRAY = 1185
UNKNOWN = 705
UUID_TYPE = 2950
UUID_ARRAY = 2951
VARCHAR = 1043
VARCHAR_ARRAY = 1015
XID = 28


MIN_INT2, MAX_INT2 = -(2**15), 2**15
MIN_INT4, MAX_INT4 = -(2**31), 2**31
MIN_INT8, MAX_INT8 = -(2**63), 2**63


def bool_in(data):
    return data == "t"


def bool_out(v):
    return "true" if v else "false"


def bytes_in(data):
    return bytes.fromhex(data[2:])


def bytes_out(v):
    return "\\x" + v.hex()


def cidr_out(v):
    return str(v)


def cidr_in(data):
    return ip_network(data, False) if "/" in data else ip_address(data)


def date_in(data):
    if data in ("infinity", "-infinity"):
        return data
    else:
        return Datetime.strptime(data, "%Y-%m-%d").date()


def date_out(v):
    return v.isoformat()


def datetime_out(v):
    if v.tzinfo is None:
        return v.isoformat()
    else:
        return v.astimezone(Timezone.utc).isoformat()


def enum_out(v):
    return str(v.value)


def float_out(v):
    return str(v)


def inet_in(data):
    return ip_network(data, False) if "/" in data else ip_address(data)


def inet_out(v):
    return str(v)


def int_in(data):
    return int(data)


def int_out(v):
    return str(v)


def interval_in(data):
    t = {}

    curr_val = None
    for k in data.split():
        if ":" in k:
            t["hours"], t["minutes"], t["seconds"] = map(float, k.split(":"))
        else:
            try:
                curr_val = float(k)
            except ValueError:
                t[PGInterval.UNIT_MAP[k]] = curr_val

    for n in ["weeks", "months", "years", "decades", "centuries", "millennia"]:
        if n in t:
            raise InterfaceError(
                f"Can't fit the interval {t} into a datetime.timedelta."
            )

    return Timedelta(**t)


def interval_out(v):
    return f"{v.days} days {v.seconds} seconds {v.microseconds} microseconds"


def json_in(data):
    return loads(data)


def json_out(v):
    return dumps(v)


def null_out(v):
    return None


def numeric_in(data):
    return Decimal(data)


def numeric_out(d):
    return str(d)


def pg_interval_in(data):
    return PGInterval.from_str(data)


def pg_interval_out(v):
    return str(v)


def string_in(data):
    return data


def string_out(v):
    return v


def time_in(data):
    pattern = "%H:%M:%S.%f" if "." in data else "%H:%M:%S"
    return Datetime.strptime(data, pattern).time()


def time_out(v):
    return v.isoformat()


def timestamp_in(data):
    if data in ("infinity", "-infinity"):
        return data

    pattern = "%Y-%m-%d %H:%M:%S.%f" if "." in data else "%Y-%m-%d %H:%M:%S"
    return Datetime.strptime(data, pattern)


def timestamptz_in(data):
    patt = "%Y-%m-%d %H:%M:%S.%f%z" if "." in data else "%Y-%m-%d %H:%M:%S%z"
    return Datetime.strptime(data + "00", patt)


def unknown_out(v):
    return str(v)


def vector_in(data):
    return eval("[" + data.replace(" ", ",") + "]")


def uuid_out(v):
    return str(v)


def uuid_in(data):
    return UUID(data)


class PGInterval:
    UNIT_MAP = {
        "year": "years",
        "years": "years",
        "millennia": "millennia",
        "millenium": "millennia",
        "centuries": "centuries",
        "century": "centuries",
        "decades": "decades",
        "decade": "decades",
        "years": "years",
        "year": "years",
        "months": "months",
        "month": "months",
        "mon": "months",
        "mons": "months",
        "weeks": "weeks",
        "week": "weeks",
        "days": "days",
        "day": "days",
        "hours": "hours",
        "hour": "hours",
        "minutes": "minutes",
        "minute": "minutes",
        "seconds": "seconds",
        "second": "seconds",
        "microseconds": "microseconds",
        "microsecond": "microseconds",
    }

    @staticmethod
    def from_str(interval_str):
        t = {}

        curr_val = None
        for k in interval_str.split():
            if ":" in k:
                hours_str, minutes_str, seconds_str = k.split(":")
                hours = int(hours_str)
                if hours != 0:
                    t["hours"] = hours
                minutes = int(minutes_str)
                if minutes != 0:
                    t["minutes"] = minutes
                try:
                    seconds = int(seconds_str)
                except ValueError:
                    seconds = float(seconds_str)

                if seconds != 0:
                    t["seconds"] = seconds

            else:
                try:
                    curr_val = int(k)
                except ValueError:
                    t[PGInterval.UNIT_MAP[k]] = curr_val

        return PGInterval(**t)

    def __init__(
        self,
        millennia=None,
        centuries=None,
        decades=None,
        years=None,
        months=None,
        weeks=None,
        days=None,
        hours=None,
        minutes=None,
        seconds=None,
        microseconds=None,
    ):
        self.millennia = millennia
        self.centuries = centuries
        self.decades = decades
        self.years = years
        self.months = months
        self.weeks = weeks
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.microseconds = microseconds

    def __repr__(self):
        return f"<PGInterval {self}>"

    def __str__(self):
        pairs = (
            ("millennia", self.millennia),
            ("centuries", self.centuries),
            ("decades", self.decades),
            ("years", self.years),
            ("months", self.months),
            ("weeks", self.weeks),
            ("days", self.days),
            ("hours", self.hours),
            ("minutes", self.minutes),
            ("seconds", self.seconds),
            ("microseconds", self.microseconds),
        )
        return " ".join(f"{v} {n}" for n, v in pairs if v is not None)

    def normalize(self):
        months = 0
        if self.months is not None:
            months += self.months
        if self.years is not None:
            months += self.years * 12

        days = 0
        if self.days is not None:
            days += self.days
        if self.weeks is not None:
            days += self.weeks * 7

        seconds = 0
        if self.hours is not None:
            seconds += self.hours * 60 * 60
        if self.minutes is not None:
            seconds += self.minutes * 60
        if self.seconds is not None:
            seconds += self.seconds
        if self.microseconds is not None:
            seconds += self.microseconds / 1000000

        return PGInterval(months=months, days=days, seconds=seconds)

    def __eq__(self, other):
        if isinstance(other, PGInterval):
            s = self.normalize()
            o = other.normalize()
            return s.months == o.months and s.days == o.days and s.seconds == o.seconds
        else:
            return False


class ArrayState(Enum):
    InString = 1
    InEscape = 2
    InValue = 3
    Out = 4


def _parse_array(data, adapter):
    state = ArrayState.Out
    stack = [[]]
    val = []
    for c in data:
        if state == ArrayState.InValue:
            if c in ("}", ","):
                value = "".join(val)
                stack[-1].append(None if value == "NULL" else adapter(value))
                state = ArrayState.Out
            else:
                val.append(c)

        if state == ArrayState.Out:
            if c == "{":
                a = []
                stack[-1].append(a)
                stack.append(a)
            elif c == "}":
                stack.pop()
            elif c == ",":
                pass
            elif c == '"':
                val = []
                state = ArrayState.InString
            else:
                val = [c]
                state = ArrayState.InValue

        elif state == ArrayState.InString:
            if c == '"':
                stack[-1].append(adapter("".join(val)))
                state = ArrayState.Out
            elif c == "\\":
                state = ArrayState.InEscape
            else:
                val.append(c)
        elif state == ArrayState.InEscape:
            val.append(c)
            state = ArrayState.InString

    return stack[0][0]


def _array_in(adapter):
    def f(data):
        return _parse_array(data, adapter)

    return f


bool_array_in = _array_in(bool_in)
bytes_array_in = _array_in(bytes_in)
cidr_array_in = _array_in(cidr_in)
date_array_in = _array_in(date_in)
inet_array_in = _array_in(inet_in)
int_array_in = _array_in(int)
interval_array_in = _array_in(interval_in)
json_array_in = _array_in(json_in)
float_array_in = _array_in(float)
numeric_array_in = _array_in(numeric_in)
string_array_in = _array_in(string_in)
time_array_in = _array_in(time_in)
timestamp_array_in = _array_in(timestamp_in)
timestamptz_array_in = _array_in(timestamptz_in)
uuid_array_in = _array_in(uuid_in)


def array_string_escape(v):
    cs = []
    for c in v:
        if c == "\\":
            cs.append("\\")
        elif c == '"':
            cs.append("\\")
        cs.append(c)
    val = "".join(cs)
    if (
        len(val) == 0
        or val == "NULL"
        or any([c in val for c in ("{", "}", ",", " ", "\\")])
    ):
        val = f'"{val}"'
    return val


def array_out(ar):
    result = []
    for v in ar:

        if isinstance(v, (list, tuple)):
            val = array_out(v)

        elif v is None:
            val = "NULL"

        elif isinstance(v, dict):
            val = array_string_escape(json_out(v))

        elif isinstance(v, (bytes, bytearray)):
            val = f'"\\{bytes_out(v)}"'

        elif isinstance(v, str):
            val = array_string_escape(v)

        else:
            val = make_param(PY_TYPES, v)

        result.append(val)

    return "{" + ",".join(result) + "}"


PY_PG = {
    Date: DATE,
    Decimal: NUMERIC,
    IPv4Address: INET,
    IPv6Address: INET,
    IPv4Network: INET,
    IPv6Network: INET,
    PGInterval: INTERVAL,
    Time: TIME,
    Timedelta: INTERVAL,
    UUID: UUID_TYPE,
    bool: BOOLEAN,
    bytearray: BYTES,
    dict: JSONB,
    float: FLOAT,
    type(None): NULLTYPE,
    bytes: BYTES,
    str: TEXT,
}


PY_TYPES = {
    Date: date_out,  # date
    Datetime: datetime_out,
    Decimal: numeric_out,  # numeric
    Enum: enum_out,  # enum
    IPv4Address: inet_out,  # inet
    IPv6Address: inet_out,  # inet
    IPv4Network: inet_out,  # inet
    IPv6Network: inet_out,  # inet
    PGInterval: interval_out,  # interval
    Time: time_out,  # time
    Timedelta: interval_out,  # interval
    UUID: uuid_out,  # uuid
    bool: bool_out,  # bool
    bytearray: bytes_out,  # bytea
    dict: json_out,  # jsonb
    float: float_out,  # float8
    type(None): null_out,  # null
    bytes: bytes_out,  # bytea
    str: string_out,  # unknown
    int: int_out,
    list: array_out,
    tuple: array_out,
}


PG_TYPES = {
    BIGINT: int,  # int8
    BIGINT_ARRAY: int_array_in,  # int8[]
    BOOLEAN: bool_in,  # bool
    BOOLEAN_ARRAY: bool_array_in,  # bool[]
    BYTES: bytes_in,  # bytea
    BYTES_ARRAY: bytes_array_in,  # bytea[]
    CHAR: string_in,  # char
    CHAR_ARRAY: string_array_in,  # char[]
    CIDR_ARRAY: cidr_array_in,  # cidr[]
    CSTRING: string_in,  # cstring
    CSTRING_ARRAY: string_array_in,  # cstring[]
    DATE: date_in,  # date
    DATE_ARRAY: date_array_in,  # date[]
    FLOAT: float,  # float8
    FLOAT_ARRAY: float_array_in,  # float8[]
    INET: inet_in,  # inet
    INET_ARRAY: inet_array_in,  # inet[]
    INTEGER: int,  # int4
    INTEGER_ARRAY: int_array_in,  # int4[]
    JSON: json_in,  # json
    JSON_ARRAY: json_array_in,  # json[]
    JSONB: json_in,  # jsonb
    JSONB_ARRAY: json_array_in,  # jsonb[]
    MACADDR: string_in,  # MACADDR type
    MONEY: string_in,  # money
    MONEY_ARRAY: string_array_in,  # money[]
    NAME: string_in,  # name
    NAME_ARRAY: string_array_in,  # name[]
    NUMERIC: numeric_in,  # numeric
    NUMERIC_ARRAY: numeric_array_in,  # numeric[]
    OID: int,  # oid
    INTERVAL: interval_in,  # interval
    INTERVAL_ARRAY: interval_array_in,  # interval[]
    REAL: float,  # float4
    REAL_ARRAY: float_array_in,  # float4[]
    SMALLINT: int,  # int2
    SMALLINT_ARRAY: int_array_in,  # int2[]
    SMALLINT_VECTOR: vector_in,  # int2vector
    TEXT: string_in,  # text
    TEXT_ARRAY: string_array_in,  # text[]
    TIME: time_in,  # time
    TIME_ARRAY: time_array_in,  # time[]
    INTERVAL: interval_in,  # interval
    TIMESTAMP: timestamp_in,  # timestamp
    TIMESTAMP_ARRAY: timestamp_array_in,  # timestamp
    TIMESTAMPTZ: timestamptz_in,  # timestamptz
    TIMESTAMPTZ_ARRAY: timestamptz_array_in,  # timestamptz
    UNKNOWN: string_in,  # unknown
    UUID_ARRAY: uuid_array_in,  # uuid[]
    UUID_TYPE: uuid_in,  # uuid
    VARCHAR: string_in,  # varchar
    VARCHAR_ARRAY: string_array_in,  # varchar[]
    XID: int,  # xid
}


# PostgreSQL encodings:
# https://www.postgresql.org/docs/current/multibyte.html
#
# Python encodings:
# https://docs.python.org/3/library/codecs.html
#
# Commented out encodings don't require a name change between PostgreSQL and
# Python.  If the py side is None, then the encoding isn't supported.
PG_PY_ENCODINGS = {
    # Not supported:
    "mule_internal": None,
    "euc_tw": None,
    # Name fine as-is:
    # "euc_jp",
    # "euc_jis_2004",
    # "euc_kr",
    # "gb18030",
    # "gbk",
    # "johab",
    # "sjis",
    # "shift_jis_2004",
    # "uhc",
    # "utf8",
    # Different name:
    "euc_cn": "gb2312",
    "iso_8859_5": "is8859_5",
    "iso_8859_6": "is8859_6",
    "iso_8859_7": "is8859_7",
    "iso_8859_8": "is8859_8",
    "koi8": "koi8_r",
    "latin1": "iso8859-1",
    "latin2": "iso8859_2",
    "latin3": "iso8859_3",
    "latin4": "iso8859_4",
    "latin5": "iso8859_9",
    "latin6": "iso8859_10",
    "latin7": "iso8859_13",
    "latin8": "iso8859_14",
    "latin9": "iso8859_15",
    "sql_ascii": "ascii",
    "win866": "cp886",
    "win874": "cp874",
    "win1250": "cp1250",
    "win1251": "cp1251",
    "win1252": "cp1252",
    "win1253": "cp1253",
    "win1254": "cp1254",
    "win1255": "cp1255",
    "win1256": "cp1256",
    "win1257": "cp1257",
    "win1258": "cp1258",
    "unicode": "utf-8",  # Needed for Amazon Redshift
}


def make_param(py_types, value):
    try:
        func = py_types[type(value)]
    except KeyError:
        func = str
        for k, v in py_types.items():
            try:
                if isinstance(value, k):
                    func = v
                    break
            except TypeError:
                pass

    return func(value)


def make_params(py_types, values):
    return tuple([make_param(py_types, v) for v in values])


def identifier(sql):
    if not isinstance(sql, str):
        raise InterfaceError("identifier must be a str")

    if len(sql) == 0:
        raise InterfaceError("identifier must be > 0 characters in length")

    quote = not sql[0].isalpha()

    for c in sql[1:]:
        if not (c.isalpha() or c.isdecimal() or c in "_$"):
            if c == "\u0000":
                raise InterfaceError(
                    "identifier cannot contain the code zero character"
                )
            quote = True
            break

    if quote:
        sql = sql.replace('"', '""')
        return f'"{sql}"'
    else:
        return sql


def literal(value):
    if value is None:
        return "NULL"
    elif isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    elif isinstance(value, (int, float, Decimal)):
        return str(value)
    elif isinstance(value, (bytes, bytearray)):
        return f"X'{value.hex()}'"
    elif isinstance(value, Date):
        return f"'{date_out(value)}'"
    elif isinstance(value, Time):
        return f"'{time_out(value)}'"
    elif isinstance(value, Datetime):
        return f"'{datetime_out(value)}'"
    elif isinstance(value, Timedelta):
        return f"'{interval_out(value)}'"
    else:
        val = str(value).replace("'", "''")
        return f"'{val}'"


def pack_funcs(fmt):
    struc = Struct(f"!{fmt}")
    return struc.pack, struc.unpack_from


i_pack, i_unpack = pack_funcs("i")
h_pack, h_unpack = pack_funcs("h")
ii_pack, ii_unpack = pack_funcs("ii")
ihihih_pack, ihihih_unpack = pack_funcs("ihihih")
ci_pack, ci_unpack = pack_funcs("ci")
bh_pack, bh_unpack = pack_funcs("bh")
cccc_pack, cccc_unpack = pack_funcs("cccc")





NULL_BYTE = b"\x00"


# Message codes
NOTICE_RESPONSE = b"N"
AUTHENTICATION_REQUEST = b"R"
PARAMETER_STATUS = b"S"
BACKEND_KEY_DATA = b"K"
READY_FOR_QUERY = b"Z"
ROW_DESCRIPTION = b"T"
ERROR_RESPONSE = b"E"
DATA_ROW = b"D"
COMMAND_COMPLETE = b"C"
PARSE_COMPLETE = b"1"
BIND_COMPLETE = b"2"
CLOSE_COMPLETE = b"3"
PORTAL_SUSPENDED = b"s"
NO_DATA = b"n"
PARAMETER_DESCRIPTION = b"t"
NOTIFICATION_RESPONSE = b"A"
COPY_DONE = b"c"
COPY_DATA = b"d"
COPY_IN_RESPONSE = b"G"
COPY_OUT_RESPONSE = b"H"
EMPTY_QUERY_RESPONSE = b"I"

BIND = b"B"
PARSE = b"P"
QUERY = b"Q"
EXECUTE = b"E"
FLUSH = b"H"
SYNC = b"S"
PASSWORD = b"p"
DESCRIBE = b"D"
TERMINATE = b"X"
CLOSE = b"C"


def _create_message(code, data=b""):
    return code + i_pack(len(data) + 4) + data


FLUSH_MSG = _create_message(FLUSH)
SYNC_MSG = _create_message(SYNC)
TERMINATE_MSG = _create_message(TERMINATE)
COPY_DONE_MSG = _create_message(COPY_DONE)
EXECUTE_MSG = _create_message(EXECUTE, NULL_BYTE + i_pack(0))

# DESCRIBE constants
STATEMENT = b"S"
PORTAL = b"P"

# ErrorResponse codes
RESPONSE_SEVERITY = "S"  # always present
RESPONSE_SEVERITY = "V"  # always present
RESPONSE_CODE = "C"  # always present
RESPONSE_MSG = "M"  # always present
RESPONSE_DETAIL = "D"
RESPONSE_HINT = "H"
RESPONSE_POSITION = "P"
RESPONSE__POSITION = "p"
RESPONSE__QUERY = "q"
RESPONSE_WHERE = "W"
RESPONSE_FILE = "F"
RESPONSE_LINE = "L"
RESPONSE_ROUTINE = "R"

IDLE = b"I"
IDLE_IN_TRANSACTION = b"T"
IDLE_IN_FAILED_TRANSACTION = b"E"


class CoreConnection:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __init__(
        self,
        user,
        host="localhost",
        database=None,
        port=5432,
        password=None,
        source_address=None,
        unix_sock=None,
        ssl_context=None,
        timeout=None,
        tcp_keepalive=True,
        application_name=None,
        replication=None,
    ):
        self._client_encoding = "utf8"
        self._commands_with_count = (
            b"INSERT",
            b"DELETE",
            b"UPDATE",
            b"MOVE",
            b"FETCH",
            b"COPY",
            b"SELECT",
        )
        self.notifications = deque(maxlen=100)
        self.notices = deque(maxlen=100)
        self.parameter_statuses = deque(maxlen=100)

        if user is None:
            raise InterfaceError("The 'user' connection parameter cannot be None")

        init_params = {
            "user": user,
            "database": database,
            "application_name": application_name,
            "replication": replication,
        }

        for k, v in tuple(init_params.items()):
            if isinstance(v, str):
                init_params[k] = v.encode("utf8")
            elif v is None:
                del init_params[k]
            elif not isinstance(v, (bytes, bytearray)):
                raise InterfaceError(f"The parameter {k} can't be of type {type(v)}.")

        self.user = init_params["user"]

        if isinstance(password, str):
            self.password = password.encode("utf8")
        else:
            self.password = password

        self.autocommit = False
        self._xid = None
        self._statement_nums = set()

        self._caches = {}

        if unix_sock is None and host is not None:
            try:
                self._usock = socket.create_connection(
                    (host, port), timeout, source_address
                )
            except socket.error as e:
                raise InterfaceError(
                    f"Can't create a connection to host {host} and port {port} "
                    f"(timeout is {timeout} and source_address is {source_address})."
                ) from e

        elif unix_sock is not None:
            try:
                if not hasattr(socket, "AF_UNIX"):
                    raise InterfaceError(
                        "attempt to connect to unix socket on unsupported platform"
                    )
                self._usock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self._usock.settimeout(timeout)
                self._usock.connect(unix_sock)
            except socket.error as e:
                if self._usock is not None:
                    self._usock.close()
                raise InterfaceError("communication error") from e

        else:
            raise InterfaceError("one of host or unix_sock must be provided")

        if tcp_keepalive:
            self._usock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        self.channel_binding = None
        if ssl_context is not None:
            try:
                import ssl

                if ssl_context is True:
                    ssl_context = ssl.create_default_context()

                request_ssl = getattr(ssl_context, "request_ssl", True)

                if request_ssl:
                    # Int32(8) - Message length, including self.
                    # Int32(80877103) - The SSL request code.
                    self._usock.sendall(ii_pack(8, 80877103))
                    resp = self._usock.recv(1)
                    if resp != b"S":
                        raise InterfaceError("Server refuses SSL")

                self._usock = ssl_context.wrap_socket(self._usock, server_hostname=host)

                if request_ssl:
                    self.channel_binding = scramp.make_channel_binding(
                        "tls-server-end-point", self._usock
                    )

            except ImportError:
                raise InterfaceError(
                    "SSL required but ssl module not available in this python "
                    "installation."
                )

        self._sock = self._usock.makefile(mode="rwb")

        def sock_flush():
            try:
                self._sock.flush()
            except OSError as e:
                raise InterfaceError("network error on flush") from e

        self._flush = sock_flush

        def sock_read(b):
            try:
                return self._sock.read(b)
            except OSError as e:
                raise InterfaceError("network error on read") from e

        self._read = sock_read

        def sock_write(d):
            try:
                self._sock.write(d)
            except OSError as e:
                raise InterfaceError("network error on write") from e

        self._write = sock_write
        self._backend_key_data = None

        self.pg_types = defaultdict(lambda: string_in, PG_TYPES)
        self.py_types = dict(PY_TYPES)

        self.message_types = {
            NOTICE_RESPONSE: self.handle_NOTICE_RESPONSE,
            AUTHENTICATION_REQUEST: self.handle_AUTHENTICATION_REQUEST,
            PARAMETER_STATUS: self.handle_PARAMETER_STATUS,
            BACKEND_KEY_DATA: self.handle_BACKEND_KEY_DATA,
            READY_FOR_QUERY: self.handle_READY_FOR_QUERY,
            ROW_DESCRIPTION: self.handle_ROW_DESCRIPTION,
            ERROR_RESPONSE: self.handle_ERROR_RESPONSE,
            EMPTY_QUERY_RESPONSE: self.handle_EMPTY_QUERY_RESPONSE,
            DATA_ROW: self.handle_DATA_ROW,
            COMMAND_COMPLETE: self.handle_COMMAND_COMPLETE,
            PARSE_COMPLETE: self.handle_PARSE_COMPLETE,
            BIND_COMPLETE: self.handle_BIND_COMPLETE,
            CLOSE_COMPLETE: self.handle_CLOSE_COMPLETE,
            PORTAL_SUSPENDED: self.handle_PORTAL_SUSPENDED,
            NO_DATA: self.handle_NO_DATA,
            PARAMETER_DESCRIPTION: self.handle_PARAMETER_DESCRIPTION,
            NOTIFICATION_RESPONSE: self.handle_NOTIFICATION_RESPONSE,
            COPY_DONE: self.handle_COPY_DONE,
            COPY_DATA: self.handle_COPY_DATA,
            COPY_IN_RESPONSE: self.handle_COPY_IN_RESPONSE,
            COPY_OUT_RESPONSE: self.handle_COPY_OUT_RESPONSE,
        }

        # Int32 - Message length, including self.
        # Int32(196608) - Protocol version number.  Version 3.0.
        # Any number of key/value pairs, terminated by a zero byte:
        #   String - A parameter name (user, database, or options)
        #   String - Parameter value
        protocol = 196608
        val = bytearray(i_pack(protocol))

        for k, v in init_params.items():
            val.extend(k.encode("ascii") + NULL_BYTE + v + NULL_BYTE)
        val.append(0)
        self._write(i_pack(len(val) + 4))
        self._write(val)
        self._flush()

        code = self.error = None
        while code not in (READY_FOR_QUERY, ERROR_RESPONSE):
            code, data_len = ci_unpack(self._read(5))
            self.message_types[code](self._read(data_len - 4), None)
        if self.error is not None:
            raise self.error

        self.in_transaction = False

    def register_out_adapter(self, typ, out_func):
        self.py_types[typ] = out_func

    def register_in_adapter(self, oid, in_func):
        self.pg_types[oid] = in_func

    def handle_ERROR_RESPONSE(self, data, context):
        msg = {
            s[:1].decode("ascii"): s[1:].decode(self._client_encoding, errors="replace")
            for s in data.split(NULL_BYTE)
            if s != b""
        }

        self.error = DatabaseError(msg)

    def handle_EMPTY_QUERY_RESPONSE(self, data, context):
        self.error = DatabaseError("query was empty")

    def handle_CLOSE_COMPLETE(self, data, context):
        pass

    def handle_PARSE_COMPLETE(self, data, context):
        # Byte1('1') - Identifier.
        # Int32(4) - Message length, including self.
        pass

    def handle_BIND_COMPLETE(self, data, context):
        pass

    def handle_PORTAL_SUSPENDED(self, data, context):
        pass

    def handle_PARAMETER_DESCRIPTION(self, data, context):
        """https://www.postgresql.org/docs/current/protocol-message-formats.html"""

        # count = h_unpack(data)[0]
        # context.parameter_oids = unpack_from("!" + "i" * count, data, 2)

    def handle_COPY_DONE(self, data, context):
        pass

    def handle_COPY_OUT_RESPONSE(self, data, context):
        """https://www.postgresql.org/docs/current/protocol-message-formats.html"""

        is_binary, num_cols = bh_unpack(data)
        # column_formats = unpack_from('!' + 'h' * num_cols, data, 3)

        if context.stream is None:
            raise InterfaceError(
                "An output stream is required for the COPY OUT response."
            )

        elif isinstance(context.stream, TextIOBase):
            if is_binary:
                raise InterfaceError(
                    "The COPY OUT stream is binary, but the stream parameter is text."
                )
            else:
                decode = codecs.getdecoder(self._client_encoding)

                def w(data):
                    context.stream.write(decode(data)[0])

                context.stream_write = w

        else:
            context.stream_write = context.stream.write

    def handle_COPY_DATA(self, data, context):
        context.stream_write(data)

    def handle_COPY_IN_RESPONSE(self, data, context):
        """https://www.postgresql.org/docs/current/protocol-message-formats.html"""
        is_binary, num_cols = bh_unpack(data)
        # column_formats = unpack_from('!' + 'h' * num_cols, data, 3)

        if context.stream is None:
            raise InterfaceError(
                "An input stream is required for the COPY IN response."
            )

        elif isinstance(context.stream, TextIOBase):
            if is_binary:
                raise InterfaceError(
                    "The COPY IN stream is binary, but the stream parameter is text."
                )

            else:

                def ri(bffr):
                    bffr.clear()
                    bffr.extend(context.stream.read(4096).encode(self._client_encoding))
                    return len(bffr)

                readinto = ri
        else:
            readinto = context.stream.readinto

        bffr = bytearray(8192)
        while True:
            bytes_read = readinto(bffr)
            if bytes_read == 0:
                break
            self._write(COPY_DATA)
            self._write(i_pack(bytes_read + 4))
            self._write(bffr[:bytes_read])
            self._flush()

        # Send CopyDone
        self._write(COPY_DONE_MSG)
        self._write(SYNC_MSG)
        self._flush()

    def handle_NOTIFICATION_RESPONSE(self, data, context):
        """https://www.postgresql.org/docs/current/protocol-message-formats.html"""
        backend_pid = i_unpack(data)[0]
        idx = 4
        null_idx = data.find(NULL_BYTE, idx)
        channel = data[idx:null_idx].decode("ascii")
        payload = data[null_idx + 1 : -1].decode("ascii")

        self.notifications.append((backend_pid, channel, payload))

    def close(self):
        """Closes the database connection.

        This function is part of the `DBAPI 2.0 specification
        <http://www.python.org/dev/peps/pep-0249/>`_.
        """
        try:
            self._write(TERMINATE_MSG)
            self._flush()
            self._sock.close()
        except AttributeError:
            raise InterfaceError("connection is closed")
        except ValueError:
            raise InterfaceError("connection is closed")
        except socket.error:
            pass
        finally:
            self._usock.close()
            self._sock = None

    def handle_AUTHENTICATION_REQUEST(self, data, context):
        """https://www.postgresql.org/docs/current/protocol-message-formats.html"""

        auth_code = i_unpack(data)[0]
        if auth_code == 0:
            pass
        elif auth_code == 3:
            if self.password is None:
                raise InterfaceError(
                    "server requesting password authentication, but no password was "
                    "provided"
                )
            self._send_message(PASSWORD, self.password + NULL_BYTE)
            self._flush()

        elif auth_code == 5:
            salt = b"".join(cccc_unpack(data, 4))
            if self.password is None:
                raise InterfaceError(
                    "server requesting MD5 password authentication, but no password "
                    "was provided"
                )
            pwd = b"md5" + md5(
                md5(self.password + self.user).hexdigest().encode("ascii") + salt
            ).hexdigest().encode("ascii")
            self._send_message(PASSWORD, pwd + NULL_BYTE)
            self._flush()

        elif auth_code == 10:
            # AuthenticationSASL
            mechanisms = [m.decode("ascii") for m in data[4:-2].split(NULL_BYTE)]

            self.auth = scramp.ScramClient(
                mechanisms,
                self.user.decode("utf8"),
                self.password.decode("utf8"),
                channel_binding=self.channel_binding,
            )

            init = self.auth.get_client_first().encode("utf8")
            mech = self.auth.mechanism_name.encode("ascii") + NULL_BYTE

            # SASLInitialResponse
            self._send_message(PASSWORD, mech + i_pack(len(init)) + init)
            self._flush()

        elif auth_code == 11:
            # AuthenticationSASLContinue
            self.auth.set_server_first(data[4:].decode("utf8"))

            # SASLResponse
            msg = self.auth.get_client_final().encode("utf8")
            self._send_message(PASSWORD, msg)
            self._flush()

        elif auth_code == 12:
            # AuthenticationSASLFinal
            self.auth.set_server_final(data[4:].decode("utf8"))

        elif auth_code in (2, 4, 6, 7, 8, 9):
            raise InterfaceError(
                f"Authentication method {auth_code} not supported by pg8000."
            )
        else:
            raise InterfaceError(
                f"Authentication method {auth_code} not recognized by pg8000."
            )

    def handle_READY_FOR_QUERY(self, data, context):
        self.in_transaction = data != IDLE

    def handle_BACKEND_KEY_DATA(self, data, context):
        self._backend_key_data = data

    def handle_ROW_DESCRIPTION(self, data, context):
        count = h_unpack(data)[0]
        idx = 2
        columns = []
        input_funcs = []
        for i in range(count):
            name = data[idx : data.find(NULL_BYTE, idx)]
            idx += len(name) + 1
            field = dict(
                zip(
                    (
                        "table_oid",
                        "column_attrnum",
                        "type_oid",
                        "type_size",
                        "type_modifier",
                        "format",
                    ),
                    ihihih_unpack(data, idx),
                )
            )
            field["name"] = name.decode(self._client_encoding)
            idx += 18
            columns.append(field)
            input_funcs.append(self.pg_types[field["type_oid"]])

        context.columns = columns
        context.input_funcs = input_funcs
        if context.rows is None:
            context.rows = []

    def send_PARSE(self, statement_name_bin, statement, oids=()):

        val = bytearray(statement_name_bin)
        val.extend(statement.encode(self._client_encoding) + NULL_BYTE)
        val.extend(h_pack(len(oids)))
        for oid in oids:
            val.extend(i_pack(0 if oid == -1 else oid))

        self._send_message(PARSE, val)
        self._write(FLUSH_MSG)

    def send_DESCRIBE_STATEMENT(self, statement_name_bin):
        self._send_message(DESCRIBE, STATEMENT + statement_name_bin)
        self._write(FLUSH_MSG)

    def send_QUERY(self, sql):
        self._send_message(QUERY, sql.encode(self._client_encoding) + NULL_BYTE)

    def execute_simple(self, statement):
        context = Context()

        self.send_QUERY(statement)
        self._flush()
        self.handle_messages(context)

        return context

    def execute_unnamed(self, statement, vals=(), oids=(), stream=None):
        context = Context(stream=stream)

        self.send_PARSE(NULL_BYTE, statement, oids)
        self._write(SYNC_MSG)
        self._flush()
        self.handle_messages(context)
        self.send_DESCRIBE_STATEMENT(NULL_BYTE)

        self._write(SYNC_MSG)

        try:
            self._flush()
        except AttributeError as e:
            if self._sock is None:
                raise InterfaceError("connection is closed")
            else:
                raise e
        params = make_params(self.py_types, vals)
        self.send_BIND(NULL_BYTE, params)
        self.handle_messages(context)
        self.send_EXECUTE()

        self._write(SYNC_MSG)
        self._flush()
        self.handle_messages(context)

        return context

    def prepare_statement(self, statement, oids=None):

        for i in count():
            statement_name = f"pg8000_statement_{i}"
            statement_name_bin = statement_name.encode("ascii") + NULL_BYTE
            if statement_name_bin not in self._statement_nums:
                self._statement_nums.add(statement_name_bin)
                break

        self.send_PARSE(statement_name_bin, statement, oids)
        self.send_DESCRIBE_STATEMENT(statement_name_bin)
        self._write(SYNC_MSG)

        try:
            self._flush()
        except AttributeError as e:
            if self._sock is None:
                raise InterfaceError("connection is closed")
            else:
                raise e

        context = Context()
        self.handle_messages(context)

        return statement_name_bin, context.columns, context.input_funcs

    def execute_named(self, statement_name_bin, params, columns, input_funcs):
        context = Context(columns=columns, input_funcs=input_funcs)

        self.send_BIND(statement_name_bin, params)
        self.send_EXECUTE()
        self._write(SYNC_MSG)
        self._flush()
        self.handle_messages(context)
        return context

    def _send_message(self, code, data):
        try:
            self._write(code)
            self._write(i_pack(len(data) + 4))
            self._write(data)
        except ValueError as e:
            if str(e) == "write to closed file":
                raise InterfaceError("connection is closed")
            else:
                raise e
        except AttributeError:
            raise InterfaceError("connection is closed")

    def send_BIND(self, statement_name_bin, params):
        """https://www.postgresql.org/docs/current/protocol-message-formats.html"""

        retval = bytearray(
            NULL_BYTE + statement_name_bin + h_pack(0) + h_pack(len(params))
        )

        for value in params:
            if value is None:
                retval.extend(i_pack(-1))
            else:
                val = value.encode(self._client_encoding)
                retval.extend(i_pack(len(val)))
                retval.extend(val)
        retval.extend(h_pack(0))

        self._send_message(BIND, retval)
        self._write(FLUSH_MSG)

    def send_EXECUTE(self):
        """https://www.postgresql.org/docs/current/protocol-message-formats.html"""
        self._write(EXECUTE_MSG)
        self._write(FLUSH_MSG)

    def handle_NO_DATA(self, msg, context):
        pass

    def handle_COMMAND_COMPLETE(self, data, context):
        values = data[:-1].split(b" ")
        try:
            row_count = int(values[-1])
            if context.row_count == -1:
                context.row_count = row_count
            else:
                context.row_count += row_count
        except ValueError:
            pass

    def handle_DATA_ROW(self, data, context):
        idx = 2
        row = []
        for func in context.input_funcs:
            vlen = i_unpack(data, idx)[0]
            idx += 4
            if vlen == -1:
                v = None
            else:
                v = func(str(data[idx : idx + vlen], encoding=self._client_encoding))
                idx += vlen
            row.append(v)
        context.rows.append(row)

    def handle_messages(self, context):
        code = self.error = None

        while code != READY_FOR_QUERY:

            try:
                code, data_len = ci_unpack(self._read(5))
            except struct.error as e:
                raise InterfaceError("network error on read") from e

            self.message_types[code](self._read(data_len - 4), context)

        if self.error is not None:
            raise self.error

    def close_prepared_statement(self, statement_name_bin):
        """https://www.postgresql.org/docs/current/protocol-message-formats.html"""
        self._send_message(CLOSE, STATEMENT + statement_name_bin)
        self._write(FLUSH_MSG)
        self._write(SYNC_MSG)
        self._flush()
        context = Context()
        self.handle_messages(context)
        self._statement_nums.remove(statement_name_bin)

    def handle_NOTICE_RESPONSE(self, data, context):
        """https://www.postgresql.org/docs/current/protocol-message-formats.html"""
        self.notices.append({s[0:1]: s[1:] for s in data.split(NULL_BYTE)})

    def handle_PARAMETER_STATUS(self, data, context):
        pos = data.find(NULL_BYTE)
        key, value = data[:pos], data[pos + 1 : -1]
        self.parameter_statuses.append((key, value))
        if key == b"client_encoding":
            encoding = value.decode("ascii").lower()
            self._client_encoding = PG_PY_ENCODINGS.get(encoding, encoding)

        elif key == b"integer_datetimes":
            if value == b"on":
                pass

            else:
                pass

        elif key == b"server_version":
            pass


class Context:
    def __init__(self, stream=None, columns=None, input_funcs=None):
        self.rows = None if columns is None else []
        self.row_count = -1
        self.columns = columns
        self.stream = stream
        self.input_funcs = [] if input_funcs is None else input_funcs




OUTSIDE = 0  # outside quoted string
INSIDE_SQ = 1  # inside single-quote string '...'
INSIDE_QI = 2  # inside quoted identifier   "..."
INSIDE_ES = 3  # inside escaped single-quote string, E'...'
INSIDE_PN = 4  # inside parameter name eg. :name
INSIDE_CO = 5  # inside inline comment eg. --


def to_statement(query):
    in_quote_escape = False
    placeholders = []
    output_query = []
    state = OUTSIDE
    prev_c = None
    for i, c in enumerate(query):
        if i + 1 < len(query):
            next_c = query[i + 1]
        else:
            next_c = None

        if state == OUTSIDE:
            if c == "'":
                output_query.append(c)
                if prev_c == "E":
                    state = INSIDE_ES
                else:
                    state = INSIDE_SQ
            elif c == '"':
                output_query.append(c)
                state = INSIDE_QI
            elif c == "-":
                output_query.append(c)
                if prev_c == "-":
                    state = INSIDE_CO
            elif c == ":" and next_c not in ":=" and prev_c != ":":
                state = INSIDE_PN
                placeholders.append("")
            else:
                output_query.append(c)

        elif state == INSIDE_SQ:
            if c == "'":
                if in_quote_escape:
                    in_quote_escape = False
                elif next_c == "'":
                    in_quote_escape = True
                else:
                    state = OUTSIDE
            output_query.append(c)

        elif state == INSIDE_QI:
            if c == '"':
                state = OUTSIDE
            output_query.append(c)

        elif state == INSIDE_ES:
            if c == "'" and prev_c != "\\":
                # check for escaped single-quote
                state = OUTSIDE
            output_query.append(c)

        elif state == INSIDE_PN:
            placeholders[-1] += c
            if next_c is None or (not next_c.isalnum() and next_c != "_"):
                state = OUTSIDE
                try:
                    pidx = placeholders.index(placeholders[-1], 0, -1)
                    output_query.append(f"${pidx + 1}")
                    del placeholders[-1]
                except ValueError:
                    output_query.append(f"${len(placeholders)}")

        elif state == INSIDE_CO:
            output_query.append(c)
            if c == "\n":
                state = OUTSIDE

        prev_c = c

    for reserved in ("types", "stream"):
        if reserved in placeholders:
            raise InterfaceError(
                f"The name '{reserved}' can't be used as a placeholder because it's "
                f"used for another purpose."
            )

    def make_vals(args):
        vals = []
        for p in placeholders:
            try:
                vals.append(args[p])
            except KeyError:
                raise InterfaceError(
                    f"There's a placeholder '{p}' in the query, but no matching "
                    f"keyword argument."
                )
        return tuple(vals)

    return "".join(output_query), make_vals


class Connection(CoreConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._context = None

    @property
    def columns(self):
        context = self._context
        if context is None:
            return None
        return context.columns

    @property
    def row_count(self):
        context = self._context
        if context is None:
            return None
        return context.row_count

    def run(self, sql, stream=None, types=None, **params):
        if len(params) == 0 and stream is None:
            self._context = self.execute_simple(sql)
        else:
            statement, make_vals = to_statement(sql)
            oids = () if types is None else make_vals(defaultdict(lambda: None, types))
            self._context = self.execute_unnamed(
                statement, make_vals(params), oids=oids, stream=stream
            )
        return self._context.rows

    def prepare(self, sql):
        return PreparedStatement(self, sql)


class PreparedStatement:
    def __init__(self, con, sql, types=None):
        self.con = con
        statement, self.make_vals = to_statement(sql)
        oids = () if types is None else self.make_vals(defaultdict(lambda: None, types))
        self.name_bin, self.cols, self.input_funcs = con.prepare_statement(
            statement, oids
        )

    @property
    def columns(self):
        return self._context.columns

    def run(self, stream=None, **params):
        params = make_params(self.con.py_types, self.make_vals(params))

        self._context = self.con.execute_named(
            self.name_bin, params, self.cols, self.input_funcs
        )

        return self._context.rows

    def close(self):
        self.con.close_prepared_statement(self.name_bin)


### pgconn.py ends here
