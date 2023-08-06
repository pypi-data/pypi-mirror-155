import json

HEADER_PROTOCOL = []
MESSAGE_PROTOCOL = []
DETAILLIST_PROTOCOL = []
PROTOCOL_MAP = {}


def set_var(headers, protocol: str):
    """设置全局变量"""
    global HEADER_PROTOCOL
    global MESSAGE_PROTOCOL
    global DETAILLIST_PROTOCOL
    global PROTOCOL_MAP

    temp_var = {}
    if protocol == 'HEADER_PROTOCOL':
        key = list(headers.keys())[0]
        ingeter = int(hex(ord(key)), base=16)
        HEADER_PROTOCOL.append(key)
        HEADER_PROTOCOL.append(ingeter)
        for index, value in enumerate(headers[key]):
            temp_var[bytes.fromhex(f"000{index+1}")] = value
        PROTOCOL_MAP[(key, ingeter)] = {
            "reverse": {
                v: k for k, v in temp_var.items()
            },
            "fields": temp_var
        }
    elif protocol == 'MESSAGE_PROTOCOL':
        key = headers
        ingeter = int(hex(ord(key)), base=16)
        MESSAGE_PROTOCOL.append(key)
        MESSAGE_PROTOCOL.append(ingeter)
    elif protocol == 'DETAILLIST_PROTOCOL':
        key = list(headers.keys())[0]
        ingeter = int(hex(ord(key)), base=16)
        DETAILLIST_PROTOCOL.append(key)
        DETAILLIST_PROTOCOL.append(ingeter)
        for index, value in enumerate(headers[key]):
            temp_var[bytes.fromhex(f"000{index+1}")] = value
        PROTOCOL_MAP[(key, ingeter)] = {
            "reverse": {
                v: k for k, v in temp_var.items()
            },
            "fields": temp_var
        }
    else:
        raise Exception("Unsupported protocol")


def read_config(file_path: str):
    '''读取配置文件'''
    with open(file_path, 'r', encoding='utf-8') as f:
        if file_path.split('.')[-1] == 'json':
            config = json.loads(f.read())
        else:
            raise Exception("Unsupported file format")
    for i in config:
        for headers in config[i]:
            set_var(headers, i)
