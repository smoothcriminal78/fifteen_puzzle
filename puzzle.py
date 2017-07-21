from tkinter import *
from fifteen_puzzle import *
from tkinter import messagebox

top = Tk()
top.title('Fifteen title puzzle')
# top.geometry("400x400")

board_frm = Frame(top, highlightbackground="green", highlightcolor="green",
                    highlightthickness=1, width=100, height=100, bd=0)

board = FifteenPuzzle(4, 4)
SOLVED = FifteenPuzzle(4, 4)
board.shuffle(15)
moves = 0

def OnButtonClick(tile):
    if not board.isValidMove(tile):
        return
    global moves
    moves += 1
    x, y = tile.x, tile.y
    board.move(tile)
    refreshBoard()
    if board == SOLVED:
        messagebox.showinfo("INFO", "Solved with {} moves!".format(moves))


def refreshBoard():
    for tile in board.allTilePos():
        val, x, y = board.tiles[tile.x][tile.y], tile.x, tile.y
        if val == 0:
            txt, bgr = '', 'black'
        else:
            txt, bgr = str(val), 'white'
        Button(board_frm, text = txt, bg = bgr, relief = GROOVE, width = 7, height = 3,
                command = lambda t = tile : OnButtonClick(t)).grid(row=x, column=y)

refreshBoard()

board_frm.pack(padx=(10,10), pady=(10,10))
top.mainloop()
