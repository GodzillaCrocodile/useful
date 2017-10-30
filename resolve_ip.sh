#!/bin/bash
IFS=$'\r\n' GLOBIGNORE='*' command eval  'DOMAINS=($(cat domains.txt))'
for line in "${DOMAINS[@]}"; do
	ip=$(getent hosts "$line" | awk '{ print $1 }')
	echo $ip, "$line"
done
