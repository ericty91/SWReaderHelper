import random,string,unittest
from pathlib import Path
from parser.function_index import FunctionIndexBuilder
class LocalFallbackTests(unittest.TestCase):
 def test_out_wins_and_local_is_fallback(self):
  idx=FunctionIndexBuilder().build((Path(__file__).parent/'fixtures'/'local_fallback.a2l').read_text())
  self.assertEqual(idx.measurements['Both_MP'].name,'OutFn');self.assertNotIn('Both_MP',idx.local_measurements);self.assertEqual(idx.local_measurements['LocalOnly_MP'].name,'LocalFn')
 def test_20000_generated_out_and_local_cases(self):
  rng=random.Random(9090);parts=[];expected_out={};expected_local={}
  for i in range(400):
   fn=f'Fn_{i}';desc=f'Description {i}';outs=[];locals_=[]
   for j in range(25):
    s=''.join(rng.choice(string.ascii_letters+string.digits+'_') for _ in range(8));o=f'Out_{i}_{j}_{s}';l=f'Loc_{i}_{j}_{s}';outs.append(o);locals_.append(l);expected_out[o]=(fn,desc);expected_local[l]=(fn,desc)
   parts+=['/begin FUNCTION',fn,f'"{desc}"','/begin OUT_MEASUREMENT',' '.join(outs),'/end OUT_MEASUREMENT','/begin LOC_MEASUREMENT',' '.join(locals_),'/end LOC_MEASUREMENT','/end FUNCTION']
  idx=FunctionIndexBuilder().build('\n'.join(parts));self.assertEqual(len(idx.measurements),10000);self.assertEqual(len(idx.local_measurements),10000)
  for n,v in expected_out.items():self.assertEqual((idx.measurements[n].name,idx.measurements[n].description),v)
  for n,v in expected_local.items():self.assertEqual((idx.local_measurements[n].name,idx.local_measurements[n].description),v)
