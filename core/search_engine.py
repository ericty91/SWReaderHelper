from utils.category_regex import CategoryRegex
class SearchEngine:
 def __init__(self,db,logger):self.db=db;self.r=CategoryRegex()
 def find(self,key):
  for valid,index in ((self.r.measurement_matches,self.db.measurements_by_name),(self.r.characteristic_matches,self.db.characteristics_by_name),(self.r.system_constant_matches,self.db.system_constants_by_name)):
   if valid(key) and (result:=index.get(key)):return result
  return None
