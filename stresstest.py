import os
import time
import random
import mysql.connector
import subprocess
import logging
import google.generativeai as genai
from twilio.rest import Client
from dotenv import load_dotenv #for api key to load from .env

load_dotenv() # load env variables from .env file

# Configure logging
logging.basicConfig(filename="stress_test_logs.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#saves to this file stress_test_logs.txt
#sets the minimum log level to info - level=logging.INFO so logs all levels
#%(asctime)s → Timestamp of the log entry.
#%(levelname)s → Log level (e.g., INFO, WARNING, ERROR).
#%(message)s → The actual log message.


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

def gemini_log():

    # Set up Gemini API key
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    log_and_print("Analyzing logs...")

    #read logs from file
    with open("stress_test_logs.txt", "r") as file:
       logs = file.read()
    #prepare prompt
    prompt = (
    "Analyze the following logs and provide suggestions. "
    "Make sure your response is **concise** and does not exceed **1600 characters**:\n\n"
    f"{logs}"
    )
    #initialise the gemini model and
    model = genai.GenerativeModel("gemini-pro")
    #generate content based on prompt
    response = model.generate_content(prompt)
    #store response in variable
    suggestions = response.text[:1600]  # Limit to 1600 characters  # Get the response text

    # Save suggestions
    with open("suggestions.txt", "w") as file:
        file.write(suggestions)
    #open - opens the file in write mode, if it doesnt exist then creates, if file exists overwrites the content
    #with(context manager) - ensures the file automatically closes after block code executes
    # w - write, a - append, r - read file

    return suggestions

def whatsapp(message):
#twilio account setup to a number
#dont hardcode sensitive information - store .env file

    account_sid = os.getenv("sidKey")
    auth_token = os.getenv("authKey")

    client = Client(account_sid, auth_token)

    from_phone = os.getenv("FROM_PHONE_NUMBER")
    to_phone = os.getenv("TO_PHONE_NUMBER")


    message = client.messages.create(
  		from_=from_phone,
  		body=message,
		to=to_phone
    )
    log_and_print("Success: message sent")


def memory_stress():
    log_and_print("Running Memory Stress Test...")
    os.system("stress-ng --vm 2 --vm-bytes 512M --timeout 30s")
    #os.system function - runs an external system command using a tool
    #--vm 2 - run 2 virtual memory workers(stimulate memory load by running 2 processors)
    #--vm-bytes 512M - each virtual worker will allocate 512MB of memory
    #--timeout 30s - stress test runs for 30 secs

    log_and_print("Memory Stress Test Completed.")

def disk_stress():
    log_and_print("Running Disk Stress Test...")
    os.system("dd if=/dev/zero of=/tmp/stress_test_file bs=1M count=1000")
    #runs dd command - utility for low-level copying and conversion of data
    #if(input file)= /dev/zero (special file that produces null bytes(0s))-data written to the disks
    #of(output file)= /tmp/stress_test_file - specifies output file
    #parameters: bs=1M - blocksize for each write operation (1 MegaByte)
    #parameters: count=1000 - specifies how many blocks of data will be written - therefore 1000 of 1MB = 1GB on disk
    os.system("rm -f /tmp/stress_test_file")
    #removes output file

    log_and_print("Disk Stress Test Completed.")

def network_stress():
    log_and_print("Running Network Stress Test...")

    server_process = subprocess.Popen(["iperf3", "-s"])
    #starts the iperf3(tool) in background using subprocess.Popen() method
    #["iperf3", "-s"] - runs iperf3 command in server mode (-s) - listens to incoming connections
    time.sleep(2)
    result = os.system("iperf3 -c localhost -u -b 100M -t 30")
    #runs iperf3 client in command line
    #-c localhost - connects client of same machine to iperf3 server
    #-u - tells iperf3 to use UDP instead of TCP for the test
    #-b 100M - sets bandwidth to 100Mbps
    #-t 30 - test runs for 30s

    server_process.terminate()
    #stops background service

    log_and_print("Network Stress Test Completed.")
    return result

def cpu_stress():
    log_and_print("Running CPU Stress Test...")
    os.system("stress-ng --cpu 4 --timeout 30s")
    log_and_print("CPU Stress Test Completed.")
    #tells stress-ng to stress 4 cpu cores for 30 seconds

def mysql_stress():
    log_and_print("Running MySQL Stress Test...")
    #exeception handling
    try:
        #establishes a connection
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=MYSQL_DB
        )
        #cursor object to execute SQL queries
        cursor = conn.cursor()
        #stimulates 500 queries
        for _ in range(500):
            #randomly chooses a query
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
	    #subquery randomises id column and retrieves the first one and outer query matches to the selected ID and then changes the value of ID in outer query - both are the same table
            elif query_type == "SELECT":
                cursor.execute("SELECT * FROM stress_table ORDER BY RAND() LIMIT 10")
                cursor.fetchall()

            conn.commit()
            #realistic interval of database operations
            time.sleep(0.1)

        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        log_error("MySQL Error: connection error")

    log_and_print("MySQL Stress Test Completed.")


def main():
    #while loop
    while True:
        print("\n=== Stress Testing Menu ===")
        print("1. Memory Stress Testing")
        print("2. Disk Stress Testing")
        print("3. Network Stress Testing")
        print("4. CPU Stress Testing")
        print("5. MySQL Stress Testing")
        print("6. Analyze Logs to ChatGPT and Send Logs to your whatsapp")
        print("7. Exit")

        #input statement
        choice = input("Enter your choice: ")

        #if-elif-else
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
            suggestions=gemini_log()
            whatsapp(suggestions)
        elif choice == '7':
            log_and_print("Exiting Stress Testing Script.")
            break
        else:
            log_error("Invalid choice! Please enter a number between 1-6.")

if __name__ == "__main__":
    main()
