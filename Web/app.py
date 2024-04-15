import mysql.connector
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, redirect, url_for
import logging
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'Dlcmdls23!@'

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='./logfile.log',  # 로그 파일 경로와 이름
    filemode='a'  # 'a'는 로그 파일에 내용을 추가하는 모드입니다. 'w'로 설정하면 파일을 쓸 때마다 내용이 덮어씌워집니다.
)


# 로컬 데이터베이스 연결 설정 함수
def get_local_db_connection():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='2022Dlcmdls!@',
            database='portal'
        )
    except Exception as e:
        logging.error("Local database connection failed: %s", e)
        raise


# 외부 데이터베이스 연결 설정 함수
def get_external_db_connection():
    try:
        return mysql.connector.connect(
            host='61.97.248.8',
            user='root',
            password='2022Dlcmdls!@',
            database='portal',
            port=13306
        )
    except Exception as e:
        logging.error("External database connection failed: %s", e)
        raise


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 데이터베이스 연결 및 사용자 정보 조회
        conn = get_local_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # 사용자 정보가 있고, 비밀번호가 일치하는지 검증
        if user and check_password_hash(user['password_hash'], password):
            # 로그인 성공: 사용자 세션 생성, 홈 페이지로 리디렉션 등의 처리
            # 예: session['user_id'] = user['id']
            session['username'] = user['username']  # 세션에 username 저장
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'

    # GET 요청 또는 로그인 실패 시 로그인 페이지를 다시 렌더링
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    # 세션에서 사용자 정보 제거
    session.pop('username', None)
    # 사용자를 로그인 페이지로 리디렉션
    return redirect(url_for('login'))


@app.route('/')
def home():
    try:
        if 'username' not in session:  # 사용자가 로그인하지 않았다면
            return redirect(url_for('login'))  # 로그인 페이지로 리디렉션

        external_connection = get_external_db_connection()
        local_connection = get_local_db_connection()

        # 외부 데이터베이스에서 장치 정보를 조회
        external_cursor = external_connection.cursor(dictionary=True)
        external_cursor.execute(
            "SELECT d.device_id, c.customer_nm, d.host_nm, d.serial_num FROM tb_device d JOIN tb_customer c ON d.customer_id = c.customer_id")
        devices = external_cursor.fetchall()
        external_cursor.close()
        external_connection.close()

        # 로컬 데이터베이스에서 체크 상태를 조회
        local_cursor = local_connection.cursor(dictionary=True)
        local_cursor.execute("SELECT device_id, external_device_id, sms_check, email_check FROM tb_device_checks")
        checks = local_cursor.fetchall()
        local_cursor.close()
        local_connection.close()

        # 체크 상태를 장치 정보에 매핑
        for device in devices:
            device['sms_checked'] = 'Y'
            device['email_checked'] = 'Y'
            for check in checks:
                if str(device['device_id']) == str(check['device_id']):
                    device['sms_checked'] = check['sms_check']
                    device['email_checked'] = check['email_check']

    except Exception as e:
        logging.error("Error fetching data: %s", e)
        devices = []  # 오류 발생 시 빈 리스트 반환

    return render_template('home.html', devices=devices)


@app.route('/test')
def test_page():
    try:
        if 'username' not in session:  # 사용자가 로그인하지 않았다면
            return redirect(url_for('login'))  # 로그인 페이지로 리디렉션

    except Exception as e:
        logging.error("Error fetching data: %s", e)
        devices = []  # 오류 발생 시 빈 리스트 반환

    return render_template('test.html')


@app.route('/security_rules')
def security_rules():
    if 'username' not in session:  # 사용자가 로그인하지 않았다면
        return redirect(url_for('login'))  # 로그인 페이지로 리디렉션

    try:
        # 여기서는 예제로 로컬 DB 연결 함수를 사용합니다. 실제 상황에 맞게 조정하세요.
        conn = get_local_db_connection()
        cursor = conn.cursor(dictionary=True)

        # SecurityRules 테이블에서 모든 보안 규칙을 조회
        cursor.execute("SELECT id, rule, description, tactics, technique  FROM SecurityRules")
        rules = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        logging.error("Error fetching security rules: %s", e)
        rules = []  # 오류 발생 시 빈 리스트 반환

    return render_template('security_rules.html', rules=rules)


@app.route('/submit', methods=['POST'])
def submit():
    try:

        external_connection = get_external_db_connection()
        local_connection = get_local_db_connection()

        for external_device_id in request.form.getlist('external_device_id'):
            # 외부 DB에서 해당 device_id의 정보를 조회
            external_cursor = external_connection.cursor(dictionary=True)
            external_cursor.execute(
                "SELECT d.device_id, c.customer_nm, d.host_nm, d.serial_num FROM tb_device d JOIN tb_customer c ON d.customer_id = c.customer_id WHERE d.device_id = %s",
                (external_device_id,))
            device_info = external_cursor.fetchone()
            external_cursor.close()

            if device_info:
                # 폼에서 제공된 SMS와 Email 체크 여부
                sms_check = 'Y' if f'sms_check_{external_device_id}' in request.form else 'N'
                email_check = 'Y' if f'email_check_{external_device_id}' in request.form else 'N'

                # 조회한 정보와 함께 로컬 DB에 저장
                local_cursor = local_connection.cursor()
                insert_query = '''INSERT INTO tb_device_checks (device_id, customer_name, host_name, serial_num, sms_check, email_check)
                  VALUES (%s, %s, %s, %s, %s, %s)
                  ON DUPLICATE KEY UPDATE customer_name = VALUES(customer_name), host_name = VALUES(host_name), serial_num = VALUES(serial_num), sms_check = VALUES(sms_check), email_check = VALUES(email_check)'''
                local_cursor.execute(insert_query, (
                external_device_id, device_info['customer_nm'], device_info['host_nm'], device_info['serial_num'],
                sms_check, email_check))
                local_connection.commit()
                local_cursor.close()

        external_connection.close()
        local_connection.close()
    except Exception as e:
        logging.error("Error during form submission: %s", e)

    return redirect(url_for('home'))


@app.route('/add_rule', methods=['POST'])
def add_rule():
    if 'username' not in session:
        return redirect(url_for('login'))

    rule_name = request.form['rule_name']
    description = request.form['description']
    tactics = request.form['tactics']
    technique = request.form['technique']

    try:
        conn = get_local_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO SecurityRules (rule, description, tactics, technique) VALUES (%s, %s, %s, %s)", (rule_name, description, tactics, technique))
        conn.commit()

        cursor.close()
        conn.close()
    except Exception as e:
        logging.error("Error adding new rule: %s", e)
        return "Error adding new rule", 500

    return redirect(url_for('security_rules'))


@app.route('/edit_rule/<int:rule_id>')
def edit_rule(rule_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_local_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, rule, description, tactics, technique FROM SecurityRules WHERE id = %s", (rule_id,))
    rule = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('edit_rule.html', rule=rule)


@app.route('/update_rule/<int:rule_id>', methods=['POST'])
def update_rule(rule_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    rule_name = request.form['rule_name']
    description = request.form['description']
    tactics = request.form['tactics']
    technique = request.form['technique']

    conn = get_local_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE SecurityRules SET rule = %s, description = %s WHERE id = %s",
                   (rule_name, description, rule_id, tactics, technique))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('security_rules'))


@app.route('/delete_rule/<int:rule_id>')
def delete_rule(rule_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        conn = get_local_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM SecurityRules WHERE id = %s", (rule_id,))
        conn.commit()

        cursor.close()
        conn.close()
    except Exception as e:
        logging.error("Error deleting rule: %s", e)
        # 오류 처리를 위한 추가 로직을 여기에 추가할 수 있습니다.

    return redirect(url_for('security_rules'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

