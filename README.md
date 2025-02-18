# MThreeProject

### By Laura, Naomi, Sadika, Zainab

# How to use:

## How to run stress tests
- create a database on VM 2 called test
- create a user with root privileges who can access the database from any machine
- create a table called stress_table
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

- Install stress-ng with ‘yum install stress-ng’
- Write a python script
- Yum install git
- Git clone https://github.com/laura-arch/MThreeProject.git
- Install iPerf with 'yum install iperf3'
- https://www.baeldung.com/linux/iperf-measure-network-performance


https://manpages.ubuntu.com/manpages/xenial/man1/stress-ng.1.html 

## Part 5: Configuration Management using Ansible
- Yum install ansible


