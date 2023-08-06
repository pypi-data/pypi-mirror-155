import sys
import logging
from typing import Dict
from configs import const


HEADER_PROTOCOL = const.HEADER_PROTOCOL
MESSAGE_PROTOCOL = const.MESSAGE_PROTOCOL
DETAILLIST_PROTOCOL = const.DETAILLIST_PROTOCOL
PROTOCOL_MAP = const.PROTOCOL_MAP


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s]: %(filename)s - %(funcName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def read_int32(buf):
    return int.from_bytes(buf, sys.byteorder)


def int_to_int32(i: int):
    """将数字转为4字节的字节流"""
    return i.to_bytes(4, sys.byteorder)


def int_to_int16(i: int):
    """将数字转为2字节的字节流"""
    return i.to_bytes(2, sys.byteorder)


def judge_data_format(mtype, data):
    SUM_PROTOCOL = MESSAGE_PROTOCOL + HEADER_PROTOCOL + DETAILLIST_PROTOCOL
    if mtype not in SUM_PROTOCOL:
        logger.error(f"Unknown meta type: {mtype}")
        raise ValueError(f"Unknown meta type: {mtype}")
    elif mtype in MESSAGE_PROTOCOL and not isinstance(data, str):
        logger.error("Message Protocol data must be a string")
        raise ValueError("Message Protocol data must be a string")
    elif mtype in HEADER_PROTOCOL and not isinstance(data, dict):
        logger.error("Header Protocol data must be a dict")
        raise ValueError("Header Protocol data must be a dict")
    elif mtype in DETAILLIST_PROTOCOL and not isinstance(data, list):
        logger.error("DetailList Protocol data must be a list")
        raise ValueError("DetailList Protocol data must be a list")
    else:
        pass


def get_filed_map(mtype, reverse: bool) -> Dict[str, str]:
    '''获取字段映射表'''
    for t, v in PROTOCOL_MAP.items():
        if mtype in t:
            if reverse:
                return v["reverse"]
            return v["fields"]
    logger.error(f"Unknown meta type: {mtype}")
    raise ValueError("Unknown meta type: {}".format(mtype))


def _to_filed_protocol(mtype: str, d: Dict[str, str]) -> bytes:
    '''filed protocol'''
    buf = b""
    field_map = get_filed_map(mtype, False)
    reversed_field_map = get_filed_map(mtype, True)
    for index, key in field_map.items():
        if key not in reversed_field_map:
            continue
        vlen = int_to_int32(len(d[key].encode("utf8")))
        buf += index + vlen + d[key].encode("utf8")
    return buf


def resolve_field_protocol(mtype, num_fields, buf: bytes) -> Dict[str, str]:
    """解析field protocol"""
    ptr = 0
    buf_len = len(buf)
    field_map = get_filed_map(mtype, False)
    result = {}
    while num_fields and ptr < buf_len:
        key = buf[ptr: ptr + 2]
        if key not in field_map:
            logger.error(f"Unknown field: {key}")
            raise ValueError(f"Unsupported field: {key}")
        vlen = read_int32(buf[ptr + 2: ptr + 6])
        value = buf[ptr + 6: vlen + ptr + 6]
        result[field_map[key]] = value.decode("utf8")
        ptr += vlen + 6
        num_fields -= 1

    if ptr != buf_len or num_fields != 0:
        logger.error("Bad message")
        raise ValueError("Bad message")
    return result

# ------------------message protocol------------------


def to_msg_protocol(mtype: str, body: str) -> bytes:
    '''message protocol'''
    mtype = mtype.encode("utf8")
    mlen = int_to_int32(len(body.encode("utf8")))
    body = body.encode("utf8")
    return mtype + mlen + body


def resolve_msg_protocol(buf: bytes) -> str:
    '''解析message protocol'''
    str_len = read_int32(buf[1:5])
    return buf[5: 5+str_len].decode("utf-8")


# ------------------header protocol------------------


def to_header_protocol(mtype: str, d: Dict[str, str]):
    '''header protocol'''
    _mtype = mtype.encode("utf8")
    buf_fields = _to_filed_protocol(mtype, d)
    mlen = int_to_int32(len(buf_fields))
    num_fields = int_to_int32(len(d))
    return _mtype + mlen + num_fields + buf_fields


def resolve_header_protocol(buf: bytes) -> Dict[str, str]:
    '''解析header protocol'''
    ptr = 0
    buf_len = len(buf)

    mtype = buf[ptr]
    num_fields = read_int32(buf[5: 9])

    field_buf = buf[9: buf_len]
    result = resolve_field_protocol(mtype, num_fields, field_buf)

    return result

# ------------------DetailList protocol------------------


def to_detaillist_protocol(mtype: str, value_list: list) -> bytes:
    '''detaillist protocol'''
    _mtype = mtype.encode("utf8")
    num_elements = int_to_int32(len(value_list))
    detail_buf = b""
    for index, value in enumerate(value_list):
        detail_buf += _to_detail_protocol(mtype, index, value)
    mlen = int_to_int32(len(detail_buf))
    return _mtype + mlen + num_elements + detail_buf


def _to_detail_protocol(mtype, index, d: Dict[str, str]) -> bytes:
    index_buf = int_to_int32(index)
    num_fields = int_to_int32(len(d))
    buf_fields = _to_filed_protocol(mtype, d)
    return index_buf + num_fields + buf_fields


def resolve_detaillist_protocol(buf: bytes) -> list:
    ptr = 0
    field_map = get_filed_map(buf[ptr], False)
    mlen = read_int32(buf[ptr + 1: ptr + 5])
    num_elements = read_int32(buf[5: 9])
    detail_buf = buf[9: mlen + 9]
    field_buf = detail_buf[8: mlen + 9]
    for _ in range(num_elements):
        result = {}
        num_fields = read_int32(detail_buf[4:8])
        while num_fields:
            key = field_buf[ptr: ptr + 2]
            if key not in field_map:
                logger.error(f"Unknown field: {key}")
                raise ValueError(f"Unsupported field: {key}")
            vlen = read_int32(field_buf[ptr + 2: ptr + 6])
            value = field_buf[ptr + 6: vlen + ptr + 6]
            result[field_map[key]] = value.decode("utf8")
            ptr += vlen + 6
            num_fields -= 1
        ptr += 8
        yield result

        if num_fields != 0:
            logger.error("Bad message")
            raise ValueError("Bad message")
