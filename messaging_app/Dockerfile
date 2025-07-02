FROM jenkins/jenkins:lts

USER root

# Install Python and system packages needed to build mysqlclient
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    pkg-config default-libmysqlclient-dev build-essential \
    apt-transport-https ca-certificates curl gnupg lsb-release

# Install Docker
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update && apt-get install -y docker-ce-cli

# Create a virtual environment and install pytest
RUN python3 -m venv /opt/jenkins-venv \
  && /opt/jenkins-venv/bin/pip install --upgrade pip \
  && /opt/jenkins-venv/bin/pip install pytest \
  && chown -R jenkins:jenkins /opt/jenkins-venv

# Create docker group and add jenkins user to docker group
RUN groupadd docker && usermod -aG docker jenkins

ENV PATH="/opt/jenkins-venv/bin:$PATH"

USER jenkins