import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import database

root=customtkinter.CTk()
root.title('Inventory Management System')
root.geometry('800x800+10+10')
root.config(bg='#0A0B0C')
root.resizable(False,False)

font1=('Arial',25,'bold')
font2=('Arial',18,'bold')
font3=('Arial',13,'bold')

def create_chart():
    product_details = database.fetch_products()
    product_names = [product[1] for product in product_details]
    stock_values = [product[2] for product in product_details]

    figure = Figure(figsize=(12, 4.7),dpi=80,facecolor='#0A0B0C')
    ax=figure.add_subplot(111)
    ax.bar(product_names,stock_values,width=0.4,color='#11EA05')
    ax.set_xlabel("Product Name ",color='#fff',fontsize=10)
    ax.set_ylabel("Stock Value",color='#fff',fontsize=10)
    ax.set_title("Product Stock Levels",color='#fff',fontsize=14)
    ax.tick_params(axis='y',labelcolor='#fff',labelsize=12)
    ax.tick_params(axis='x',labelcolor='#fff',labelsize=12)
    ax.set_facecolor('#1B181B')

    canvas=FigureCanvasTkAgg(figure)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0,column=0,padx=0,pady=550)


def insert():
    id=id_entry.get()
    name=name_entry.get()
    stock=stock_entry.get()
    if not(id and name and stock):
        messagebox.showerror('Error','Enter all fields.')
    elif database.id_exists(id):
        messagebox.showerror('Error','ID already exists.')
    else:
        try:
            stock_value=int(stock)
            database.insert_product(id,name,stock_value)
            add_to_treeview()
            clear()
            create_chart()
            messagebox.showinfo('Success','Data has been inserted.')
        except ValueError:
            messagebox.showerror('Error','Stock should be an integer.')

def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
        tree.focus('')
    id_entry.delete(0,END)
    name_entry.delete(0,END)
    stock_entry.delete(0,END)

def add_to_treeview():
    products=database.fetch_products()
    tree.delete(*tree.get_children())
    for product in products:
        tree.insert('',END,values=product)

def display_data(event):
    selected_item=tree.focus()
    if selected_item:
        row=tree.item(selected_item)['values']
        clear()
        id_entry.insert(0,row[0])
        name_entry.insert(0,row[1])
        stock_entry.insert(0,row[2])
    else:
        pass
def update():
    selected_item=tree.focus()
    if not selected_item:
        messagebox.showerror('Error','Choose a product to update.')
    else:
        id=id_entry.get()
        name=name_entry.get()
        stock=stock_entry.get()
        database.update_product(name,stock,id)
        add_to_treeview()
        clear()
        create_chart()
        messagebox.showinfo('Success','Data has been updated')

def delete():
    selected_item=tree.focus()
    if not selected_item:
        messagebox.showerror('Error','Choose a product to delete.')
    else:
        id=id_entry.get()
        database.delete_product(id)
        add_to_treeview()
        clear()
        create_chart()
        messagebox.showinfo('Success','Data has been deleted.')

title_label=customtkinter.CTkLabel(root,font=font1,text='Product Details',text_color='#fff',bg_color='#0A0B0C')
title_label.place(x=35,y=15)

frame=customtkinter.CTkFrame(root,bg_color='#0A0B0C',fg_color='#1B1B21',corner_radius=10,border_width=2,border_color='#fff',width=200,height=370)
frame.place(x=25,y=45)

image1=PhotoImage(file='logo1.png')
image_label=Label(frame,image=image1,bg='#1B1B21')
image_label.place(x=65,y=5)

id_label=customtkinter.CTkLabel(frame,font=font2,text='Coffee ID:',text_color="#fff",bg_color='#0A0B0C')
id_label.place(x=60,y=75)

id_entry=customtkinter.CTkEntry(frame,font=font2,text_color='#000',fg_color='#fff',border_color='#B2016C',border_width=2,width=160)
id_entry.place(x=20,y=105)

name_label=customtkinter.CTkLabel(frame,font=font2,text='Coffee Name:',text_color="#fff",bg_color='#0A0B0C')
name_label.place(x=50,y=140)

name_entry=customtkinter.CTkEntry(frame,font=font2,text_color='#000',fg_color='#fff',border_color='#B2016C',border_width=2,width=160)
name_entry.place(x=20,y=175)

stock_label=customtkinter.CTkLabel(frame,font=font2,text='In Stock:',text_color="#fff",bg_color='#0A0B0C')
stock_label.place(x=60,y=205)

stock_entry=customtkinter.CTkEntry(frame,font=font2,text_color='#000',fg_color='#fff',border_color='#B2016C',border_width=2,width=160)
stock_entry.place(x=20,y=240)

add_button=customtkinter.CTkButton(frame,command=insert,font=font2,text_color='#fff',text='Add',fg_color='#047E43',hover_color='#025B30',bg_color='#1B1B21',cursor='hand2',corner_radius=8,width=80)
add_button.place(x=15,y=280)

clear_button=customtkinter.CTkButton(frame,command=lambda:clear(True),font=font2,text_color='#fff',text='New',fg_color='#E93E05',hover_color='#A82A00',bg_color='#1B1B21',cursor='hand2',corner_radius=8,width=80)
clear_button.place(x=108,y=280)

update_button=customtkinter.CTkButton(frame,command=update,font=font2,text_color='#fff',text='Update',fg_color='#E93E05',hover_color='#A82A00',bg_color='#1B1B21',cursor='hand2',corner_radius=8,width=80)
update_button.place(x=15,y=320)

delete_button=customtkinter.CTkButton(frame,command=delete,font=font2,text_color='#fff',text='Delete',fg_color='#D20B02',hover_color='#8F0600',bg_color='#1B1B21',cursor='hand2',corner_radius=8,width=80)
delete_button.place(x=108,y=320)

style=ttk.Style(root)

style.theme_use('clam')
style.configure('Treeview',font=font3,foreground='#fff',background='#0A0B0C',fieldbackground='#1B1B21')
style.map('Treeview',background=[('selected','#AA04A7')])

tree=ttk.Treeview(root,height=17)

tree['columns']=('ID','Name','In Stock')

tree.column('#0',width=0,stretch=tk.NO)
tree.column('ID',anchor=tk.CENTER,width=150)
tree.column('Name',anchor=tk.CENTER,width=150)
tree.column('In Stock',anchor=tk.CENTER,width=150)

tree.heading('ID',text='ID')
tree.heading('Name',text='Name')
tree.heading('In Stock',text='In Stock')

tree.place(x=400,y=45)
tree.bind('<ButtonRelease>',display_data)
add_to_treeview()
create_chart()
root.mainloop()


