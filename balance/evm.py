import json
import requests
from web3 import Web3
from concurrent.futures import ThreadPoolExecutor
import time
from util.logger import getLogger

eth_url = "https://mainnet.infura.io/v3/e8649d0c19c04643a1d5a1c55a32d565"
bnb_url = "https://bsc-dataseed3.ninicoin.io"
ht_url = "https://http-mainnet.hecochain.com"
matic_url = "https://polygon-rpc.com"
eth_arbi_url = "https://arb1.arbitrum.io/rpc"
avax_url = "https://api.avax.network/ext/bc/C/rpc"
lat_url = "https://openapi.platon.network/rpc"
etc_url = "https://etc.getblock.io/mainnet/?api_key=17069f81-530f-4e6a-9fab-f08e53d47d09"
ethf_url = "https://rpc.etherfair.org"
ethw_url = "https://mainnet.ethereumpow.org"

logger = getLogger()


def getEvmBalance(param):
    start_time = time.time()  # 记录开始时间
    data = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [
            param['address'],
            "latest"
        ],
        "id": 1
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(param['url'], headers=headers, data=json.dumps(data))
        resultJson = json.loads(response.text)
        result = resultJson['result']
        valueStr = result[2:]
        wei_amount = int(valueStr, 16)
        amount = Web3.from_wei(wei_amount, 'ether')
        return {param['symbol']: str(amount)}
    except requests.exceptions.RequestException as e:
        error_message = f'Error fetching data from API: {e}'
        logger.error(error_message)
        return 0
    finally:
        end_time = time.time()  # 记录结束时间
        execution_time = end_time - start_time  # 计算方法执行时间
        logger.info(f"【{param['symbol']}】请求时间：{execution_time} 秒")


def getBalanceWrapper(address):
    """
    根据address返回各Evm链的余额
    :param address:地址
    :return:各Evm链address余额
    """
    start_time = time.time()  # 记录开始时间
    params = [
        {'url': eth_url, 'symbol': 'eth', 'address': address},
        {'url': bnb_url, 'symbol': 'bnb', 'address': address},
        {'url': ht_url, 'symbol': 'ht', 'address': address},
        {'url': ethf_url, 'symbol': 'ethf', 'address': address},
        {'url': ethw_url, 'symbol': 'ethw', 'address': address},
        {'url': eth_arbi_url, 'symbol': 'arbi', 'address': address},
        {'url': avax_url, 'symbol': 'avax', 'address': address},
        {'url': lat_url, 'symbol': 'lat', 'address': address},
        {'url': etc_url, 'symbol': 'etc', 'address': address},
        {'url': matic_url, 'symbol': 'matic', 'address': address}
    ]
    with ThreadPoolExecutor() as executor:
        # 提交任务给线程池，并获取结果（按提交顺序）
        results = list(executor.map(getEvmBalance, params))
        resultDict = {}
        # 处理结果
        for result in results:
            resultDict.update(result)
    jsonStr = json.dumps(resultDict)
    logger.info(jsonStr)
    end_time = time.time()  # 记录结束时间
    execution_time = end_time - start_time  # 计算方法执行时间
    logger.info(f"方法执行时间：{execution_time} 秒")
    return jsonStr
