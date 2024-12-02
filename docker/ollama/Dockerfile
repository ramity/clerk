FROM ollama/ollama:0.1.43

WORKDIR /root/.ollama

# Get latest apt updates and upgrades
RUN apt update
RUN apt upgrade -y

# Start ollama serve and disown
RUN ollama serve & disown
RUN ollama pull qwen2.5-coder:3b

ENTRYPOINT sleep infinity
