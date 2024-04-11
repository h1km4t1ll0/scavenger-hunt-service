#!/bin/bash
BOT_TOKEN=6652038217:AAEY0Znq7UHaM4aP7WF8ZXnP6Ef99sFd-B4
CHAT_ID=-695909740
docker exec scavenger-hunt_database_1 pg_dump -U postgres scavenger_hunt  > scavenger_hunt_dump.sql
# curl -F document=@"./scavenger_hunt_dump.sql" https://api.telegram.org/bot$BOT_TOKEN/sendDocument?chat_id=$CHAT_ID

TEXT_TO_SEND='some *example text* _caption_ here, use Markdown v1 syntax'

curl -4 -s -S -L -w"\n" -o- \
    -F document=@"./scavenger_hunt_dump.sql" \
    -F caption="Дамп от $(date +%d-%m-%Y"T"%H%M%S)" \
    -X POST https://api.telegram.org/bot${BOT_TOKEN}/sendDocument \
    -F chat_id="${CHAT_ID}"
