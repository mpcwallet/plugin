import json

import dotenv
from dune_client.client import DuneClient
from dune_client.query import Query
from dune_client.types import QueryParameter
from datetime import datetime
from config import DUNE_API_KEY,DUNE_DATA_CACHE_PATH
import os
import pandas as pd
from util.logger import getLogger

DUNE_API_KEY = DUNE_API_KEY
DUNE_DATA_CACHE_PATH = DUNE_DATA_CACHE_PATH

logger = getLogger()


# 下划线转换为驼峰形式
def underscore_to_camel(key):
    parts = key.split('_')
    return parts[0] + ''.join(x.title() for x in parts[1:])


# 转换JSON中的键
def convert_keys(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = underscore_to_camel(key)
            new_value = convert_keys(value)
            new_data[new_key] = new_value
        return new_data
    elif isinstance(data, list):
        return [convert_keys(item) for item in data]
    else:
        return data


def getCurrentDateYYYYMMDD():
    current_time = datetime.now()
    return current_time.strftime("%Y-%m-%d")


def readFromCache(cache_file):
    df = pd.read_csv(cache_file)
    # 转换键
    converted_data = convert_keys(df.to_dict(orient='records'))
    # 转换后的JSON字符串
    converted_json_str = json.dumps(converted_data, indent=4)
    logger.info(converted_json_str)
    return converted_json_str


def readFromDune(top_num):
    query = Query(
        # name="查询layer0排名前n的用户信息",
        name="查询layer0排名前n的用户信息",
        query_id=2671528,
        params=[
            # QueryParameter.text_type(name="TextField", value="Word"),
            # QueryParameter.number_type(name="NumberField", value=3.1415926535),
            # QueryParameter.date_type(name="DateField", value="2022-05-04 00:00:00"),
            # QueryParameter.enum_type(name="ListField", value="Option 1"),
            QueryParameter.number_type(name="top_num", value=top_num)
        ],
    )
    logger.info("Results available at {}", query.url())

    dotenv.load_dotenv()
    dune = DuneClient(DUNE_API_KEY)
    df = dune.refresh_into_dataframe(query)
    if not os.path.exists(DUNE_DATA_CACHE_PATH):
        os.makedirs(DUNE_DATA_CACHE_PATH)
    cache_file = DUNE_DATA_CACHE_PATH + getCurrentDateYYYYMMDD() + '_' + str(top_num) + '.csv'
    df.to_csv(cache_file, index=False)
    # 转换键
    converted_data = convert_keys(df.to_dict(orient='records'))
    # 转换后的JSON字符串
    converted_json_str = json.dumps(converted_data, indent=4)
    logger.info(converted_json_str)
    return converted_json_str


def queryTop10Users4layer0(top_num):
    cache_file = DUNE_DATA_CACHE_PATH + getCurrentDateYYYYMMDD() + '_' + str(top_num) + '.csv'
    if os.path.exists(cache_file):
        return readFromCache(cache_file)
    else:
        return readFromDune(top_num)


if __name__ == '__main__':
    # queryTop10Users4layer0(10)
    readFromDune(10)
