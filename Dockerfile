# Pull base image
FROM python:3.11.3

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /inoa_challenge

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Install cron and supervisor
RUN apt-get update && apt-get install -y cron supervisor

# Copy project
COPY . /inoa_challenge

# Adding scripts to the Docker image
ADD https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh /usr/wait-for-it.sh

# Give execute permissions
RUN chmod +x /usr/wait-for-it.sh

# Copy your cron file to the cron.d directory
COPY cron_manager /etc/cron.d/cron_manager

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron_manager

# Create the log file to be able to run tail
RUN touch /var/log/cron.log