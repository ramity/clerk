FROM ollama/ollama:0.1.43

WORKDIR /root/.ollama

# Get latest apt updates and upgrades
RUN apt update
RUN apt upgrade -y

ADD docker/ollama/init.bash /tmp/init.bash
ENTRYPOINT /tmp/init.bash
