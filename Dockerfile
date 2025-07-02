FROM jenkins/jenkins:lts

USER root

# Install Python and system packages needed to build mysqlclient
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    pkg-config default-libmysqlclient-dev build-essential

# Create a virtual environment and install pytest
RUN python3 -m venv /opt/jenkins-venv \
  && /opt/jenkins-venv/bin/pip install --upgrade pip \
  && /opt/jenkins-venv/bin/pip install pytest

ENV PATH="/opt/jenkins-venv/bin:$PATH"

USER jenkins
