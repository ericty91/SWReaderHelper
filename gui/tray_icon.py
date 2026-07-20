import pystray
from PIL import Image,ImageDraw
class TrayIcon:
 def __init__(self,o,r,c,l):self.icon=pystray.Icon("SWReaderHelper",self._image(),"SW Reader Helper",pystray.Menu(pystray.MenuItem("Open Window",o),pystray.MenuItem("Restart",r),pystray.MenuItem("Close",c)))
 @staticmethod
 def _image():
  x=Image.new("RGB",(64,64),"#1f6feb");ImageDraw.Draw(x).text((20,22),"SW",fill="white");return x
 def start(self):self.icon.run_detached()
 def stop(self):self.icon.stop()
