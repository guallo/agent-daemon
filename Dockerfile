FROM ubuntu
RUN apt-get update

RUN apt-get install -y git python3 python3-pip

RUN git clone https://github.com/guallo/agent-daemon.git /opt/agent-daemon
WORKDIR /opt/agent-daemon

RUN pip3 install -r requirements
RUN chmod a+x agent.py

ENTRYPOINT ["/opt/agent-daemon/agent.py"]
