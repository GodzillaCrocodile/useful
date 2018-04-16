#!/bin/bash
# EStroev

USERID=""
KEY=""
URL="https://api.telegram.org/bot$KEY/sendMessage"
DATE_EXEC="$(date "+%d %b %Y %H:%M")"
HTTP_PROXY=""
MESSAGE=$1
TEXT="$DATE_EXEC: $MESSAGE"

curl -s -x $HTTP_PROXY -d "chat_id=$USERID&disable_web_page_preview=1&text=$TEXT" $URL > /dev/null