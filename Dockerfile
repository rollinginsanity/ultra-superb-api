FROM python:3.6
RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/rollinginsanity/ultra-superb-api.git /api/
WORKDIR /api/
RUN pip3 install -r /api/docker_requirements.txt
RUN pip3 install flask-jsontools
RUN mkdir -p /api/logs
RUN ["python", "create_db.py"]

EXPOSE 5000

CMD ["python", "start.py"]
