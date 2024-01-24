#!/bin/bash

# 파라미터로 IP 주소와 검색할 디렉토리를 받습니다.
search_string="$1"
search_directory="$2"
conf_string=".conf"
file_search_string="${search_string}${conf_string}"

echo $file_search_string >> /search_cmd.txt

if [ -e "${search_directory}/${file_search_string}" ]
then
    #echo "${file_search_string}: 존재합니다."
    echo "success"
else
    #echo "${file_search_string}: 존재하지 않습니다."
    echo "false2"
fi
