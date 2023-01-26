from tkinter import ttk
import tkinter as tk


root = tk.Tk()

signin = ttk.Frame(root)
signin.pack(padx=10, pady=10, fill='x', expand=True)


email_entry = ttk.Entry(signin)
email_entry.pack(fill='x', expand=True)
email_entry.focus()

email_entry.configure(state='disable')
email_entry.configure(state='enable')

root.mainloop()