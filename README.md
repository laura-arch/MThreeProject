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

In vm1
- Install stress-ng with ‘yum install stress-ng’
- Write a python script
- Yum install git
- Git clone https://github.com/laura-arch/MThreeProject.git
- Install iPerf with 'yum install iperf3'
- https://www.baeldung.com/linux/iperf-measure-network-performance


https://manpages.ubuntu.com/manpages/xenial/man1/stress-ng.1.html 

## Part 3 Stress test alerts: 

![image](https://github.com/user-attachments/assets/f20b82fa-2f94-439a-a7c2-df64dd390387)

Example of alerts when running test:
Inactive: When no threshold has been exceeded

![image](https://github.com/user-attachments/assets/19254e0a-8dc0-44c7-aeb5-9fa50e4ba8cf)

Pending: When threshold has been exceeded

![image](https://github.com/user-attachments/assets/e3945aa7-9726-41af-9bab-100033034ec4)

Firing: When threshold has been exceeded over time limit set

![image](https://github.com/user-attachments/assets/21199740-8c48-4d1e-b884-bc4da9c9c680)


## Part 4 Jenkins Pipeline: 

Created Jenkins pipeline to automate building and deploying of script on github

![image](https://github.com/user-attachments/assets/31e84994-89c6-4bf3-8bba-511e4d72a595)


## Part 5: Configuration Management using Ansible

- Yum install ansible
- Created an inventory of the vms used
  
![image](https://github.com/user-attachments/assets/8fa72d08-a575-4800-8af7-a3794c99955f)

- Created playbooks: webservers.yaml & exporters.yaml
  
![image](https://github.com/user-attachments/assets/61e79481-a6ad-4929-abac-75fe49540e72) 

![image](https://github.com/user-attachments/assets/b074786a-ed5f-4d42-b14b-9e67eb928d88)

- Playbooks confirurations were consistent across the vms after deployment using
- ansible-playbook -i nodes webservers.yaml &
- ansible-playbook -i nodes exporters.yaml
-  Deployed to automate the installation of required software on the vms


## Part 6: Containerising our Python script using Docker

### Install Docker
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo service docker start
```

### Install Kubernetes (Minikube)
```
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-arm64
sudo install minikube-linux-arm64 /usr/local/bin/minikube && rm minikube-linux-arm64
minikube start
```

### Clone Project
```
yum install git
git clone https://github.com/laura-arch/MThreeProject.git
```
### Build Dockerfile
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

### Run in Kubernetes
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

### Shell into pod
```
minikube kubectl -- get pods
```


```
minikube kubectl -- exec -it stresstest-dp-xyz -- /bin/bash
```


## Part 7 Prometheus / Grafana with Node_exporter and Mysqld_exporter: 

### Installing and Configuring Exporters for Prometheus/Grafana
- install mysqld_exporter on VM1 in /usr/local/bin/ directory
- install node_exporter on VM1 in /usr/local/bin directory 
- run node_exporter (make sure you have execution rights)

Need to configure mysqld_exporter to link the database in VM2:
- nano /etc/.mysqld_exporter.cnf
  
Add the following to cnf file:
  - [client]
  - user=userName of database 
  - password=password of database
  - host=ip address of server that stores the database

Execution rights on file:
- chmod 600 /etc/.mysqld_exporter.cnf

Run the mysqld exporter with config file
- mysqld_exporter --config.my-cnf=/etc/.mysqld_exporter.cnf
- can create a systemd file instead of running mysqld_exporter with config file

### Setting Up Prometheus/Grafana
- Edit prometheus yaml file to add node_exporter IP address and port number and mysqld_exporter IP address and port number

![image](https://github.com/user-attachments/assets/32946f96-b974-451e-87d3-8fc8ace67d8f)

- Run Grafana on VM
- On Grafana, add data source with Prometheus IP address, add node_exporter and mysqld_exporter dashboard
  
node_exporter dashboard:

![image](https://github.com/user-attachments/assets/3797fb29-2d1d-48d7-897b-da2a45da0ff0)

mysqld_exporter dashbaord:

![image](https://github.com/user-attachments/assets/77812b1d-539e-4168-b66f-024f0c1ce740)


## Part 8: Email notifications when alerts are in firing state:
- Set up 2FA on gmail account
- Go to App Passwords to create an App Password - make sure to store the password on local device
Example:

![image](https://github.com/user-attachments/assets/d28e738d-16b4-4df1-bd83-8b963dbc2615)

### Set up alert configuration file
#### Used this link to help set up email notifications: https://signoz.io/guides/how-do-i-add-alerts-to-prometheus/
- create a config file in alert manager directory (make sure its a different filename to the other ones)
- paste this code in:

![image](https://github.com/user-attachments/assets/35ec804c-5ecb-4d01-809b-00c0f0584ecb)

- Paste and replace with your gmail account and App Password that you created earlier:

![image](https://github.com/user-attachments/assets/ae7fff11-9cb7-4c7c-974b-80e009f26729)

- Lastly run the alertmanager with config file
  - `./alertmanager --config.file=alertmanager.yml`

- Now you will receive an email when alert is in firing state:

title:

![image](https://github.com/user-attachments/assets/f4df3f4e-5af6-442f-902b-f26cc9b19dbb)

Content:

![image](https://github.com/user-attachments/assets/ef4bb95f-0c33-420e-a021-860bbf8e8627)


## Part 9: Log Analysis and Suggestions - Integration with WhatsApp:

### Dependencies to install:
- `pip install google google-generativeai`
- `pip install twilio`
- `pip install dotenv`
- `pip install --upgrade grpcio absl-py`

### SetUp
- Get API key at Google AI Studio
- Get Twilio API key and setup alerts to WhatsApp on Twilio website
- In the directory of your python script, create and .env file to store all API keys needed
- Replace all keys with your own corresponding keys

Example on WhatsApp:

![image](https://github.com/user-attachments/assets/c320ef29-e71b-4a8f-931f-8fcf9ff5bb05)


