#!/usr/bin/env bash

pip3_list=$(pip3 list)
need_list=(openpyxl pandas xlrd xlwt)

for need_package in "${need_list[@]}"
do
  if [[ $pip3_list =~  $need_package ]];then
    echo "$need_package" is installed
  else
    pip3 install "$need_package"
  fi
done

cd test2 || exit
pwd

if [[ $1 = "check" ]];then
  python3 check_data.py
elif [[ $1 = "upload" ]];then
 python3 upload_data.py
elif [[ $1 = "pull" ]];then
  python3 pull_data.py
else
   python3 test2.py
fi
