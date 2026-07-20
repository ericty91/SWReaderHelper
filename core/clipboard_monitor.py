import threading
import keyboard,pyperclip
class ClipboardMonitor:
 def __init__(self,on_text,logger):self.on_text=on_text;self.log=logger;self.stop_event=threading.Event();self.copy_event=threading.Event();self.thread=None;self.hook=None;self.last=""
 def start(self):self.stop_event.clear();self.last="";self.hook=keyboard.add_hotkey("ctrl+c",self.copy_event.set,suppress=False);self.thread=threading.Thread(target=self._run,name="ClipboardMonitor",daemon=True);self.thread.start()
 def stop(self):
  self.stop_event.set();self.copy_event.set()
  if self.hook is not None:
   try:keyboard.remove_hotkey(self.hook)
   except Exception:self.log.exception("Hook cleanup failure")
  if self.thread and self.thread.is_alive():self.thread.join(1)
 def sanitize(self,v):
  if not isinstance(v,str):return None
  v=v.strip()
  if not v or len(v)>200 or "\n" in v or "\r" in v or v==self.last:return None
  self.last=v;return v
 def _run(self):
  while not self.stop_event.is_set():
   self.copy_event.wait(.5)
   if self.stop_event.is_set():break
   if not self.copy_event.is_set():continue
   self.copy_event.clear()
   if self.stop_event.wait(.15):break
   try:v=self.sanitize(pyperclip.paste())
   except Exception:self.log.exception("Clipboard failure");continue
   if v:self.on_text(v)
