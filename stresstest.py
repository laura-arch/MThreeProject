import os

print("Stress Tester App")
print('''
Press 1 for Memory stress testing
Press 2 for Disk stress testing
Press 3 for Network stress testing
Press 4 for CPU stress testing
Press 5 for MySQL stress testing
''')

stresstest = int(input("Option:"))

if stresstest == 1:
	os.system('stress-ng --vm 4 --vm-bytes 1024M')
if stresstest == 2:
	os.system('df -h')
	# os.system('stress-ng --disk 2 --io 2 --timeout 60s --metrics-brief')
if stresstest == 3:
	print('we will use iperf')
	os.system('')
if stresstest == 4:
	os.system('uptime')
	os.system('stress-ng --cpu 4 --timeout 60s --metrics-brief')
	os.system('uptime')
if stresstest == 5:
	print('still to come')
