import tkinter as tk
from tkinter import ttk
from csv import DictWriter
import os

win = tk.Tk()
win.title('RegGUIapp')

name_label = ttk.Label(win, text='Enter your name : ')
name_label.grid(row=0, column=0, sticky=tk.W)

email_label = ttk.Label(win, text='Enter your email: ')
email_label.grid(row=1, column=0, sticky=tk.W)

age_label = ttk.Label(win, text='Enter your age: ')
age_label.grid(row=2, column=0, sticky=tk.W)

gender_label = ttk.Label(win, text='Select your gender: ')
gender_label.grid(row=3, column=0, sticky=tk.W)

name_var = tk.StringVar()
name_entrybox = ttk.Entry(win, width=16, textvariable=name_var)
name_entrybox.grid(row=0, column=1)
name_entrybox.focus()

email_var = tk.StringVar()
email_entrybox = ttk.Entry(win, width=16, textvariable=email_var)
email_entrybox.grid(row=1, column=1)

age_var = tk.StringVar()
age_entrybox = ttk.Entry(win, width=16, textvariable=age_var)
age_entrybox.grid(row=2, column=1)

gender_var = tk.StringVar()
gender_combobox = ttk.Combobox(win, width=14, textvariable=gender_var, state='readonly')
gender_combobox['values'] = ('Male', 'Female', 'Other')
gender_combobox.current(0)
gender_combobox.grid(row=3, column=1)

user_type = tk.StringVar()
radiobtn1 = ttk.Radiobutton(win, text='Student', value='Student', variable=user_type)
radiobtn1.grid(row=4, column=0)
radiobtn2 = ttk.Radiobutton(win, text='Teacher', value='Teacher', variable=user_type)
radiobtn2.grid(row=4, column=1)

checkbtn_var = tk.IntVar()
checkbtn = ttk.Checkbutton(win, text='Check if you want to subscribe to our newsletters', variable=checkbtn_var)
checkbtn.grid(row=5, columnspan=3)


# def action():
# 	username = name_var.get()
# 	useremail = email_var.get()
# 	userage = age_var.get()
# 	usergender = gender_var.get()
# 	usertype = user_type.get()

# 	if checkbtn_var.get() == 0:
# 		subscribed = 'No'
# 	else:
# 		subscribed = 'Yes'

# 	with open('file.txt', 'a') as f:
# 		f.write(f'{username}, {userage}, {useremail}, {usergender}, {usertype}, {subscribed}\n ')


# 	name_entrybox.delete(0, tk.END)
# 	age_entrybox.delete(0, tk.END)
# 	email_entrybox.delete(0, tk.END)
# 	name_label.configure(foreground='#b388ff')

# 	submit_button.configure(foreground='Blue')

def action():
	username = name_var.get()
	useremail = email_var.get()
	userage = age_var.get()
	usergender = gender_var.get()
	usertype = user_type.get()

	if checkbtn_var.get() == 0:
		subscribed = 'No'
	else:
		subscribed = 'Yes'

	with open('file.csv', 'a',newline='') as f:
		dict_writer = DictWriter(f, fieldnames=['Username', 'User Email', 'User Age', 'User Gender', 'User Type', 'Subscribed'])
		if os.stat('file.csv').st_size == 0:
			dict_writer.writeheader()

		dict_writer.writerow({
			'Username' : username,
			'User Email' : useremail,
			'User Age' : userage,
			'User Gender' : usergender,
			'User Type' : usertype,
			'Subscribed' : subscribed
			})
		
	name_entrybox.delete(0, tk.END)
	age_entrybox.delete(0, tk.END)
	email_entrybox.delete(0, tk.END)
	name_label.configure(foreground='#b388ff')

submit_button = ttk.Button(win, text='Submit', command=action)
submit_button.grid(row=6, column=0)

win.mainloop()