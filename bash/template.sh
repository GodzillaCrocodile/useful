#!/bin/bash
# EStroev

timing () {
	now=$(date +%s)
	runtime=$(expr $now - $start)
	echo $runtime
	return $runtime
}
echo -en "${LGREEN}$(timing) seconds${NC}\n"

if [[ $# -eq 0 ]] ; then
    echo "No arguments supplied"
    exit 0
fi

if [ -z "$1" ]
  then
    echo "No argument supplied"
fi

start=$(date +%s)
LGREEN='\033[1;32m'
NC="\033[0m"


lines=0
lines=$((lines+l))

end=$(date +%s)
runtime=$(expr $end - $start)
echo -en "\n${LGREEN}Finished: $runtime seconds${NC}\n"
tput sgr0