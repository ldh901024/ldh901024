#!/bin/bash

# 체크할 파일의 경로와 이름을 입력하세요.
input_file="/usr/local/backup/Backup_v2/compare_file.txt"

# 파일에 포함된 각 줄을 반복하여 처리합니다.
while IFS= read -r line
do
    # 공백 제거를 위해 문자열 앞뒤의 공백을 제거합니다.
    search_string=$(echo "$line" | tr -d '[:space:]')
    conf_string=".conf"
    file_search_string="$search_string$conf_string"

    # 파일이나 디렉토리에 해당 문자열이 존재하는지 확인합니다.
    if [ -e "/backup/Backup/Backup/2023/07/MSS/Backup_FG/$file_search_string" ]
    then
        echo "$file_search_string: 존재합니다."
    else
        echo "$file_search_string: 존재하지 않습니다."
    fi
done < "$input_file"











