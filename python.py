from time import sleep
from threading import Thread
from os import system, _exit
from readchar import readchar
from random import randrange
from playsound import playsound

rows, columns = 15,20
arena = [[" " for x in range(columns)] for y in range(rows)]
score=0
def displayArena():
    print(' '*(columns//2+3),'SCORE', ':','\033[36m',score,'\033[00m')
    print("\n ", end="")
    for k in range(2 * columns + 1):
        print("–", end="")
    print()
    for i in range(rows):
        print("|", end=" ")
        for j in range(columns):
            if arena[i][j] == "O":
                print("\033[91m", arena[i][j], "\033[00m", sep="", end=" ")
            elif arena[i][j] == "*":
                print("\033[42m", ".", "\033[00m", sep="", end=" ")
            else:
                print(arena[i][j], end=" ")
        print("|", end=" ")
        print()
    print(" ", end="")
    for k in range(2 * columns + 1):
        print("–", end="")
    print()


hr, hc, tr, tc = 0, 2, 0, 0
key, f, k = "d", [0, 1], "d"


def readKey():
    while True:
        global key
        k = readchar()
        if key == "d" and k in ("w", "s", "d"):
            key = k
        elif key == "a" and k in ("w", "a", "s"):
            key = k
        elif key == "w" and k in ("w", "a", "d"):
            key = k
        elif key == "s" and k in ("a", "s", "d"):
            key = k

pos = [[0, 0], [0, 1], [0, 2]]
for i in pos:
    arena[i[0]][i[1]] = "*"


def food():
    global pos, hr, hc
    f = [randrange(0, rows - 1), randrange(0, columns - 1)]
    if f in pos:
        food()
    else:
        arena[f[0]][f[1]] = "O"


def sound(event):
    if event == "chew":
        playsound("chew.mp3")
    elif event == "gameOver":
        playsound("failuredrum.mp3")
        print("GAME OVER!")
        playsound("game_over.mp3")
        _exit(1)


def foodGen():
    global arena, hr, hc, pos,score
    present = False
    for x in arena:
        if "O" in x:
            present = True
            break
    if not present:
        Thread(target=sound, args=["chew"]).start()
        score+=1
        tr, tr_, tc, tc_ = pos[0][0], pos[1][0], pos[0][1], pos[1][1]
        if tr == tr_:
            if tc < tc_:
                pos.append([tr, tc - 1])
            else:
                pos.append([tr, tc + 1])
        else:
            if tr < tr_:
                pos.append([tr - 1, tc])
            else:
                pos.append([tr, tc + 1])
        food()


def nextFrame():
    global arena, pos, hr, hc
    arena[hr][hc] = "*"
    pos.append([hr, hc])
    arena[pos[0][0]][pos[0][1]] = " "
    pos = pos[1:]


def move():
    try:
        global hr, key, hc, tr, tc, pos, f, k
        if pos[-1] in pos[:-1]:
            print('CRASH!')
            sound("gameOver")
            print("\033[?25h", end="", flush=True)
        if key == "d":
            hc += 1
            nextFrame()
        elif key == "s":
            hr += 1
            nextFrame()
        elif key == "a":
            if hc > 0:
                hc -= 1
            else:
                sound("gameOver")
                print("\033[?25h", end="", flush=True)
            nextFrame()
        elif key == "w":
            if hr > 0:
                hr -= 1
            else:
                sound("gameOver")
                print("\033[?25h", end="", flush=True)
            nextFrame()
        else:
            pass
    except IndexError:
        sound("gameOver")
        print("\033[?25h", end="", flush=True)


def show():
    food()
    while True:
        system("clear")
        foodGen()
        displayArena()
        move()
        sleep(0.07)

t1, t2 = Thread(target=readKey), Thread(target=show)
print("\033[?25l", end="", flush=True)
print("\033[1D",end="")
system("clear")
print("\nUse W,A,S,D to move.Press any key to start...\n")
displayArena()
try:
    if ord(readchar())>0:
        t1.start()
        t2.start()
except KeyboardInterrupt:
    print("\033[?25h", end="", flush=True)