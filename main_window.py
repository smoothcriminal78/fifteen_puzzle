from fifteen_puzzle import *
from tkinter import *
import sys

root = Tk()

star = LabelFrame(root, text="A* algorithm",
                    highlightbackground="green", highlightcolor="green",
                    highlightthickness=1, width=100, height=100, bd=0)
star.pack(padx=(10,10), pady=(10,10))

dijkstra = LabelFrame(root, text="dijkstra algorithm",
                    highlightbackground="green", highlightcolor="green",
                    highlightthickness=1, width=100, height=100, bd=0)
dijkstra.pack(padx=(10,10), pady=(10,10))

def showBoard(algoFrame, fp):
    f = Frame(algoFrame, highlightbackground="black", highlightcolor="green",
                    highlightthickness=1, width=100, height=100, bd=0)
    for (i, t) in enumerate(fp.tiles):
        for j in range(fp.c):
            if t[j] == 0:
                Label(f, text=str('').rjust(2, ' '),
                    relief=FLAT, bg="black").grid(row=i, column=j)
            else:
                Label(f, text=str(t[j]).rjust(2, ' '),
                    relief=FLAT).grid(row=i, column=j)
    f.pack(side = LEFT, padx=(7, 7), pady=(7,7))


fp = FifteenPuzzle(2, 5)
fp.shuffle(10)
solution1 = fp.aStarSolve()
solution2 = fp.dijkstraSolve()

for fp in solution1:
    showBoard(star, fp)
for fp in solution2:
    showBoard(dijkstra, fp)

root.mainloop()
