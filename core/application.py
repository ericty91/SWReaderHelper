import os,queue,sys
from core.background_worker import BackgroundWorker
from core.clipboard_monitor import ClipboardMonitor
from core.search_engine import SearchEngine
from gui.main_window import MainWindow
from gui.dialogs import show_error
from gui.tray_icon import TrayIcon
from parser.a2l_parser import A2LParser
from utils.popup_manager import PopupManager
from utils.validation import validate_a2l
class Application:
 def __init__(self,root,logger):
  self.root=root;self.log=logger;self.events=queue.Queue();self.window=MainWindow(root,self.start,self.minimize);self.popup=PopupManager(root,logger);self.parser=A2LParser(logger);self.worker=BackgroundWorker(logger);self.engine=None;self.monitor=None;self.exiting=False;self.tray=TrayIcon(lambda:self.events.put(("open",None)),lambda:self.events.put(("restart",None)),lambda:self.events.put(("close",None)),logger);self.tray.start();root.protocol("WM_DELETE_WINDOW",self.minimize);root.after(50,self._drain)
 def run(self):self.root.mainloop()
 def start(self):
  try:p=validate_a2l(self.window.path.get())
  except Exception as x:show_error(self.root,str(x));return
  self.window.busy(True);self.window.set_status("Parsing A2L...");self.worker.start(lambda:self.parser.parse(p,lambda n:self.events.put(("progress",n))),lambda db:self.events.put(("parsed",db)),lambda x:self.events.put(("error",x)))
 def _drain(self):
  if self.exiting:return
  try:
   while True:
    n,p=self.events.get_nowait()
    if n=="progress":self.window.set_status(f"Parsing A2L... {p}%")
    elif n=="parsed":self.engine=SearchEngine(p,self.log);self.monitor=ClipboardMonitor(lambda x:self.events.put(("clip",x)),self.log);self.monitor.start();self.window.set_status(f"Monitoring active - {p.object_count:,} objects loaded");self.window.busy(False);self.root.after(250,self.window.hide)
    elif n=="error":self.window.busy(False);self.window.set_status("Error - A2L loading failed");show_error(self.root,str(p))
    elif n=="clip":self.popup.show(self.engine.find(p))
    elif n=="open":self.window.show()
    elif n=="restart":self.restart()
    elif n=="close":self.close()
  except queue.Empty:pass
  finally:
   if not self.exiting:self.root.after(50,self._drain)
 def minimize(self):self.window.hide()
 def restart(self):self._cleanup();os.execl(sys.executable,sys.executable,*sys.argv)
 def close(self):self.exiting=True;self._cleanup();self.root.destroy()
 def _cleanup(self):
  if self.monitor:self.monitor.stop()
  self.tray.stop()
