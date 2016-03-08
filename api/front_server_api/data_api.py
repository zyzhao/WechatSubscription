from api.front_server_api.api_functions import *
from api.front_server_api.api_share_function import response_json
from api import *

@flask_app.route("/wechat/datajs/article_list")
@response_json
def api_article_summary_list():
    """

    :return:
    """
    page_num = request.args.get("page_num", 1)
    page_num = int(page_num)
    return article_summary_list(pn=page_num)


@flask_app.route("/wechat/datajs/account_list")
@response_json
def api_account_list():
    """

    :return:
    """

    return account_list()











