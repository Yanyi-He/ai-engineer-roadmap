"""Guard against company boilerplate counting as a qualification."""
import hashlib,unittest
from scripts.extract_keywords import extract,features

class SectionTests(unittest.TestCase):
 def setUp(self):
  self.body='Our company uses Python. Duties: integrate APIs. Qualifications: SQL or Java.'
  a=self.body.index('Duties:');b=self.body.index('Qualifications:')
  self.record={'jd_id':'T1','body_sha256':hashlib.sha256(self.body.encode()).hexdigest(),'sections':[{'label':label,'start':start,'end':end,'sha256':hashlib.sha256(self.body[start:end].encode()).hexdigest()} for label,start,end in [('responsibilities',a,b),('qualifications',b,len(self.body))]]}
 def test_excludes_intro_and_preserves_sections(self):
  out=extract([{'jd_id':'T1','body':self.body}],[self.record])[0]
  self.assertFalse(out['features']['python'])
  self.assertTrue(out['section_features']['responsibilities']['http_apis_integrations'])
  self.assertTrue(out['section_features']['qualifications']['sql_databases'])
 def test_refuses_changed_body(self):
  with self.assertRaisesRegex(ValueError,'Body hash mismatch'):extract([{'jd_id':'T1','body':self.body+' altered'}],[self.record])
 def test_refuses_tampered_section(self):
  self.record['sections'][0]['start']+=1
  with self.assertRaisesRegex(ValueError,'Section hash mismatch'):extract([{'jd_id':'T1','body':self.body}],[self.record])
 def test_mixed_chinese_english_boundaries(self):
  result=features('熟悉Python开发，掌握MCP协议及LangGraph框架。')
  self.assertTrue(result['python'])
  self.assertTrue(result['mcp'])
  self.assertTrue(result['langgraph'])
  self.assertFalse(features('Pythonic style')['python'])

if __name__=='__main__':unittest.main()
