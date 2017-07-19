from fifteen_puzzle import *
from tkinter import *
import sys

root = Tk()

def run():
    fp = FifteenPuzzle(2, 5)
    sn = 4
    try:
        sn = int(shflNum.get())
    except ValueError:
        messagebox.showinfo("INFO", "Shuffle number must be integer")
        return

    fp.shuffle(sn)

    showBoard(*fp.aStarSolve())
    showBoard(*fp.dijkstraSolve())

def showBoard(solution, txt):
    algoFrm = LabelFrame(root, text=txt,
                        highlightbackground="green", highlightcolor="green",
                        highlightthickness=1, width=100, height=100, bd=0)
    algoFrm.pack(padx=(10,10), pady=(10,10))
    for fp in solution:
        f = Frame(algoFrm, highlightbackground="black", highlightcolor="green",
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

def on_entry_click(event):
    shflNum.delete(0, END)

def run_btn_click(event):
    run()

settingsFrm = LabelFrame(root, text="Settings",
                    highlightbackground="green", highlightcolor="green",
                    highlightthickness=1, width=100, height=100, bd=0)
settingsFrm.pack(padx=(10,10), pady=(10,10))

shflNum = Entry(settingsFrm, textvariable=StringVar(root, value="Enter shuffle number"), fg="black")
shflNum.bind('<FocusIn>', on_entry_click)
shflNum.pack(padx=(5,5), pady=(5,5))

runBtn = Button(settingsFrm, text="Run")
runBtn.bind('<Button-1>', run_btn_click)
runBtn.pack(padx=(5,5), pady=(5,5))

root.mainloop()
