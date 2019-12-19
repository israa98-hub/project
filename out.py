from framework.runner import Runner
from app.utility.utility import render_index
from app.auth.signin import Signin
from app.auth.register import Register
from app.auth.confirm import ConfirmEmail
from app.auth.resendemail import resend_email
from app.signout import Signout
from app.upload import Upload
from app.avatar import VisitAvatar


app = Runner(entry_file=__file__, debug=False)


@app.route("/")
def index():
    return render_index()


@app.route("/register")
def register():
    register = Register()
    register.register()


@app.route("/signin")
def signin():
    signin = Signin()
    signin.signin()


@app.route("/confirm")
def confirm_email():
    confirm = ConfirmEmail()
    confirm.confirm_email()


@app.route("/resend_confirmation")
def resend_confirmation():
    resend_email()


@app.route("/upload")
def upload():
    upfile = Upload()
    upfile.upload()


@app.route("/signout")
def signout():
    signout = Signout()
    signout.signout()


@app.route("/avatar")
def avatar():
    avatar = VisitAvatar()
    avatar.visit()


if __name__ == '__main__':
    app.dispatch_request()