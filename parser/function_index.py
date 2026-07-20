import re
from models import Function
from utils.category_regex import CategoryRegex
B=re.compile(r"^\s*/begin\s+(?P<k>\w+)\b(?P<t>.*)$",re.I);E=re.compile(r"^\s*/end\s+(?P<k>\w+)\b",re.I);T=re.compile(r'[^\s"]+');Q=re.compile(r'^\s*"((?:\\.|[^"\\])*)"')
class FunctionIndexes:
 def __init__(self,f,m,l,c):self.functions=f;self.measurements=m;self.local_measurements=l;self.characteristics=c
class FunctionIndexBuilder:
 def __init__(self):self.r=CategoryRegex()
 def build(self,text):
  fs={};ms={};ls={};cs={};inside=False;depth=0;header='';direct=[];rel=None;rd=-1;outs=[];locs=[];defs=[]
  def finish():
   nonlocal inside,direct,outs,locs,defs
   cand=[x for x in direct if x and not x.upper().startswith('FUNCTION_VERSION')];ht=T.findall(header)
   if ht:name=ht[0]
   elif cand:name=T.findall(cand.pop(0))[0]
   else:inside=False;return
   desc='Not available'
   if cand:
    q=Q.match(cand[0]);desc=q.group(1) if q else T.findall(cand[0])[0]
   f=Function(name,desc);fs[name]=f
   for x in outs:ms.setdefault(x,f)
   for x in locs:
    if x not in ms:ls.setdefault(x,f)
   for x in defs:cs.setdefault(x,f)
   inside=False;direct=[];outs=[];locs=[];defs=[]
  for raw in text.splitlines():
   line=raw.strip()
   if m:=B.match(line):
    k=m.group('k').upper()
    if not inside and k=='FUNCTION':inside=True;depth=1;header=m.group('t').strip();direct=[];outs=[];locs=[];defs=[];rel=None;continue
    if inside:
     depth+=1
     if k in {'OUT_MEASUREMENT','LOC_MEASUREMENT','DEF_CHARACTERISTIC'}:rel=k;rd=depth;self._add(m.group('t'),outs if k=='OUT_MEASUREMENT' else locs if k=='LOC_MEASUREMENT' else defs)
    continue
   if m:=E.match(line):
    if not inside:continue
    k=m.group('k').upper()
    if rel==k and depth==rd:rel=None
    depth-=1
    if k=='FUNCTION' and depth==0:finish()
    continue
   if not inside or not line:continue
   if rel:self._add(line,outs if rel=='OUT_MEASUREMENT' else locs if rel=='LOC_MEASUREMENT' else defs)
   elif depth==1:direct.append(line)
  if inside:finish()
  # OUT always wins globally over LOC.
  for x in tuple(ls):
   if x in ms:del ls[x]
  return FunctionIndexes(fs,ms,ls,cs)
 def _add(self,line,target):
  for x in T.findall(line):
   if self.r.function_reference_matches(x):target.append(x)
