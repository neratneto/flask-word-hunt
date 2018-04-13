from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from board import Board


ALLOWED_EXTENSIONS = set(['txt'])
app = Flask(__name__)

answers = []


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template('home.html')


@app.route("/file", methods=['POST'])
def file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                global BoardClass
                BoardClass = Board(txtfile=filename)
                boardarray = BoardClass.boardarray
                boardlength = BoardClass.boardlength
                return render_template('board.html', boardarray=boardarray, boardlength=boardlength)
            except Exception:
                return "A lista não é adequada"


@app.route("/choice", methods=['POST'])
def choice():
    if request.method == 'POST':
        first = ['', '']
        last = ['', '']
        first[1] = int(request.form['firstx'])
        first[0] = int(request.form['firsty'])
        last[1] = int(request.form['lastx'])
        last[0] = int(request.form['lasty'])
        answer = BoardClass.findSequence(a=first, b=last)
        boardarray = BoardClass.boardarray
        boardlength = BoardClass.boardlength
        if answer:
            global answers
            answers.append(answer)
            return render_template('answers.html', answers=answers, boardarray=boardarray, boardlength=boardlength, message="")
        else:
            return render_template('answers.html', answers=answers, boardarray=boardarray, boardlength=boardlength, message="Try again")


if __name__ == "__main__":
    app.run()
