from web3 import Web3
from config import readConfig
from datetime import datetime
import os
from balance.evm import getBalanceWrapper

config = readConfig()


def getCurrentDateYYYYMMDD():
    current_time = datetime.now()
    return current_time.strftime("%Y-%m-%d")


if __name__ == "__main__":
    # wei_amount = 1000000000000000;
    # ether = Web3.from_wei(wei_amount, 'ether')
    # print(ether)
    # a = 1 == '1'
    # print(type(a))
    # print(True)
    # if 1 == '1':
    #     print('true')
    # else:
    #     print('false')
    # print(config['dune_data_cache_path'])
    # print(getCurrentDateYYYYMMDD())
    # cache_file = config['dune_data_cache_path'] + getCurrentDateYYYYMMDD() + '_' + str(10)
    # print(cache_file)
    # if os.path.exists(cache_file):
    #     print('文件存在')
    # else:
    #     print('文件不存在')
    address = '0xe93685f3bba03016f02bd1828badd6195988d950'
    result = getBalanceWrapper(address)
    print(result)
