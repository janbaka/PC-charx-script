#!/bin/bash

# Define the IP address
ip=192.168.0.32

# Define controller ports
ports=(2 3 4 5)

# Define ping attempts
ping_attempts=4

# Define color codes for colored printing
red=31
green=32
blue=94

# Prints colored text
color() {
	echo -e "\e[$1m$2\e[0m"
}

# Prints a separator
separator() {
	echo -ne "\n\e[90m"

	for i in $(seq 1 $(tput cols)); do
		echo -n -
	done

	echo -e "\e[0m\n"
}

# Enables a port
enable_port() {
	echo "Enabling port $1..."

	curl "http://192.168.0.254/php/command.php?usr=admin&pwd=private&cmd=port%20$1%20admin-mode%20enable"
}

# Disables a port
disable_port() {
	echo "Disabling port $1..."

	curl "http://192.168.0.254/php/command.php?usr=admin&pwd=private&cmd=port%20$1%20admin-mode%20disable"
}

# Disables all ports
disable_all_ports() {
	echo "Disabling all ports..."

	for port in ${ports[@]}; do
		disable_port $port
	done
}

# Sets the IP address for a port
set_port_ip() {
	echo "Setting IP address $ip for port $1..."

	curl "http://192.168.0.254/php/command.php?usr=admin&pwd=private&cmd=dhcp-service%20server%20port-local-clear%20|%20dhcp-service%20server%20port-local%20$1%20status%20enable%20|%20dhcp-service%20server%20port-local%20$1%20net-mask%20255.255.255.000%20|%20dhcp-service%20server%20port-local%20$1%20local-ip%20$ip"
}

# Tries to ping a port
ping_port() {
	echo "Checking ping for IP address $ip and port $1..."

	for attempt in $(seq 1 $ping_attempts); do
		sleep 30
		echo "Port $1: $(color $blue "Ping attempt $attempt")"

		if ping -c 1 $ip > /dev/null; then
			echo "Port $1: $(color $green "Ping successful")"
			break
		elif [ $attempt == $ping_attempts ]; then
			echo "Port $1: $(color $red "Ping failed")"
		fi
	done
}

# Tests a port
test_port() {
	echo "Testing port $1..."

	set_port_ip $1
	separator

	enable_port $1
	separator

	ping_port $1
	separator

	disable_port $1
	separator
}

# Tests all ports
test_all_ports() {
	echo "Testing all ports..."

	for port in ${ports[@]}; do
		test_port $port
	done
}

disable_all_ports
test_all_ports
