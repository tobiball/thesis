try:
    import Tkinter as tk
except:
    import tkinter as tk

app = tk.Tk()
app.title("Experiment")
app.geometry('300x200')

app.configure(bg='green')
app.mainloop()