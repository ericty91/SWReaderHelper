import re
from dataclasses import dataclass,field
B=re.compile(r"^\s*/begin\s+(\w+)\b(.*)$",re.I);E=re.compile(r"^\s*/end\s+(\w+)\b",re.I);C=re.compile(r"/\*.*?\*/",re.S);T=re.compile(r'"((?:\\.|[^"\\])*)"|(\S+)')
@dataclass(slots=True)
class Block:kind:str;header:str;body:list[str];line:int;children:list['Block']=field(default_factory=list)
class BlockReader:
 def read(self,text):
  roots=[];stack=[]
  for n,line in enumerate(C.sub('',text).splitlines(),1):
   if m:=B.match(line):x=Block(m.group(1).upper(),m.group(2).strip(),[],n);(stack[-1].children if stack else roots).append(x);stack.append(x)
   elif m:=E.match(line):
    if stack and stack[-1].kind==m.group(1).upper():stack.pop()
   elif stack:stack[-1].body.append(line.strip())
  return roots
 def walk(self,roots):
  s=list(reversed(roots))
  while s:x=s.pop();yield x;s.extend(reversed(x.children))
 @staticmethod
 def tokens(lines):
  o=[]
  for line in lines:
   for m in T.finditer(line):q,p=m.groups();o.append(q if q is not None else p)
  return o
 def all_tokens(self,x):return self.tokens([x.header,*x.body])
