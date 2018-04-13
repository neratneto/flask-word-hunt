import random
import string
import math
import time


class Board:
    def __init__(self, txtfile):
        self.boardlength = len(Board.getWords(txtfile))
        self.words = random.sample(Board.getWords(txtfile), math.ceil(self.boardlength / 2))  # I'll use half of the possible words picked randomly, so they all fit in the board
        self.boardarray = self.createBoardArray()

    def createBoardArray(self):
        boardarray = []
        count = 0
        for num in range(0, self.boardlength):
            boardarray.append([''] * self.boardlength)
        for i in range(0, len(self.words)):
            if i % 2 == 0:  # Writes the word in the boardarray vertically using a random position
                while True:
                    try:
                        word = self.words[i]
                        position = self.checkPosition(i, boardarray)
                        for x in range(0, len(word)):
                            boardarray[(position[0] + x)][position[1]] = word[x]
                    except ValueError:
                        count += 1
                        if count > self.boardlength:
                            raise Exception("as palavras utilizadas tem tamanho incompatível")
                        continue
                    break
            else:  # Writes the word in the boardarray horizontally using a random position
                while True:
                    try:
                        word = self.words[i]
                        position = self.checkPosition(i, boardarray)
                        for y in range(0, len(word)):
                            boardarray[position[0]][(position[1] + y)] = word[y]
                    except ValueError:
                        count += 1
                        if count > self.boardlength:
                            raise Exception("as palavras utilizadas tem tamanho incompatível")
                        else:
                            continue
                    break
        for i in range(0, self.boardlength):
            for j in range(0, self.boardlength):
                if boardarray[i][j] == '':
                    boardarray[i][j] = random.choice(string.ascii_uppercase)

        return boardarray

    def getWords(txtfile):
        file = open(txtfile, "r")
        prewords = file.readlines()
        words = []
        for word in prewords:
            words.append(word.replace("\n", "").upper())
        if len(max(words, key=len)) > len(words):
            raise ImportError("a maior palavra da lista é maior que o tabuleiro")
        return words

    def randomPosition(self):
        x = random.randrange(0, self.boardlength)
        y = random.randrange(0, self.boardlength)
        position = (x, y)
        return position

    def checkPosition(self, index, boardarray):
        position = self.randomPosition()
        word = self.words[index]
        if index % 2 == 0:  # Even words are vertical
            auxlist = []
            auxarray = boardarray[position[0]:(position[0] + len(word))]
            for i in range(0, len(word)):
                try:
                    auxlist.append(auxarray[i][position[1]])  # If the desired array size is greater than possible, raise error
                except IndexError:
                    raise ValueError("The word does not fit")
            if auxlist == [''] * len(word):  # Checks if the possible spaces are all empty
                return position
            else:
                raise ValueError("The position is not empty")
        else:  # Odd words are horizontal
            if (self.boardlength - position[1]) >= len(word):
                if boardarray[position[0]][position[1]:(position[1] + len(word))] == [''] * len(word):
                    return position
                else:
                    raise ValueError("The position is not empty")
            else:
                raise ValueError("The word does not fit")

    def printBoard(self):
        print("                    Seja bem vindo ao Caça Palavras.")
        time.sleep(1)
        print(" De suas " + str(self.boardlength) + " palavras, selecionamos " + str(len(self.words)) + " aleatórias para incluir no tabuleiro.")
        time.sleep(1)
        print(" Para jogar informe as coordenadas do ponto inicial e final da palavra encontrada.")
        time.sleep(1)
        print(" Caso a resposta seja a correta, lhe informamos a palavra escolhida.\n")
        time.sleep(3)
        print("     ", end="")
        for item in range(0, 10):
            print(" " + str(item) + " ", end="")
        for item in range(10, self.boardlength):
            print(" " + str(item), end="")
        print("")
        for item in range(0, 9):
            print("   " + str(item) + " ", end="")
            for i in range(0, self.boardlength):
                print(" " + str(self.boardarray[item][i]) + " ", end="")
            print(" " + str(item))
        print("y", end="")
        for item in range(9, self.boardlength):
            print("  " + str(item) + " ", end="")
            for i in range(0, self.boardlength):
                print(" " + str(self.boardarray[item][i]) + " ", end="")
            print(" " + str(item))
        print("     ", end="")
        for item in range(0, 10):
            print(" " + str(item) + " ", end="")
        for item in range(10, self.boardlength):
            print(" " + str(item), end="")
        print("\n                                   x")

    def findSequence(self, a, b):
        if a[0] == b[0]:
            try:
                chosen = str().join(self.boardarray[a[0]][a[1]:(b[1] + 1)])
                self.words.index(chosen)
                return chosen
            except (ValueError, IndexError):
                return False
        elif a[1] == b[1]:
            auxlist = []
            try:
                for x in range(a[0], (b[0] + 1)):
                    auxlist.append(self.boardarray[x][a[1]])
                chosen = str().join(auxlist)
                self.words.index(chosen)
                return chosen
            except (ValueError, IndexError):
                return False
        else:
            return False


def playerInput(board):
    while True:
        try:
            first = ["", ""]
            last = ["", ""]
            first[1] = int(input(" X da primeira letra: "))
            first[0] = int(input(" Y da primeira letra: "))
            last[1] = int(input(" X da última letra: "))
            last[0] = int(input(" Y da última letra: "))
        except ValueError:
            print(" Por favor informe um número válido")
            continue
        break
    answer = board.findSequence(a=first, b=last)
    if answer:
        return answer
    else:
        return " Tente novamente"


def main():
    board = Board(txtfile="words.txt")
    board.printBoard()
    while True:
        print(playerInput(board))
