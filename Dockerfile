FROM python:3.9

# working directory
# WORKDIR /app/faust

# copy requirements
COPY requirements.txt requirements.txt

# install requirements
RUN pip3 install -r requirements.txt

# copy all files to the container
COPY .  .

# run the command
CMD ["python","-u", "producer.py", "&", "faust", "-A", "faust_worker", "worker", "-l", "info"] 

