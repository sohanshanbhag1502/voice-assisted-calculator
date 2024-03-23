from math import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as ms
from win32api import GetKeyState
from win32con import VK_NUMLOCK
from PIL import ImageTk, Image
import speech_recognition as srr
import pyttsx3 as py
from threading import Thread


def evaluate(event=None):
    if event:
        b_cal.config(relief=SUNKEN, fg="grey")
        def fu():
            b_cal.config(relief=RAISED, fg="black")
        root.after(100, fu)
    try:
        a = str(expr.get().lower()).replace('ln(', 'log(').replace("^", "**")
        b = eval(a)
        Thread(target=lambda: (speech.say(
            f'The aanswer of {a} is {b}'), speech.runAndWait()), daemon=True).start()
        root.bell()
        val.config(state=NORMAL)
        val.delete(0, END)
        val.insert(0, b)
        val.config(state=DISABLED)

    except ValueError:
        ms.showerror("Input Error", "Enter a valid number")
    except SyntaxError:
        ms.showerror("Input Error", "Invalid expression provided.")
    except TypeError:
        ms.showerror("Input Error", "Enter a valid number")
    except ZeroDivisionError:
        ms.showerror("Division Error", "Cannot divide a number by zero.")
    except NameError:
        ms.showerror("Input Error", "Invalid number.")


def box_entry(literal, backstep=False):
    expr.config(fg='black')
    expr.delete(0, len(expr.get())) if 'Type Here' in expr.get() else 0
    expr.insert(len(expr.get()), literal)
    expr.icursor(expr.index(INSERT)-1) if backstep else 0
    if 'log' in literal:
        Thread(target=lambda: (speech.say(
            'Enter log in the form log(value,base) or use ln for base e.'), speech.runAndWait())).start()
        ms.showinfo(
            'Note', 'Enter log in the form \nlog(value,base) or use ln for base e.')


def del1(event):
    if 'Type Here' in expr.get() and ((str(event.keysym).isdigit()) or (str(event.keysym).isalpha() and len(str(event.keysym)) == 1)):
        expr.delete(0, END)
        expr.insert(END, event.keysym)
        expr.config(fg='black')
    if str(event.keysym).isdigit():
        eval(f'b_{event.keysym}.config(relief=SUNKEN, fg="grey")')

        def fu(): return eval(
            f'b_{event.keysym}.config(relief=RAISED, fg="blue")')
        root.after(100, fu)
    elif str(event.keysym) in ['plus', 'minus', 'slash', 'star', 'percent', 'asciicircum']:
        op = {'plus': 'a', 'minus': 's', 'slash': 'd',
              'star': 'm', 'percent': 'r', 'asciicircum': 'e'}
        eval(f'b_{op[event.keysym]}.config(relief=SUNKEN, fg="grey")')
        def fu(): return eval(
            f'b_{op[event.keysym]}.config(relief=RAISED, fg="blue")')
        root.after(100, fu)
    elif event.keysym.lower() in 'abcdefghijklmnopqrstuvwxyz' or event.keysym.isspace() or event.keysym in ['Tab', 'Scroll_lock']:
        expr.delete(len(expr.get())-1, END)
        ms.showerror('Chars not allowed', 'Only numbers and operators\nare allowed to enter.To enter functions use buttons.')
        root.focus()
        expr.focus()

flag = 0


def listen():
    global flag, comm
    expr.config(fg='black')
    expr.delete(0, len(expr.get()))
    listen = srr.Recognizer()
    if flag == 0:
        speech = py.init()
        speech.say('Hello')
        speech.say(
            'I am your Simple Calculator. Just give me a expression and i will calculate it for you.')
        speech.say('Waiting for your command')
        speech.runAndWait()
    with srr.Microphone() as source:
        root.bell()
        listen.adjust_for_ambient_noise(source, duration=1.0)
        command = listen.listen(source)
        try:
            comm = listen.recognize_google(command)
        except:
            comm=''
            speech.say('Sorry my dear user I cannot hear you.')
            speech.runAndWait()
            speech.stop()
    flag += 1
    dic1={' ':'', 'plus': '+', 'minus':'-', 'into':'*', 'multiplied by':'*', 'dividedby':'/', 'by':'/', 'remainder':'%',
    'raised by':'**', 'comma':',', 'sign':'sin', 'cause':'cos', 'tangent':'tan', 'pie':'pi'}
    comm = comm.lower()
    for i in dic1:
        comm.replace(i, dic1[i])
    comm = comm.replace(' ', '')
    if 'of' in comm:
        o = ''
        for i in comm:
            if ('log' in comm and i.isdigit() == True) or (i == ','):
                o += i
            elif ('sin' in comm and i.isdigit() == True):
                o += i
            elif ('cos' in comm and i.isdigit() == True):
                o += i
            elif ('tan' in comm and i.isdigit() == True):
                o += i
            elif 'degrees' in comm and i.isdigit() == True:
                o += i
            elif 'radians' in comm and i.isdigit() == True:
                o += i
        comm = comm.replace('of', '(')
        comm = comm[:-len(o)]+o+')'
    try:
        speech.say(f'The aanswer of {comm} is'+str(eval(str(comm))))
        speech.runAndWait()
        speech.stop()
    except SyntaxError:
        speech.say('Sorry my dear friend i was not able to hear you try again.')
        speech.runAndWait()
        speech.stop()
    except ZeroDivisionError:
        speech.say('A Number can\'t be divided by zero')
        speech.runAndWait()
        speech.stop()
    except NameError:
        speech.say(
            "Sorry my dear friend i didnt understand what you said. try again.")
        speech.runAndWait()
        speech.stop()
    val.config(state=NORMAL)
    val.delete(0, END)
    val.insert(0, eval(comm))
    expr.delete(0, END)
    expr.insert(0, comm)
    val.config(state=DISABLED)


eve = 1


def Inv():
    global eve
    if eve:
        b_deg.config(text='Rad', command=lambda: box_entry('radians()', 1))
        b_sin.config(text='Sin⁻¹', command=lambda: box_entry('Sin⁻¹()', 1))
        b_cos.config(text='Cos⁻¹', command=lambda: box_entry('Cos⁻¹()', 1))
        b_tan.config(text='Tan⁻¹', command=lambda: box_entry('Tan⁻¹()', 1))
        b_cosec.config(text='Csc⁻¹', command=lambda: box_entry('Csc⁻¹()', 1))
        b_sec.config(text='Sec⁻¹', command=lambda: box_entry('Sec⁻¹()', 1))
        b_cot.config(text='Cot⁻¹', command=lambda: box_entry('Cot⁻¹()', 1))
        eve = 0
    else:
        b_deg.config(text='Deg', command=lambda: box_entry('degrees()', 1))
        b_sin.config(text='Sin', command=lambda: box_entry('Sin()', 1))
        b_cos.config(text='Cos', command=lambda: box_entry('Cos()', 1))
        b_tan.config(text='Tan', command=lambda: box_entry('Tan()', 1))
        b_cosec.config(text='Csc', command=lambda: box_entry('Cosec()', 1))
        b_sec.config(text='Sec', command=lambda: box_entry('Sec()', 1))
        b_cot.config(text='Cot', command=lambda: box_entry('Cot()', 1))
        eve = 1


def e10(en):
    expr.config(fg='black')
    expr.delete(0, len(expr.get())) if 'Type Here' in expr.get() else 0
    if en == 'pi':
        expr.insert(len(expr.get()), pi)
    elif en == 'e':
        expr.insert(len(expr.get()), e)


def op():
    if 'Type Here' in expr.get():
        expr.delete(0, len(expr.get()))
    expr.insert(len(expr.get())+'(')


def prompt(_):
    if str(GetKeyState(VK_NUMLOCK)) == '-128':
        ms.showwarning("Numlock WARNING", "Please turn your Numlock on.")


def insertion(_):
    if expr.get().isspace() or not expr.get():
        expr.config(fg='grey')
        expr.insert(0, 'Type Here...')
        expr.focus()
        expr.icursor(0)

def clear(_):
    global expr, val, b_c
    expr.delete(0, len(expr.get()))
    val.config(state=NORMAL)
    val.delete(0, END)
    val.config(state=DISABLED)
    b_c.config(relief=SUNKEN, fg="grey")
    expr.insert(0, 'Type Here...')
    expr.config(fg='grey')
    expr.icursor(0)
    root.after(100, fu)


root = Tk()
root.resizable(0, 0)
root.attributes("-topmost", True)
root.title("Scientific Calculator")
root.geometry("410x450")
root.iconbitmap('Icon.ico')

bg = PhotoImage(file='img.png')
img = ImageTk.PhotoImage(Image.open('mic.png'))
canvas = Canvas(width=410, height=450)
canvas.place(x=0, y=0)
canvas.create_image(0, 0, anchor=NW, image=bg)

Entryframe = Frame()
Entryframe.place(x=70, y=50)
expr = Entry(Entryframe, font="Arial 17", width=25, fg='grey', relief='ridge', bg='white',
             highlightthickness=2, highlightbackground="#7afefb", highlightcolor="#7afefb")
expr.pack(side=TOP)
expr.insert(0, "Type Here...")
expr.icursor(0)
expr.bind('<FocusIn>', lambda _: expr.config(
    highlightbackground="#7afefb", highlightcolor="#7afefb"))
expr.bind('<FocusOut>', lambda _: expr.config(
    highlightbackground="lightgrey", highlightcolor="lightgrey"))
expr.focus()

xscroll_entry = ttk.Scrollbar(
    Entryframe, orient=HORIZONTAL, command=expr.xview)
xscroll_entry.pack(side=BOTTOM, fill=X)
expr.config(xscrollcommand=xscroll_entry.set)

Valueframe = Frame()
Valueframe.place(x=70, y=115)
val = Entry(Valueframe, font="Arial 17", width=25, fg='grey', relief='ridge', bg='white', borderwidth=2, state=DISABLED,
            disabledbackground='white', disabledforeground='grey')
val.pack(anchor=NW, side=TOP)

xscroll_val = ttk.Scrollbar(Valueframe, orient=HORIZONTAL, command=val.xview)
xscroll_val.pack(side=BOTTOM, fill=X)
val.config(xscrollcommand=xscroll_val.set)

speech = py.init()
speech.setProperty('voice', speech.getProperty('voices')[1].id)

canvas.create_text(207, 20, text='Scientific Calculator Version 2.0(AI)',
                   font='Arial 18 bold', justify=CENTER, fill='darkblue')
canvas.create_text(40, 67, text='Exp:', fill='darkblue', font='Arial 18 bold')
canvas.create_text(40, 130, text='Val:', fill='darkblue', font='Arial 18 bold')

b_1 = Button(text="1", font="Arial 15", command=lambda: box_entry(
    '1'), width=5, bg='white', fg='blue', relief='raised')
b_2 = Button(text="2", font="Arial 15", command=lambda: box_entry(
    '2'), width=5, bg='white', fg='blue', relief='raised')
b_3 = Button(text="3", font="Arial 15", command=lambda: box_entry(
    '3'), width=5, bg='white', fg='blue', relief='raised')
b_4 = Button(text="4", font="Arial 15", command=lambda: box_entry(
    '4'), width=5, bg='white', fg='blue', relief='raised')
b_5 = Button(text="5", font="Arial 15", command=lambda: box_entry(
    '5'), width=5, bg='white', fg='blue', relief='raised')
b_6 = Button(text="6", font="Arial 15", command=lambda: box_entry(
    '6'), width=5, bg='white', fg='blue', relief='raised')
b_7 = Button(text="7", font="Arial 15", command=lambda: box_entry(
    '7'), width=5, bg='white', fg='blue', relief='raised')
b_8 = Button(text="8", font="Arial 15", command=lambda: box_entry(
    '8'), width=5, bg='white', fg='blue', relief='raised')
b_9 = Button(text="9", font="Arial 15", command=lambda: box_entry(
    '9'), width=5, bg='white', fg='blue', relief='raised')
b_ex = Button(text="e", font="Arial 15", command=lambda: e10(
    'e'), width=5, bg='white', fg='blue', relief='raised')
b_pi = Button(text="π", font="Arial 15", command=lambda: e10(
    'pi'), width=5, bg='white', fg='blue', relief='raised')
b_0 = Button(text="0", font="Arial 15", command=lambda: box_entry(
    '0'), width=5, bg='white', fg='blue', relief='raised')
b_a = Button(text="+", font="Arial 15", command=lambda: box_entry('+'),
             width=5, bg='white', fg='blue', relief='raised')
b_s = Button(text="-", font="Arial 15", command=lambda: box_entry('-'),
             width=5, bg='white', fg='blue', relief='raised')
b_d = Button(text="/", font="Arial 15", command=lambda: box_entry('/'),
             width=5, bg='white', fg='blue', relief='raised')
b_m = Button(text="X", font="Arial 15", command=lambda: box_entry(
    'X'), width=5, bg='white', fg='blue', relief='raised')
b_r = Button(text="%", font="Arial 15", command=lambda: box_entry(
    '%'), width=5, bg='white', fg='blue', relief='raised')
b_e = Button(text="^", font="Arial 15", command=lambda: box_entry(
    '^'), width=5, bg='white', fg='blue', relief='raised')
b_ln = Button(text="ln", font="Arial 15", command=lambda: box_entry(
    'ln()', 1), width=5, bg='white', fg='blue', relief='raised')
b_log = Button(text="log", font="Arial 15", command=lambda: box_entry(
    'log()', 1), bg='white', fg='blue', relief='raised', width=5)
b_fac = Button(text="n!", font="Arial 15", command=lambda: box_entry(
    'factorial()', 1), bg='white', fg='blue', relief='raised', width=5)
b_mod = Button(text="|x|", font="Arial 15", command=lambda: box_entry(
    'mod()', 1), bg='white', fg='blue', relief='raised', width=5)
b_sin = Button(text="Sin", font="Arial 15", command=lambda: box_entry(
    'Sin()', 1), bg='white', fg='blue', relief='raised', width=5)
b_cos = Button(text="Cos", font="Arial 15", command=lambda: box_entry(
    'Cos()', 1), bg='white', fg='blue', relief='raised', width=5)
b_tan = Button(text="Tan", font="Arial 15", command=lambda: box_entry(
    'Tan()', 1), bg='white', fg='blue', relief='raised', width=5)
b_sec = Button(text="Sec", font="Arial 15", command=lambda: box_entry(
    'Sec()', 1), bg='white', fg='blue', relief='raised', width=5)
b_cosec = Button(text="Csc", font="Arial 15", command=lambda: box_entry(
    'Cosec()', 1), bg='white', fg='blue', relief='raised', width=5)
b_cot = Button(text="Cot", font="Arial 15", command=lambda: box_entry(
    'Cot()', 1), bg='white', fg='blue', relief='raised', width=5)
b_deg = Button(text='Deg', font="Arial 15", width=5, command=lambda: box_entry(
    'degrees()', 1), bg='white', fg='blue', relief='raised')
b_inv = Button(text="Inv", font="Arial 15", command=Inv,
               bg='white', fg='blue', relief='raised', width=5)
b_cal = Button(text="Calculate", font="Arial 18", width=17,
               padx=6, command=evaluate, bg='white')
b_c = Button(text="C", font="Arial 18", width=4, command=lambda: (expr.delete(0, len(expr.get(
))), val.config(state=NORMAL), val.delete(0, END), val.config(state=DISABLED)),  bg='white')
b_mic = Button(image=img, command=listen, width=59,  bg='white')
b_1.place(x=10, y=180)
b_2.place(x=75, y=180)
b_3.place(x=140, y=180)
b_4.place(x=10, y=220)
b_5.place(x=75, y=220)
b_6.place(x=140, y=220)
b_7.place(x=10, y=260)
b_8.place(x=75, y=260)
b_9.place(x=140, y=260)
b_ex.place(x=10, y=300)
b_pi.place(x=75, y=300)
b_0.place(x=140, y=300)
b_a.place(x=205, y=180)
b_s.place(x=270, y=180)
b_m.place(x=335, y=180)
b_d.place(x=205, y=220)
b_r.place(x=270, y=220)
b_e.place(x=335, y=220)
b_ln.place(x=205, y=260)
b_log.place(x=270, y=260)
b_fac.place(x=335, y=260)
b_mod.place(x=205, y=300)
b_sin.place(x=270, y=300)
b_cos.place(x=335, y=300)
b_tan.place(x=10, y=340)
b_sec.place(x=75, y=340)
b_cosec.place(x=140, y=340)
b_cot.place(x=205, y=340)
b_deg.place(x=270, y=340)
b_inv.place(x=335, y=340)
b_mic.place(x=10, y=380)
b_cal.place(x=76, y=380)
b_c.place(x=334, y=380)


fu= lambda :b_c.config(relief=RAISED, fg="black")


root.bind("<Return>", evaluate)
root.bind('<Escape>', lambda _: root.destroy())
root.bind('c', clear)

if str(GetKeyState(VK_NUMLOCK)) == '0':
    ms.showwarning("Numlock WARNING", "Please turn your Numlock on.")

root.bind('<Num_Lock>', prompt)
root.bind('<Key>', del1)
root.bind('<1>', insertion)
root.mainloop()

speech.say('Thankyou for using simple calculator. Have a good day.')
speech.runAndWait()