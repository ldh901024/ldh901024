import socket


def send_to_syslog(message, server_address=("192.168.249.22", 514)):
    # UDP 소켓 생성
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # 메시지 전송
        sock.sendto(message.encode(), server_address)

    except Exception as e:
        print("오류가 발생했습니다:", str(e))

    finally:
        # 소켓 닫기
        sock.close()


def read_file_and_send_to_syslog(file_path):
    try:
        # 파일 열기 (utf-8 인코딩으로 변경)
        with open(file_path, 'r', encoding='utf-8') as file:
            # 파일 내용 읽기
            file_content = file.read()


            # 파일 내용을 원격 시스로그 서버로 전송
            i = 0
            while i < 30:
                i+=1
                print(i)
                send_to_syslog(file_content)

        print("파일 내용을 성공적으로 원격 시스로그 서버로 전송했습니다.")

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

    except Exception as e:
        print("오류가 발생했습니다:", str(e))


# 파일 경로 지정
file_path = 'D:\\test.txt'  # 실제 파일 경로로 변경해야 합니다.

# 파일 내용을 원격 시스로그 서버로 전송
read_file_and_send_to_syslog(file_path)