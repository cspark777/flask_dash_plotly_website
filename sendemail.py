import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from dash.dependencies import Input, Output, State
import mysql.connector
from mysql.connector import errorcode
from flask import Flask
from flask_mail import Message, Mail
import json
import settings
import base64
import argparse

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))
static_path = basedir + "/source/static/"
app = Flask(__name__, static_folder=static_path)

app.config['MAIL_SERVER']=settings.MAIL_SERVER
app.config['MAIL_PORT'] = settings.MAIL_PORT
app.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = settings.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = settings.MAIL_USE_SSL

mail = Mail(app)

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def log_message(log_file, message):    
    hs = open(log_file,"a", encoding="utf8")
    hs.write(message + "\n")
    hs.close() 

def read_message(log_file):    
    hs = open(log_file,"r", encoding="utf8")
    a = hs.read()
    hs.close() 
    return a

# Load test data from json
def get_strategy1(bot_id):
    a = read_message("data/stratgy.txt")
    myresult = json.loads(a)
    strategies = pd.DataFrame(myresult)

    return strategies

def get_data1(strategy):

    a = read_message("data/data.txt")
    myresult = json.loads(a)

    b = read_message("data/col.txt")
    cols = json.loads(b)


    col3 = [column[0] for column in cols]
    strategies = pd.DataFrame(myresult, columns=col3)
    return strategies

def get_main_table1():
    a = read_message("data/table.txt")
    myresult = json.loads(a)
    table = pd.DataFrame(myresult)

    return table

# Load data
def get_data_from_db(sql):     
    print(sql)   
    mydb = mysql.connector.connect(
        host=settings.MYSQL_HOST,
        user=settings.MYSQL_USER,
        passwd=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DATABASE
    )
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    print("---")
    return myresult

def get_strategy(bot_id):
    if settings.USE_DATABASE:
        select_sql = "select strategy,minutes from bot_strategy where bot_id = " + str(bot_id)
        myresult = get_data_from_db(select_sql)
        strategies = pd.DataFrame(myresult)
    else:
        strategies = get_strategy1(bot_id)

    return strategies

def get_data(strategy):
    if settings.USE_DATABASE:
        select_sql = "select * from action_log where bot_id = " + str(strategy)     
        myresult = get_data_from_db(select_sql)

        col_sql = "SHOW columns FROM action_log"
        cols = get_data_from_db(col_sql);
        col3 = [column[0] for column in cols]
        strategies = pd.DataFrame(myresult, columns=col3)   
    else:
        strategies = get_data1(strategy)
    return strategies

def get_main_table():   
    
    if settings.USE_DATABASE == True: 
        select_sql = "SELECT bot_id , strategy ,minutes , DATE_FORMAT(bot_start_run, '%Y-%m-%d %h:%i:%s') AS bot_start_run , wallet_last , wallet_start , price_end ,price_start, DATEDIFF(NOW() , bot_start_run ) AS time_run , wallet_last/wallet_start AS change_in_per FROM ruuning_wallets_vm ORDER BY wallet_last DESC"

        myresult = get_data_from_db(select_sql)

        print(len(myresult))

        #table_str = json.dumps(myresult)
        #log_message("data/table.txt", table_str)

        table = pd.DataFrame(myresult)  
    else:
        
        table = get_main_table1()
    return table




#get db data
#get_table()
#exit()

#--------------- global functions --------------

def get_graph(bot_id):
    data = get_data(bot_id)
    strategy = get_strategy(bot_id)
    print("get_graph, bot_id={}, data length={}".format(bot_id, len(data)))
    if len(data) == 0:
        return False

    data['predict_p6'] = data['predict_price'].shift(360)
    data['wallet'] = data['cash'] + data['amount'] * data['current_price']
    data['datetime'] = pd.to_datetime(data['rest_prediction_time'],unit='s')
    data = data.set_index('datetime')
    data['buy'] = data['current_price'].loc[data['action_1'] == 1] 
    data['sell'] = data['current_price'].loc[data['action_1'] == 3] 
    data = data.sort_values(by = 'rest_prediction_time')

    trace1 = []    
    df_sub = data

    trace1.append(go.Scatter(x = data.index,y=data['wallet'],mode='lines',name='WALLET', yaxis='y1'))
    trace1.append(go.Scatter(x = data.index,y=data['current_price'],mode='lines',name='PRICE', yaxis='y2'))
    trace1.append(go.Scatter(x = data.index,y=data['predict_price'],mode='lines',name='PREDICTED PRICE', yaxis='y2'))
    trace1.append(go.Scatter(x = data.index,y=data['predict_p6'],mode='lines',name='predict_p6', yaxis='y2'))

    trace1.append(go.Scatter(x = data.index,y=data['buy'],mode ='markers', marker=dict(color='LightSkyBlue',size=20),name='BUY', yaxis='y2'))
    trace1.append(go.Scatter(x = data.index,y=data['sell'],mode ='markers', marker=dict(color='red',size=20),name='SELL', yaxis='y2'))

    traces = [trace1]
    data = [val for sublist in traces for val in sublist]

    figure = {'data': data,
        'layout': go.Layout(
            colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
            template='plotly_dark',
            #paper_bgcolor='rgba(0, 0, 0, 0)',
            #plot_bgcolor='rgba(0, 0, 0, 0)',
            margin={'b': 15},
            hovermode='x',
            autosize=True,
            title={'text': "STRATEGY = " + str(strategy[0].iloc[0]) + " TIMEINTERVAL = " + str(strategy[1].iloc[0]), 'font': {'color': 'white'}, 'x': 0.1},
            xaxis=dict(range=[df_sub.index.min(), df_sub.index.max()]),
            yaxis=dict(range=[int(df_sub['wallet'].min()), int(df_sub['wallet'].max())], side='left', overlaying='y2'),
            yaxis2=dict(range=[int(df_sub['current_price'].min()), int(df_sub['current_price'].max())], side='right'),
            height=1200
        ),
    }    
    return figure

def get_all_bot():
    table = get_main_table()
    print("--------------")
    print(table[0])
    return table[0]

def get_image_chart(bot_id):
    path = static_path + "images/chart/{}.jpeg".format(bot_id)
    figure = get_graph(bot_id)
    if figure is False:
        return
    pio.write_image(figure, path)


def send_email(email_addr):
    template_path = static_path + "email_template/maintable.html"
    template_content = read_message(template_path)

    table_url = settings.BASE_URL + "/wallet_status/maintable"

    image_path = static_path + "images/chart/"

    table_content = ""
    chart_content = ""
    table = get_main_table().values

    index = 0
    for row in table:
        index = index + 1
        tr = "<tr>"
        tr = tr + "<td>{}</td>".format(index)
        tr = tr + "<td>{}</td>".format(row[0])
        tr = tr + "<td>{}</td>".format(row[1])
        tr = tr + "<td>{}</td>".format(row[2])
        tr = tr + "<td>{}</td>".format(row[3])
        tr = tr + "<td>{}</td>".format(row[4])
        tr = tr + "<td>{}</td>".format(row[5])
        tr = tr + "<td>{}</td>".format(row[6])
        tr = tr + "<td>{}</td>".format(row[7])
        tr = tr + "<td>{}</td>".format(row[8])
        tr = tr + "<td>{}</td>".format(row[9])        
        tr = tr + "</tr>"
        table_content = table_content + tr

        bot_id = row[0]
        
        chart_url = settings.BASE_URL + "/wallet_status/?bot_id=" + str(bot_id)
        #chart_image_url = settings.BASE_URL + "/images/chart/{}.jpeg".format(bot_id)
        #chart_image_path = static_path + "/images/chart/{}.jpeg".format(bot_id)
        #chart_img_base64 = get_base64_encoded_image(chart_image_path)
        
        chart_div = '<div class="chart"><a href="' + chart_url + '"><img src="cid:' + str(bot_id) + '" width="450" height="300" style="display: block;" ></a></div>'
        chart_content = chart_content + chart_div

    template_content = template_content.replace("{{table_url}}", table_url)
    template_content = template_content.replace("{{table_content}}", table_content)
    template_content = template_content.replace("{{chart_content}}", chart_content)



    '''
    msg = Message('Hello', sender = settings.MAIL_SENDER, recipients = [email_addr])
    msg.html = template_content
    mail.send(msg)

    '''

    smtp_server = settings.MAIL_SERVER
    port = settings.MAIL_PORT  # For starttls
    sender_email = settings.MAIL_SENDER
    password = settings.MAIL_PASSWORD

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        message = MIMEMultipart("alternative")
        message["Subject"] = "test"
        message["From"] = sender_email
        message["To"] = email_addr

        part = MIMEText(template_content, "html")
        message.attach(part)

        for row in table:
            bot_id = row[0]
            chart_image_path = static_path + "/images/chart/{}.jpeg".format(bot_id)
            my_file = Path(chart_image_path)
            if not my_file.is_file():
                res = get_image_chart(bot_id)
                if not res:
                    chart_image_path = static_path + "/images/chart/none.jpeg"

            with open(chart_image_path, 'rb') as f:
                msg_image = MIMEImage(f.read())
                msg_image.add_header('Content-ID', '<{0}>'.format(bot_id))
                message.attach(msg_image)

        server.sendmail(
            sender_email, email_addr, message.as_string()
        )

    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 
    return "ok"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--email", type=str, help="email address", required=True)
    args = vars(ap.parse_args())
    
    email = args["email"]
    res = send_email(email)

    print(res)

if __name__ == '__main__':
    main()