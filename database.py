import sqlite3

def create_table():
    conn=sqlite3.connect('Products.db')
    cursor=conn.cursor()

    cursor.execute('''
                   Create table if not exists Products(
                   id Text primary key,
                   name text,
                   in_stock integer)''')
    conn.commit()
    conn.close()

def fetch_products():
    conn=sqlite3.connect('Products.db')
    cursor=conn.cursor()
    cursor.execute('select * from products')
    Products=cursor.fetchall()
    conn.close()
    return Products

def insert_product(id,name,in_stock):
    conn=sqlite3.connect('Products.db')
    cursor=conn.cursor()
    cursor.execute('insert into Products(id,name,in_stock) values (?,?,?)',(id,name,in_stock))
    conn.commit()
    conn.close()

def delete_product(id):
    conn=sqlite3.connect('Products.db')
    cursor=conn.cursor()
    cursor.execute('delete from Products where id=?',(id,))
    conn.commit()
    conn.close()

def update_product(new_name,new_stock,id):
    conn=sqlite3.connect('Products.db')
    cursor=conn.cursor()
    cursor.execute('update Products set name=?,in_stock=? where id=?',(new_name,new_stock,id))
    conn.commit()
    conn.close()

def id_exists(id):
    conn=sqlite3.connect('Products.db')
    cursor=conn.cursor()
    cursor.execute('select count(*) from Products where id=?',(id,))
    result=cursor.fetchone()
    conn.close()
    return result[0]>0

create_table()

