#!/bin/bash
# EStroev

timing () {
	now=$(date +%s)
	runtime=$(expr $now - $start)
	echo $runtime
	return $runtime
}
echo -en "${LGREEN}$(timing) seconds${NC}\n"

mover() {
	oldFile=$outFolder/$1_$2
	newFile=$outFolder/$timestamp/$1/$1_$2
	test -e $oldFile && mv $oldFile $newFile
}

start=$(date +%s)
LGREEN='\033[1;32m'
YELLOW='\033[0;33m' 
NC="\033[0m"
timestamp=$(date +'%b_%d_%Y')

if [[ $# -eq 0 ]] ; then
    echo "No arguments supplied"
    exit 0
fi

if [ -z "$1" ]
  then
    echo "No argument supplied"
fi

if [[ $# -eq 0 ]]
	then
    	echo '[-] No arguments supplied!'
	    exit 0
fi

# -d FILE - FILE exists and is a directory
# -e FILE - FILE exists
# -f FILE - FILE exists and is a regular file
if [ -f $file ]
  then
    echo "File found"
fi

echo -en "${YELLOW}[+] Network file downloaded!${NC}\n"

latestDir=$(ls -t $folder | head -1)
lines=0
lines=$((lines+l))

end=$(date +%s)
runtime=$(expr $end - $start)
echo -en "\n${LGREEN}Finished: $runtime seconds${NC}\n"
tput sgr0