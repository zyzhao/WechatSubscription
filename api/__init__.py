# -*- coding: utf-8 -*-
from flask import Flask, request, Response, render_template, redirect, url_for, \
    request, jsonify, g, session, flash, send_from_directory, send_file
from flask_bootstrap import Bootstrap
from flask_bootstrap import StaticCDN

flask_app = Flask(__name__)
bootstrap = Bootstrap(flask_app)

flask_app.config.update(dict(
    CSRF_ENABLED=True,
    SECRET_KEY='RGVwbG95UGxhdGZvcm0='

))


flask_app.extensions['bootstrap']['cdns']['jquery'] = StaticCDN()
flask_app.extensions['bootstrap']['cdns']['bootstrap'] = StaticCDN()