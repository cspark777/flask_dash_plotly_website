# core/views.py

from flask_dance.contrib.google import make_google_blueprint, google
from flask import render_template, request, Blueprint, redirect, url_for, jsonify
import random
from collections import deque
from datetime import datetime, timedelta
import time
import json
from source.util.chart import *

core = Blueprint('core', __name__)


@core.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@core.route('/wallet_status/maintable', methods=['GET'])
def maintable():
    table = get_main_table()    
    return render_template('maintable.html', table=table)

