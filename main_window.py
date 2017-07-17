from fifteen_puzzle import *
from tkinter import *


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
        for j in range(fp.DIMS):
            Label(f, text=str(t[j]).rjust(2, ' '),
                  relief=FLAT).grid(row=i, column=j)
    f.pack(side = LEFT, padx=(7, 7), pady=(7,7))


fp = FifteenPuzzle()
fp.shuffle(10)
solution = fp.aStarSolve()
for fp in solution:
    showBoard(star, fp)

root.mainloop()
