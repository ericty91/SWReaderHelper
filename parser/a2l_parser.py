import re
from pathlib import Path
from models import *
from parser.block_reader import BlockReader
from parser.function_index import FunctionIndexBuilder
INLINE=re.compile(r'^\s*SYSTEM_CONSTANT\s+"([^"]+)"\s+"([^"]*)"')
class A2LParser:
 def __init__(self,logger):self.log=logger;self.reader=BlockReader();self.functions=FunctionIndexBuilder()
 def parse(self,path,progress=None):
  raw=Path(path).read_bytes()
  for enc in ('utf-8-sig','cp1252','latin-1'):
   try:text=raw.decode(enc);break
   except UnicodeDecodeError:pass
  idx=self.functions.build(text);db=A2LDatabase(functions_by_name=idx.functions,measurement_function_by_name=idx.measurements,local_measurement_function_by_name=idx.local_measurements,characteristic_function_by_name=idx.characteristics);methods={};pm=[];pc=[];blocks=list(self.reader.walk(self.reader.read(text)));total=max(1,len(blocks))
  for i,b in enumerate(blocks,1):
   t=self.reader.all_tokens(b)
   if b.kind=='COMPU_METHOD' and t:methods[t[0]]=t[4] if len(t)>4 and t[4] else 'Unknown'
   elif b.kind=='MEASUREMENT' and len(t)>3:pm.append((t[0],t[1],t[3]))
   elif b.kind=='CHARACTERISTIC' and len(t)>6:pc.append((t[0],t[1],t[6]))
   elif b.kind=='SYSTEM_CONSTANT' and len(t)>1:db.system_constants_by_name[t[0]]=SystemConstant(t[0],t[1])
   elif b.kind=='MOD_PAR':
    for line in b.body:
     if m:=INLINE.match(line):db.system_constants_by_name[m.group(1)]=SystemConstant(m.group(1),m.group(2))
   if progress and i%1000==0:progress(int(i*100/total))
  for n,d,m in pm:
   f=idx.measurements.get(n);local=False
   if f is None:f=idx.local_measurements.get(n);local=f is not None
   db.measurements_by_name[n]=Measurement(n,d or 'Description not available',methods.get(m,'Unknown'),f.name if f else 'Not available',f.description if f else 'Not available',m,ObjectType.LOCAL_MEASUREMENT if local else ObjectType.MEASUREMENT)
  for n,d,m in pc:
   f=idx.characteristics.get(n);db.characteristics_by_name[n]=Characteristic(n,d or 'Description not available',methods.get(m,'Unknown'),f.name if f else 'Not available',f.description if f else 'Not available',m)
  if progress:progress(100)
  return db
