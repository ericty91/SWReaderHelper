import sys,types,unittest
try:
    import tkinter
    from tkinter import ttk
except ImportError:
    ttk=types.SimpleNamespace()
    tkinter=types.SimpleNamespace(Tk=object,Toplevel=object,TclError=Exception,ttk=ttk)
    sys.modules['tkinter']=tkinter
    sys.modules['tkinter.ttk']=ttk
from models import SystemConstant,Measurement,ObjectType
from utils.popup_manager import PopupManager
class PopupTests(unittest.TestCase):
 def test_system_constant_layout(self):self.assertEqual(PopupManager.text_for(SystemConstant('CPU_TYPE','TC397')),'Name: CPU_TYPE\n\nType: System_Constant\n\nValue: TC397')
 def test_local_measurement_type(self):
  x=Measurement('Local_MP','D','rpm','Fn','Desc','CM',ObjectType.LOCAL_MEASUREMENT);t=PopupManager.text_for(x);self.assertIn('Type: Local Measurement',t);self.assertIn('Function: Fn',t);self.assertIn('Function description: Desc',t)
