FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /flask_dash_plotly_website
COPY requirements.txt /flask_dash_plotly_website/
RUN pip install -r requirements.txt
COPY . /flask_dash_plotly_website/