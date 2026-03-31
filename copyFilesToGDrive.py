import tkinter as tk
from tkinter import messagebox
import shutil

def info():
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw()
    #messagebox.showinfo(title, message)
    answer = messagebox.askokcancel(
        title='Confirmation',
        message='Would you like to copy the files to GDrive?')
    
    if answer:
        fromWhere = "C:/Users/..." # Put here the local folder in your computer that not syncs
        toWhere = "G:/MyDrive/..." # Put here the GDrive folder where you would like that files be copied and sync
        shutil.copytree(fromWhere,toWhere,dirs_exist_ok=True)
        
        # If you like to make more copies just repeat
        fromWhere = "C:/Users/..." 
        toWhere = "G:/MyDrive/..." 
        shutil.copytree(fromWhere,toWhere,dirs_exist_ok=True)

        messagebox.showinfo(
            title='Sucess',
            message='The files were copied. Wait them to sync in your GDrive.')
    root.destroy()

info()

        
