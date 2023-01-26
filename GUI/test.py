from tkinter import *

root = Tk()

root.title("welcome !")
root.geometry('350x200')

menu = Menu(root)
item = Menu(menu)
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)

lbl = Label(root, text="are you ok?")
lbl.grid()

txt = Entry(root, width=10)
txt.grid(row=0, column=1)


def click():
    res = "you wrote" + txt.get()
    lbl.config(text=res)


btn = Button(root, text='click me', fg='red', command=click)
btn.grid(row=0,column=2)
root.mainloop()

