import os
import time
import random
import mysql.connector
import subprocess

# MySQL Connection Details (vm_2)
MYSQL_HOST = "VM2"
MYSQL_USER = "stressUser"
MYSQL_PASS = "Sadika"
MYSQL_DB = "test"

def memory_stress():
    print("\n[INFO] Running Memory Stress Test...")
    os.system("stress-ng --vm 2 --vm-bytes 512M --timeout 30s")
    print("\n[INFO] Memory Stress Test Completed.")

def disk_stress():
    print("\n[INFO] Running Disk Stress Test...")
    os.system("dd if=/dev/zero of=/tmp/stress_test_file bs=1M count=1000")
    os.system("rm -f /tmp/stress_test_file")
    print("\n[INFO] Disk Stress Test Completed.")

def network_stress():
    print("\n[INFO] Running Network Stress Test...")
    # Start iperf3 server in the background
    server_process = subprocess.Popen(["iperf3", "-s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the server to start (give it a moment)
    time.sleep(2)

    # Run the client
    result = os.system("iperf3 -c localhost -u -b 100M -t 30")

    # Terminate the server after test is done
    server_process.terminate()

    print("\n[INFO] Network Stress Test Completed.")
    return result

def cpu_stress():
    print("\n[INFO] Running CPU Stress Test...")
    os.system("stress-ng --cpu 4 --timeout 30s")
    print("\n[INFO] CPU Stress Test Completed.")


def mysql_stress():
    print("\n[INFO] Running MySQL Stress Test...")
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
        print(f"[ERROR] MySQL Error: {e}")

    print("\n[INFO] MySQL Stress Test Completed.")


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
            print("\n[INFO] Exiting Stress Testing Script.")
            break
        else:
            print("\n[ERROR] Invalid choice! Please enter a number between 1-6.")

if __name__ == "__main__":
    main()
