from flask import Flask, current_app, g, render_template, request, url_for, redirect, flash
from email_validator import validate_email, EmailNotValidError
from flask_debugtoolbar import DebugToolbarExtension
import logging


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.debug = True
app.config["SECRET_KEY"] = "2EAZSMss3p5QpbcY2hBsJ"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)

@app.route("/")
def index():
    return "Hello, World!"

@app.route("/contact")
def contact():
    return render_template("/contact.html")


@app.route("/contact/complete", methods=["GET","POST"])
def contact_complete():
    print("start")
    if request.method == "POST":
        print("ifstart")
        #form 속성을 얻는다.
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]
        print("dddstart")

        #입력 체크
        is_valid = True

        if not username:
            flash("사용자 명은 필수입니다.")
            is_valid = False

        if not email:
            flash("이메일은 필수입니다.")
            is_valid = False

        try:
            validate_email(email)

        except EmailNotValidError:
            flash("유효한 이메일 주소를 입력해주세요.")
            is_valid = False

        if not description:
            flash("문의 내용은 필수입니다.")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        flash("문의해주셔서 감사합니다.")
        print("test")


        # Send Email

        #contact 엔드포인트로 리다이렉트한다.
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")


if __name__ == '__main__':
    app.run()