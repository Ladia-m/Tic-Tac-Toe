#!/usr/bin/env Python

from tkinter import *


class Main_window(Frame):
    counter = 0
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("TIC TAC TOE")
#        self.pack(fill=BOTH, expand=1)

        topbar = Menu(self.master)
        self.master.config(menu=topbar)
        file = Menu(topbar)
        file.add_command(label="Exit", command=self.client_exit)
        topbar.add_cascade(label="File", menu=file)

        self.img = PhotoImage(file='data/gifs/img.gif')
        logo = Label(self.master, image=self.img)
        logo.grid(row=0, column=0, pady=10, padx=10)

        entry1label = Label(self.master, text="Enter size (5-10):")
        entry1label.grid(row=1,column=0, padx=10)

        self.entry1 = Entry(self.master)
        self.entry1.config(width=10)
        self.entry1.grid(row=2,column=0)


        self.confirm_img = PhotoImage(file='data/gifs/1.gif')
        entry_button = Button(self.master, text="confirm",
                              padx=2,
                              command=self.start_game)
        entry_button.config(image=self.confirm_img, compound='left')
        entry_button.grid(row=3, column=0)

    def start_game(self):

        try:
            size = int(self.entry1.get())
            if size not in range(5,11):
                 error_message = Label(self.master,
                                       text='Size can be from 5x5 up to 10x10.')
                 error_message.grid(row=4, column=0, padx=10)
                 return None
        except ValueError:
            error_message = Label(self.master, text='Insert only whole #!')
            error_message.grid(row=4, column=0)
            return None

        game_window = Toplevel(self)
        game_window.title("You are playing size %s x %s" %(size, size))
#        game_window.geometry('200x150')

        grid_width = 200
        grid_height = 150
        square_size = 20
        play_grid = Canvas(game_window,
                          width = grid_width,
                          height = grid_height)
        play_grid.pack()
        play_grid.create_line(square_size, 0, square_size, grid_height, fill="#0000ff")



    def client_exit(self):
        exit()



if __name__=='__main__':
    root = Tk()
    TTT = Main_window(root)
    TTT.mainloop()
