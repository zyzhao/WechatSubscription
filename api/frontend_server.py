# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from api import flask_app, render_template, request
import math
from front_server_api.web_api import *
from front_server_api.data_api import *

import sys
sys.path.append("./")


@flask_app.route("/")
def server_index():
    server_info = "Hellow World!!!!!!!!"

    # return redirect(url_for("page_article_summary_list"))
    return render_template("page_not_found.html")


@flask_app.errorhandler(404)
def server_page_404(e):
    return render_template("page_not_found.html")


@flask_app.errorhandler(500)
def server_page_500(e):
    return render_template("internal_server_error.html")

if __name__ == '__main__':
    flask_app.run(host="0.0.0.0", port=8027, debug=True)