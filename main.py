import quart
import quart_cors
from quart import request, Response, send_from_directory
import requests
from balance.evm import getBalanceWrapper
from layer0 import queryTop10Users4layer0
from util.logger import getLogger

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

logger = getLogger()

# 设置静态文件目录
app.static_folder = 'static'


# 路由处理函数，发送静态 HTML 文件
@app.route('/static/<path:filename>')
async def serve_html(filename):
    return await send_from_directory(app.static_folder, filename)


@app.route("/api/getBalance", methods=['GET'])
async def get_balance():
    """
    根据address返回各Evm链的余额
    """
    address = request.args.get('address')
    try:
        result = getBalanceWrapper(address)
        return Response(response=result, status=200)
    except requests.exceptions.RequestException as e:
        error_message = f'Error fetching data from API: {e}'
        logger.error(error_message)
        return Response(response=error_message, status=500)


@app.route("/api/getTopNUsersForLayer0")
async def get_top_n_users_for_layer0():
    """
    查询layer0排名前top_num的用户信息
    """
    top_num = request.args.get("top_num")
    try:
        result = queryTop10Users4layer0(top_num)
        return Response(response=result, status=200)
    except requests.exceptions.RequestException as e:
        error_message = f'Error fetching data from API: {e}'
        logger.error(error_message)
        return Response(response=error_message, status=500)


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5003)


if __name__ == "__main__":
    main()
