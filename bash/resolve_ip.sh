#!/bin/bash
INPUT_FILE=$1
OUTPUT_FILE=$2

IFS=$'\r\n' GLOBIGNORE='*' command eval  'DOMAINS=($(cat $1))'
for line in "${DOMAINS[@]}"; do
	ips=$(getent hosts "$line" | awk '{ print $1 }')
    if [ -z "$ips" ]
        then
            echo $ips,"$line" >> $2
        else
            for ip in $ips
                do
                    echo $ip,"$line" >> $2
            done
    fi
done
