"""Transparent strict content-and-time scoring; offline answers never establish custody."""
import json

def score(text,cell):
 out={'status':'INVALID_RESPONSE','fact_content_and_time':[],'handoff_valid':False,'custody':'NOT_ESTABLISHED_BY_SCORER'}
 if not isinstance(text,str) or not text.strip():return dict(out,reason='EMPTY')
 if len(text.encode())>8192:return dict(out,reason='OVERSIZE')
 try:value=json.loads(text)
 except (ValueError,TypeError):return dict(out,reason='NON_JSON_OR_TRUNCATED')
 if type(value) is not dict or set(value)-{'observations','handoff','unknown'}:return dict(out,reason='RESPONSE_SCHEMA')
 if any(type(value.get(k)) is not list for k in ('observations','handoff','unknown')):return dict(out,reason='RESPONSE_SCHEMA')
 if any(type(x) is not str for x in value['unknown']):return dict(out,reason='UNCERTAINTY_SCHEMA')
 if any(type(x) is not dict or set(x)!={'to','fact_id','content','source_session'} or type(x['source_session']) is not int for x in value['handoff']):return dict(out,reason='HANDOFF_SCHEMA')
 rows=value['observations'];valid=lambda x:type(x) is dict and set(x)=={'fact_id','content','source_session'} and type(x['source_session']) is int
 if not all(valid(x) for x in rows):return dict(out,reason='OBSERVATION_SCHEMA')
 gt=cell['ground_truth'];expected=gt['expected']
 out['fact_content_and_time']=[{'fact_id':e['fact_id'],'matched':e in rows,'expected_content':e['content'],'expected_source_session':e['source_session']} for e in expected]
 allowed=cell['source']['current']+cell['source']['retained']+[{k:f[k] for k in ('fact_id','content','source_session')} for f in cell['source']['incoming']]
 out['unsupported_observations']=[x for x in rows if x not in allowed]
 out['stale_assertions']=[x for x in rows if any(x.get('fact_id')==f['fact_id'] or x.get('content')==f['content'] for f in gt['forbidden_stale'])]
 out['forbidden_content']=[s for s in gt['forbidden_content'] if s.casefold() in text.casefold()]
 valid_handoff=[]
 for x in value['handoff']:
  valid_handoff.append(type(x) is dict and set(x)=={'to','fact_id','content','source_session'} and any(x['to']==h['to'] and x['fact_id'] in h['fact_ids'] for h in gt['handoff']) and {k:x[k] for k in ('fact_id','content','source_session')} in allowed)
 required=[(h['to'],f) for h in gt['handoff'] for f in h['fact_ids']]
 out['handoff_valid']=all(valid_handoff) and all(any(x.get('to')==to and x.get('fact_id')==f and valid_handoff[i] for i,x in enumerate(value['handoff'])) for to,f in required)
 out['status']='SCORED_CONTENT';out['pass']=all(x['matched'] for x in out['fact_content_and_time']) and not out['unsupported_observations'] and not out['stale_assertions'] and not out['forbidden_content'] and out['handoff_valid']
 out['interpretation']='Observed task performance; disabled history can legitimately produce missing retained facts. Exact-quote contract, not semantic paraphrase scoring.'
 return out
