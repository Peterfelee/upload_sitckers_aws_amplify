#!/usr/bin/env bash

cd '..'
cd 'python'

if [[ $1 = "check" ]];then
  python3 check_data.py
elif [[ $1 = "upload" ]];then
 python3 upload_data.py
elif [[ $1 = "pull" ]];then
  python3 pull_data.py
else
   python3 test.py
fi

