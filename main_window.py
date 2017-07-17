from fifteen_puzzle import *
from tkinter import *

root = Tk()

fp = FifteenPuzzle();
fp.shuffle(80);

def showBoard(fp):
    frame = Frame(root, highlightbackground="green", highlightcolor="green",
                        highlightthickness=1, width=100, height=100, bd=0)
    for (i, t) in enumerate(fp.tiles):
        for j in range(fp.DIMS):
            Label(frame, text=str(t[j]).rjust(2, ' '),
                  relief=FLAT).grid(row=i, column=j)
    frame.pack(side = LEFT, padx=(0, 7))

solution = fp.aStarSolve()
for fp in solution:
    showBoard(fp);

root.mainloop()
