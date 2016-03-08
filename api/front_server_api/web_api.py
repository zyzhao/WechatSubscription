from api import flask_app, render_template, request
from api.front_server_api.api_functions import *
from api import *

@flask_app.route("/wechat/article_list")
def page_article_summary_list():
    """

    :return:
    """

    return render_template("sub_articles_summary.html")

@flask_app.route("/wechat/account_list")
def page_account_summary_list():
    """

    :return:
    """

    return render_template("sub_account_list.html")

@flask_app.route("/wechat/account_list/add")
def page_add_account():
    """

    :return:
    """
    query = request.args.get("query", "")
    keywords = query.split(",")
    if keywords:
        add_account(keywords)

    return render_template("sub_account_list.html")














