FROM python:3.9-slim

ENV PATH="/scripts:${PATH}"

COPY real_requirements.txt /real_requirements.txt

RUN apt-get update
RUN apt-get install -y gcc 
RUN pip install -r real_requirements.txt


RUN mkdir /app
COPY ./app /app
WORKDIR /app
COPY ./scripts /scripts

#add executable permission to scripts
RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

#Creates new user in image, otherwise it will run as root user, security improvement
RUN adduser user
RUN chown -R user:user /vol
# grant user full access, everyone else only has read
RUN chmod -R 755 /vol/web 
# switch to user account
USER user

#This will start our app
CMD ["entrypoint.sh"]

