#!/usr/bin/env bash

cd '..'
if [[ $1 = "check" ]];then
  python3 check_data.py
elif [[ $1 = "upload" ]];then
 python3 upload_data.py
elif [[ $1 = "pull" ]];then
  python3 pull_amplify_data.py
else
   echo "nothing"
fi

