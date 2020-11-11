1. Server information
SSH : Main IP Address: 198.38.89.14, port 2222, user : root, password : vzmj230312

2. MySQL database
IP: 127.0.0.1, Port: 3306, user: root, password: "", database name : jmzv13_twitter

3: source directory on server
/home/geo_flask/geointelligence_flask#

4: Project structure
This project is consist of two part.
First is a backend service to get twitts and analyze it for positive, neutral, negative
Second is a flask website to show the data.

4-1: Backend Service
scraing.py is just for this service.
To regist it as daemon, please do as follow:

	cd /etc/systemd/system
	sudo nano scraping.service

and edit the file with following:

	[Unit]
	Description=Scraping

	[Service]
	User=root
	ExecStart=/usr/bin/python3 /home/geo_flask/geointelligence_flask/scraping.py

	[Install]
	WantedBy=multi-user.target

and save this file.
and please do to start this service

	sudo systemctl daemon-reload
	sudo systemctl start scraping.service
	sudo systemctl enable scraping.service

4-2 : Flask website
to run the website, please use following command in terminal.
	python app.py

5: Web site code structure
main page code are in /source/core/view.py
Home page has a real time graph, it is using Chart.js.
realtime graph data will be gotten via ajax function.
ajax url is "/get_chart1_data"

