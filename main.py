from flask import Flask, request, render_template, jsonify
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


@app.route("/board", methods=['POST'])
def board():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            txtfile = file.read()
            try:
                global BoardClass
                BoardClass = Board(file=str(txtfile))
                boardarray = BoardClass.boardarray
                boardlength = BoardClass.boardlength
                words = BoardClass.words
                return render_template('board.html', boardarray=boardarray, boardlength=boardlength, words=words)
            except (ValueError, IndexError, ImportError):
                return "A lista não é adequada"


@app.route("/choice", methods=['GET', 'POST'])
def choice():
    firstx = int(request.args.get('firstx'))
    firsty = int(request.args.get('firsty'))
    lastx = int(request.args.get('lastx'))
    lasty = int(request.args.get('lasty'))
    first = [firsty, firstx]
    last = [lasty, lastx]
    boardlength = int(request.args.get('boardlength'))
    preboardarray = request.args.get('boardarray').replace("[", "").replace("]", "").replace(", '", "").replace("'", "")
    boardarray = []
    for i in range(0, boardlength):
        vector = preboardarray[0:boardlength]
        preboardarray = preboardarray.replace(vector, "")
        boardarray.append(list(vector))
    words = request.args.get('words').replace("['", "").replace("']", "").replace(", '", "").split("'")
    answer = Board.findSequence(boardarray, words, first, last)
    if answer:
        return jsonify(result=answer)
    else:
        return jsonify(result="deu ruim piazada")


if __name__ == "__main__":
    app.run()
