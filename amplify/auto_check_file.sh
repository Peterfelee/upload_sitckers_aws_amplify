#!/usr/bin/env bash

pip3_list=$(pip3 list)
need_list=(openpyxl pandas xlrd xlwt PIL)

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
msgs=`python3 main.py $1`
one=','
second='['
third=']'
firstMsg=${msgs#*[}
echo $firstMsg
secondMsg=${firstMsg%$third*}
echo $secondMsg
arr=(${secondMsg//$one/})
for msg in ${arr[*]}
do
  echo $msg
done
echo "i test print: $msgs"
echo  "count: ${#arr[*]}"
