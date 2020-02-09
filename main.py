import tkinter
from tkinter import *
from tkinter import scrolledtext
import db, core
import asyncio
top = tkinter.Tk()

top.title("Telegrama")

db.createTable()

lbl1 = Label(top, text = "Total Users: ")
lbl2 = Label(top, text = "Added Users: ")
lbl3 = Label(top, text = "Left Users: ")

lbl4 = Label(top, text = str(db.stats(0)[0]))
lbl5 = Label(top, text = str(db.stats(1)[0]))
lbl6 = Label(top, text = str(db.stats(2)[0]))

lbl1.grid(column=0, row=0)
lbl2.grid(column=0, row=1)
lbl3.grid(column=0, row=2)

lbl4.grid(column=1, row=0)
lbl5.grid(column=1, row=1)
lbl6.grid(column=1, row=2)

lbl7 = Label(top, text = "Name of the group/channel: " )
lbl7.grid(column=0, row=4)

txt1 = Entry(top, width = 20)
txt1.grid(column=1, row=4)

def lookForGroup():
	db.addGroup(txt1.get())	
	core.groupLookout(txt1.get())
	# txtArea.insert('1.0', db.listGroups())
	# txt1.delete(0, 'end')
	lbl4.configure(text=str(db.stats(0)[0]))
	lbl5.configure(text=str(db.stats(1)[0]))
	lbl6.configure(text=str(db.stats(2)[0]))

def secondSearch():
	core.lookAllGroups()
	lbl4.configure(text=str(db.stats(0)[0]))
	lbl5.configure(text=str(db.stats(1)[0]))
	lbl6.configure(text=str(db.stats(2)[0]))

btn1 = Button(top, text="Search Group", command=lookForGroup)
btn2 = Button(top, text="re-search all groups", command=secondSearch)
 
btn1.grid(column=0, row=5)
btn2.grid(column=1, row=5)

lbl8 = Label(top, text = "-- add users --")
lbl9 = Label(top, text = "To group: ")
lblx1 = Label(top, text = "Quantity: ")

lbl8.grid(column=0, row=6)
lbl9.grid(column=0, row=7)
lblx1.grid(column=0, row=8)

txt2 = Entry(top, width = 20)
txt3 = Entry(top, width = 20)

txt2.grid(column=1, row=7)
txt3.grid(column=1, row=8)


async def funcname():
	await core.addToGroup(txt2.get(), db.selectSome(int(txt3.get())))

def addUsers():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(funcname())
	# print(txt2.get())
	# print(int(txt3.get()))
	# print(db.selectSome(int(txt3.get())))

btn3 = Button(top, text="Add", command=addUsers)
btn3.grid(column=1, row=6)
# txtArea = scrolledtext.ScrolledText(top,width=20,height=10) 
# txtArea.grid(column=1,row=6)
# txtArea.insert('1.0', db.listGroups())
# txtArea.config(state='disabled')

top.mainloop()

