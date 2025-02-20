import os
import time
import random
import mysql.connector
import subprocess
import logging

# Configure logging
logging.basicConfig(filename="stress_test_logs.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# MySQL Connection Details (vm_2)
MYSQL_HOST = "VM2"
MYSQL_USER = "stressUser"
MYSQL_PASS = "Sadika"
MYSQL_DB = "test"

def log_and_print(message):
    print(message)
    logging.info(message)

def log_warning(message):
    print(message)
    logging.warning(message)

def log_error(message):
    print(message)
    logging.error(message)

def log_critical(message):
    print(message)
    logging.critical(message)


def memory_stress():
    log_and_print("Running Memory Stress Test...")
    os.system("stress-ng --vm 2 --vm-bytes 512M --timeout 30s")
    log_and_print("Memory Stress Test Completed.")

def disk_stress():
    log_and_print("Running Disk Stress Test...")
    os.system("dd if=/dev/zero of=/tmp/stress_test_file bs=1M count=1000")
    os.system("rm -f /tmp/stress_test_file")
    log_and_print("Disk Stress Test Completed.")

def network_stress():
    log_and_print("Running Network Stress Test...")
    # Start iperf3 server in the background
    server_process = subprocess.Popen(["iperf3", "-s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the server to start (give it a moment)
    time.sleep(2)

    # Run the client
    result = os.system("iperf3 -c localhost -u -b 100M -t 30")

    # Terminate the server after test is done
    server_process.terminate()

    log_and_print("Network Stress Test Completed.")
    return result

def cpu_stress():
    log_and_print("Running CPU Stress Test...")
    os.system("stress-ng --cpu 4 --timeout 30s")
    log_and_print("CPU Stress Test Completed.")


def mysql_stress():
    log_and_print("Running MySQL Stress Test...")
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=MYSQL_DB
        )
        cursor = conn.cursor()

        for _ in range(80):  # Total queries (same as 8 threads * 10 queries)
            query_type = random.choice(["INSERT", "UPDATE", "SELECT"])

            if query_type == "INSERT":
                cursor.execute("INSERT INTO stress_table (name, value) VALUES ('Test', %s)", (random.randint(1, 10000),))
            elif query_type == "UPDATE":
                cursor.execute("""
                    UPDATE stress_table AS t1
                    JOIN (SELECT id FROM stress_table ORDER BY RAND() LIMIT 1) AS t2
                    ON t1.id = t2.id
                    SET t1.value = t1.value + 1
		""")
            elif query_type == "SELECT":
                cursor.execute("SELECT * FROM stress_table ORDER BY RAND() LIMIT 10")
                cursor.fetchall()

            conn.commit()
            time.sleep(0.1)

        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        log_error("MySQL Error: connection error")

    log_and_print("MySQL Stress Test Completed.")


def main():
    while True:
        print("\n=== Stress Testing Menu ===")
        print("1. Memory Stress Testing")
        print("2. Disk Stress Testing")
        print("3. Network Stress Testing")
        print("4. CPU Stress Testing")
        print("5. MySQL Stress Testing")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            memory_stress()
        elif choice == '2':
            disk_stress()
        elif choice == '3':
            network_stress()
        elif choice == '4':
            cpu_stress()
        elif choice == '5':
            mysql_stress()
        elif choice == '6':
            log_and_print("Exiting Stress Testing Script.")
            break
        else:
            log_error("Invalid choice! Please enter a number between 1-6.")

if __name__ == "__main__":
    main()
