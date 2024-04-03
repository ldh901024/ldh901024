import pandas as pd

# .dat 파일의 경로
dat_file_path = 'C:\\Users\\ldh90\\Downloads\\device_list.dat'

# Excel 파일로 저장될 경로
excel_file_path = 'C:\\Users\\ldh90\\Downloads\\device_list.xlsx'

# .dat 파일을 읽기 (이 부분은 파일의 형식에 따라 조정해야 할 수 있음)
# 여기서는 콤마로 구분된 값을 예로 들고 있습니다.
df = pd.read_csv(dat_file_path, delimiter=',')

# DataFrame을 Excel 파일로 저장
df.to_excel(excel_file_path, index=False)

print("Excel 파일이 생성되었습니다:", excel_file_path)