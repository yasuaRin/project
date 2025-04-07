from tkinter import *
import joblib

def output():
  num1 = float(e1.get())
  num2 = float(e2.get())

  model = joblib.load('project3')
  result = model.predict[[num1,num2]]
  Label(master,text="Result").grid(row=4)
  Label(master,text=result).grid(row=5)

master = Tk()
master.title('Addition of two numbers using ML')
label = Label(master, text = "Addition of two numbers using ML",
                bg = "black", fg="white").grid(row=0, columnspan=2)

Label(master, text="Enter First Number").grid(row=1)
Label(master, text="Enter Second Number").grid(row=2)

e1 = Entry(master)
e2 = Entry(master)
e1.grid(row=1, column=1)
e2.grid(row=2, column=1)

Button(master, text='Predict', command=output).grid()
