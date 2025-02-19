# MThreeProject

### By Laura, Naomi, Sadika, Zainab


# 💻 How to use:

## How to run stress tests
- create a database on VM 2 called test
  - CREATE USER 'user'@'%' IDENTIFIED BY 'YourPassword';
- create a table called stress_table
  - CREATE TABLE stress_table ( id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), value INT );
- create a user with root privileges who can access the database from any machine
  - GRANT ALL PRIVILEGES ON databaseName.* TO 'user'@'%' WITH GRANT OPTION;
  - FLUSH PRIVILEGES;
- Install dependencies:
  - `pip install mysql-connector-python`
  - `yum install iperf3`
  - `yum install stress `
  - `yum install stress-ng`
- update details inside stresstest.py:
  - MYSQL_HOST should point to the IP address for your own VM2
- run `python stresstest.py`



# Our Steps:

## Part 1: Creating the machines

- Create 3 VMs - VM0, VM1, VM2
- Setup PLA from VM1 to both VM0 and VM2

## Part 2: Stress Testing

- In vm1
- Install stress-ng with ‘yum install stress-ng’
- Write a python script
- Yum install git
- Git clone https://github.com/laura-arch/MThreeProject.git
- Install iPerf with 'yum install iperf3'
- https://www.baeldung.com/linux/iperf-measure-network-performance


https://manpages.ubuntu.com/manpages/xenial/man1/stress-ng.1.html 

## Part 3 Stress test alerts: 
![image](https://github.com/user-attachments/assets/f20b82fa-2f94-439a-a7c2-df64dd390387)


## Part 5: Configuration Management using Ansible

- Yum install ansible

## Part 6: Containerising our Python script using Docker

# Install Docker
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo service docker start
```

# Install Kubernetes (Minikube)
```
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-arm64
sudo install minikube-linux-arm64 /usr/local/bin/minikube && rm minikube-linux-arm64
minikube start
```

# Clone Project
```
yum install git
git clone https://github.com/laura-arch/MThreeProject.git
```
# Build Dockerfile
Dockerfile
```
FROM redhat/ubi8:latest

COPY . .

RUN dnf update -y
RUN dnf install -y python3.12 python3-pip
# RUN dnf install -y iperf3
# RUN dnf install -y stress-ng 
RUN pip3 install mysql-connector-python

CMD ["python3", "stresstest.py"]
```

Build
```
docker login
docker build . -t lauraarch/stresstest:latest
docker push lauraarch/stresstest:latest
```

# Run in Kubernetes
stresstest-manifest.yaml
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stresstest-dp
  labels:
    app: stresstest
spec:
  replicas: 3
  selector:
    matchLabels:
      app: stresstest
  template:
    metadata:
      labels:
        app: stresstest
    spec:
      containers:
      - name: stresstest
        image: lauraarch/stresstest:latest
        imagePullPolicy: Always
```

```
minikube kubectl -- apply -f stresstest-manifest.yaml
```

# Shell into pod
```
minikube kubectl -- get pods
```


```
minikube kubectl -- exec -it stresstest-dp-xyz -- /bin/bash
```
