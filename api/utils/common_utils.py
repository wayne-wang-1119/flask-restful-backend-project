import time
import re
import datetime
from bson.objectid import ObjectId
from functools import wraps

import logging

DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

DEFAULT_TIMESTAMP_FORMAT = "%Y%m%d%H%M%S"

logger = logging.getLogger(__name__)


def current_milli_time():
    return int(round(time.time() * 1000))


def get_datetime_with_milli_time(ms):
    return datetime.datetime.fromtimestamp(ms/1000.0)


def get_timestamp_from_date_str(date_str, format=DEFAULT_DATETIME_FORMAT):
    return int(datetime.datetime.strptime(date_str, format).timestamp()*1000)


def get_timestamp_with_format(format=DEFAULT_TIMESTAMP_FORMAT):
    return str(get_datetime_with_milli_time(current_milli_time()).strftime(format))


def get_date_with_format(ms=current_milli_time(), format=DEFAULT_DATETIME_FORMAT):
    return str(datetime.datetime.fromtimestamp(ms/1000.0).strftime(format))


def get_ignorecase_regex(in_str):
    return re.compile("^{}$".format(in_str), re.IGNORECASE)


def allowed_file(filename, allow_list):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allow_list


def parse_dict_key_to_lowercase(in_dict):
    if in_dict is None or len(in_dict) <= 0:
        return {}
    return {k.lower(): v for k, v in in_dict.items()}


def parse_dict_key_to_uppercase(in_dict):
    if in_dict is None or len(in_dict) <= 0:
        return {}
    return {k.upper(): v for k, v in in_dict.items()}


def json_converter(o):
    if isinstance(o, datetime.datetime) or isinstance(o, ObjectId):
        return o.__str__()


def str_to_bool(s):
    return (s if isinstance(s, bool) else (s.lower() in ["true"] if isinstance(s, str) else False)) if s is not None else False


def get_docker_ports_mappings(s):
    ports = {}
    if s is None:
        return {}
    ports_arr = s.split(",")
    if ports_arr is None or len(ports_arr) <= 0:
        return {}
    for p_str in ports_arr:
        if p_str is not None and p_str.strip() != "":
            if p_str.find(":") >= 0:
                p = p_str.split(":")[1].split("->")[0]
                d_p = p_str.split("->")[1].split("/")[0]
                ports[p] = d_p
            else:
                p = p_str.split("/")[0]
                ports[p] = p
    return ports


def measure_elapsed(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start_time = current_milli_time()
        ret = f(*args, **kwds)
        elapsed = current_milli_time()-start_time
        logger.info("The method[{}] elapsed {}ms".format(f.__name__, elapsed))
        return ret
    return wrapper


def verify_field_in_res(fields, res):
    return all([True if f in res else False for f in fields])


def helper(kvs, last_k, k, v):
    if type(v) is not dict:
        kvs.append(str(last_k)+"."+str(k)+"="+str(v))
        return
    for cur_k, cur_v in v.items():
        helper(kvs, str(last_k)+"."+str(k), cur_k, cur_v)


def convert_dict_kv_with_dot(data):
    kvs = []
    for k, v in data.items():
        helper(kvs, "", k, v)

    kvs = [kv[1:] for kv in kvs]
    return kvs


def extract_resp_msg(text):
    msg = ""
    i = 0
    for i in range(0, len(text)):
        if text[i] == "\"" and text[i + 1] == "T":
            break
    msg = text[i + 1:len(text) - 4]

    return msg
