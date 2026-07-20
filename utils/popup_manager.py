import tkinter as tk
from tkinter import ttk
from models import Measurement,Characteristic,SystemConstant
class PopupManager:
 def __init__(self,root,logger):self.root=root;self.log=logger
 @staticmethod
 def text_for(r):
  if isinstance(r,SystemConstant):return f"Name: {r.name}\n\nType: System_Constant\n\nValue: {r.value}"
  if isinstance(r,(Measurement,Characteristic)):return f"Variable: {r.name}\n\nType: {r.object_type.value}\n\nDescription: {r.description}\n\nUnit: {r.unit}\n\nFunction: {r.function_name}\n\nFunction description: {r.function_description}"
  return "No information found."
 def show(self,r):
  d=tk.Toplevel(self.root);d.withdraw();d.title("SW Reader Helper");d.attributes("-topmost",True);f=ttk.Frame(d,padding=20);f.grid();ttk.Label(f,text=self.text_for(r),justify="left").grid(sticky="w");ttk.Button(f,text="OK",command=d.destroy).grid(row=1,pady=12);d.update_idletasks();w=d.winfo_reqwidth();h=d.winfo_reqheight();d.geometry(f"{w}x{h}+{(d.winfo_screenwidth()-w)//2}+{(d.winfo_screenheight()-h)//2}");d.deiconify();d.lift();d.focus_force();d.grab_set()
