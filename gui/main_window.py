import tkinter as tk
from tkinter import ttk,filedialog
class MainWindow:
 def __init__(self,root,on_start,on_minimize):
  self.root=root;self.path=tk.StringVar();self.status=tk.StringVar(value="Ready");root.title("SW Reader Helper");root.resizable(False,False);f=ttk.Frame(root,padding=20);f.grid();ttk.Label(f,text="SW Reader Helper",font=("Segoe UI",14,"bold")).grid(row=0,columnspan=2,pady=(0,15));ttk.Label(f,text="A2L File").grid(row=1,column=0,sticky="w");ttk.Entry(f,textvariable=self.path,width=60,state="readonly").grid(row=2,column=0,padx=(0,8),pady=8);ttk.Button(f,text="Browse...",command=self._browse).grid(row=2,column=1);self.start_button=ttk.Button(f,text="Start",command=on_start);self.start_button.grid(row=3,column=0);ttk.Button(f,text="Minimize",command=on_minimize).grid(row=3,column=1);ttk.Label(f,textvariable=self.status).grid(row=4,columnspan=2,pady=(12,0))
 def _browse(self):
  x=filedialog.askopenfilename(filetypes=(("A2L files","*.a2l"),))
  if x:self.path.set(x)
 def set_status(self,text):self.status.set(text);self.root.update_idletasks()
 def busy(self,v):self.start_button.configure(state="disabled" if v else "normal")
 def show(self):self.root.deiconify();self.root.lift();self.root.focus_force()
 def hide(self):self.root.withdraw()
