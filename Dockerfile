
FROM redhat/ubi8:latest

COPY . .

RUN dnf update -y
RUN dnf install -y python3.12 python3-pip
# RUN dnf install -y iperf3
# RUN dnf install -y stress-ng 
RUN pip3 install mysql-connector-python

CMD ["python3", "stresstest.py"]
