#!/usr/bin/env python
import subprocess
from subprocess import Popen
import os
import argparse
import sys
import re

def check_ip(ip_address):
	ip = str(ip_address.strip())
	octets = ip.split('.')
	ip_invalid_msg = "{} is not a valid IPv4 IP address".format(ip)
	if len(octets) != 4:
		raise argparse.ArgumentTypeError(ip_invalid_msg)
		return False
	for octet in octets:
		if not octet.isdigit():
			raise argparse.ArgumentTypeError(ip_invalid_msg)
			return False
		i = int(octet)
		if i < 0 or i > 255:
			raise argparse.ArgumentTypeError(ip_invalid_msg)
			return False
	return ip

def check_file_exists(file):
	if(os.path.isfile(file)):
		return file
	else:
		no_file_exists_msg = "the file {} does not exist".format(file)
		raise argparse.ArgumentTypeError(no_file_exists_msg)
		return False

def snmpcheck_multiple_hosts(ip_address):
	ip = str(ip_address.strip())
	response = Popen(["snmp-check", "-t", ip, "-c", "public"], stdout=subprocess.PIPE)
	std_output = response.communicate()

	no_response = re.search("Error: No response from remote host", str(std_output[0]))
	
	if no_response is not None:
		#status = "{} - No Response from host".format(ip)
		error_file = open("snmp_no_response.log",'a+')
		error_file.write("{} - No Response from host".format(ip) + '\r\n')
		error_file.close()
		#print status
	else:
		output_file = open("{}_snmpcheck.txt".format(ip),'w')
		output_file.write(str(std_output[0]))
		output_file.close()

def main():
	parser = argparse.ArgumentParser(description='''Check a list of IPs using the snmp-check
        tool to gather additional information about a host''')
	parser.add_argument('-f', dest="ip_list", metavar="<FILE>", type=check_file_exists, 
			help="file containing a list of IP Addresses (1 IP per line)")

	args = parser.parse_args()

	with open(args.ip_list) as f:
		for line in f:
			snmpcheck_multiple_hosts(line)

if __name__ == "__main__":
	main()