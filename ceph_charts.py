#!/usr/bin/python3

import sys

import yaml

import icmplib

import socket

from time import time

from pathlib import Path

MON_PORT = 3300

def ping_hosts(hosts):

        times = []
        
        for host in hosts:

                try:
                        
                        ping_result = icmplib.ping(host, count=3, interval=0.35, privileged=False)                        

                        if ping_result.is_alive:

                                seconds_rtt = ping_result.avg_rtt * 0.001

                                times.append(seconds_rtt)

                        else:

                                sys.stderr.write('Host unreachable: ' + host)

                                times.append('?')

                except icmplib.ICMPError as e:
                        sys.stderr.write(f"An ICMP error occurred: {e}")
                except Exception as e:
                        sys.stderr.write(f"An unexpected error occurred: {e}")                                        

        
        return times


def check_mons(hosts):

        expected_data = 'ceph v2'
        
        times = []

        for host in hosts:

                start = time()
                
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((host, MON_PORT))
                        data = s.recv(128)

                        end = time()

                        received_bytes = data.decode('utf-8')
                        
                        if received_bytes.startswith(expected_data):

                                elapsed_ts = (end - start)

                                times.append(elapsed_ts)

                        else:

                                times.append('?')

        return times
                
                        
def main(cmd):

        yml_fn = Path.home() / '.config' / 'ceph_charts' / 'ceph_charts.yml'

        print('Using configuration file ' + str(yml_fn))
        
        with open(yml_fn, 'r') as file:

                config_data = yaml.safe_load(file)

                if cmd == 'mon_response':

                        hosts = config_data['hosts']

                        start_ts = time()
                        
                        ping_times = ping_hosts(hosts)
                        mon_times = check_mons(hosts)

                        output_line = str(start_ts) + ' '

                        output_line += str(ping_times[0]) + ' ' + str(ping_times[1]) + ' ' + str(ping_times[2]) + ' '

                        output_line += str(mon_times[0]) + ' ' + str(mon_times[1]) + ' ' + str(mon_times[2]) + ' '

                        output_line += '\n'
                        
                        data_fn = config_data['data_fn']

                        print('[WRITE] ' + str(len(output_line)) + ' bytes.')
                        
                        try:
                        
                                with open(data_fn, 'a') as datafile:
                                        result = datafile.write(output_line)
                                        if result <= 0:
                                                print('Problem udating output dat file.')
                                                return -1
                                        datafile.close()

                        except FileNotFoundError:

                                print('No such file or directory: ' + data_fn)
                                return -1
                                
                                
        return 0


if __name__ == '__main__':

	cmds = ['mon_response', 'mon_epochs']

	args = sys.argv[1:]

	if len(args) > 0 and args[0] in cmds:
		main(args[0])

