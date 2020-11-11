# backend/views.py

from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from source.backend.forms import BackendForm
from source.util.chart import *

backend = Blueprint('backend', __name__)

# dashboard
@backend.route('/backend', methods=['GET', 'POST'])
def backend_dashboard():      
    return render_template('/backend/dashboard.html')
   
# get chart images for all bot
@backend.route('/backend/get_images_chart', methods=['GET', 'POST'])
def get_images_chart(): 
    if request.method == "POST":
        bot_arr = get_all_bot()

        for bot_id in bot_arr:
            get_image_chart(bot_id)
        return "ok"

    else:    
        return render_template('/backend/get_images_chart.html')

# send email
@backend.route('/backend/sendemail', methods=['GET', 'POST'])
def sendemail(): 
    if request.method == "POST":
        email = request.form.get('email');
        res = send_email(email)

        return render_template('/backend/sendemail.html', msg="Email sent !!!")
    else:    
        return render_template('/backend/sendemail.html', msg="")