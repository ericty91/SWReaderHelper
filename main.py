import tkinter as tk
from core.application import Application
from utils.logger import configure_logging
def main():
 l=configure_logging();root=tk.Tk()
 try:Application(root,l).run()
 except Exception:l.critical("Fatal error",exc_info=True);root.destroy()
if __name__=="__main__":main()
