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

cd python || exit
pwd
python3 main.py $1
