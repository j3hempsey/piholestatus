#! /usr/bin/python

#Script originally created by JON HAYWARD: https://fattylewis.com/Graphing-pi-hole-stats/
#Adapted fo work with InfluxDB by /u/tollsjo in December 2016

# To install and run the script as a service under SystemD. See: https://linuxconfig.org/how-to-automatically-execute-shell-script-at-startup-boot-on-systemd-linux


import requests
import time
from influxdb import InfluxDBClient

HOSTNAME = "pihole" #Pi-hole hostname to report in InfluxDB for each measurement
INFLUXDB_SERVER = "192.168.0.112" #IP or hostname to InfluxDB server
INFLUXDB_PORT = 8086 #Port on InfluxDB server
INFLUXDB_USER="collectdUser" #InfluxDB username to access database with
INFLUXDB_PASSWORD="collectd" #InfluxDB password to access database with
INFLUXDB_DATABASE="collectd" #InfluxDB database to push data to
DELAY = 10 # seconds

def send_msg(domains_blocked, dns_queries_today, ads_percentage_today, ads_blocked_today):

	json_body = [
	    {
	        "measurement": "piholestats",
	        "tags": {
	            "host": HOSTNAME
	        },
	        "fields": {
	            "domains_blocked": int(domains_blocked),
                    "dns_queries_today": int(dns_queries_today),
                    "ads_percentage_today": float(ads_percentage_today),
                    "ads_blocked_today": int(ads_blocked_today)
	        }
	    }
	]

	client = InfluxDBClient(INFLUXDB_SERVER, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, INFLUXDB_DATABASE) #InfluxDB host, InfluxDB port, Username, Password, database
	client.write_points(json_body)

if __name__ == '__main__':
        while True:
          api = requests.get('http://127.0.0.1/admin/api.php') #URI to pihole server api
          API_out = api.json()
          domains_blocked = (API_out['domains_being_blocked']).replace(',', '')
          dns_queries_today = (API_out['dns_queries_today']).replace(',', '')
          ads_percentage_today = (API_out['ads_percentage_today'])
          ads_blocked_today = (API_out['ads_blocked_today']).replace(',', '')

          send_msg(domains_blocked, dns_queries_today, ads_percentage_today, ads_blocked_today)
          time.sleep(DELAY)
