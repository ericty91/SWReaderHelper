import os,unittest
from pathlib import Path
from parser.function_index import FunctionIndexBuilder
class RealFileTests(unittest.TestCase):
 def test_supplied_file(self):
  p=Path(os.environ.get('SW_READER_TEST_A2L','/mnt/data/02Z5JK07A100.txt'))
  if not p.exists():self.skipTest('production file unavailable')
  idx=FunctionIndexBuilder().build(p.read_text(errors='replace'));self.assertEqual(len(idx.measurements),13420);self.assertGreater(len(idx.local_measurements),13000)
  self.assertEqual(idx.measurements['ACCI_aReq'].name,'ACCI_calcReq');self.assertEqual(idx.local_measurements['ACCI_bAccActvEdgeRiseLoc'].name,'ACCI_calcReq')
