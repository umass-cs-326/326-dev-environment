# Use Gradescope's official autograder base image
ARG BASE_REPO=gradescope/autograder-base
ARG TAG=latest

FROM ${BASE_REPO}:${TAG}

# Install PostgreSQL and Python dependencies
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy requirements file
COPY requirements.txt /autograder/source/requirements.txt

# Install Python packages from requirements.txt
RUN pip3 install --no-cache-dir -r /autograder/source/requirements.txt

# Set up PostgreSQL
USER postgres

# Initialize PostgreSQL database cluster and create database
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER app WITH SUPERUSER PASSWORD 'app';" && \
    createdb -O app db && \
    /etc/init.d/postgresql stop

# Configure PostgreSQL to accept connections
RUN echo "host all all 127.0.0.1/32 md5" >> /etc/postgresql/14/main/pg_hba.conf && \
    echo "listen_addresses='localhost'" >> /etc/postgresql/14/main/postgresql.conf

USER root

# Copy autograder source files to /autograder/source
COPY run_tests.py /autograder/source/
COPY start_postgres.sh /autograder/source/
COPY run_autograder /autograder/run_autograder

RUN chmod +x /autograder/run_autograder \
    /autograder/source/start_postgres.sh

# Ensure that scripts are Unix-friendly and executable
RUN dos2unix /autograder/run_autograder

# Set environment variable for database connection
ENV DATABASE_URL="postgresql+psycopg://app:app@localhost:5432/db"