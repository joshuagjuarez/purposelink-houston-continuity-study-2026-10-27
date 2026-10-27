#!/usr/bin/env python3
import hashlib,json,sys
from pathlib import Path
r=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve();m=json.loads((r/"SHA256SUMS.json").read_text());expected={x["path"] for x in m["files"]}|{"SHA256SUMS.json"};actual={p.relative_to(r).as_posix() for p in r.rglob("*") if p.is_file() and p.relative_to(r).parts[0] != ".git"};assert actual==expected,f"unmanifested/missing: {sorted(actual^expected)}"
for x in m["files"]:
 d=(r/x["path"]).read_bytes();assert len(d)==x["bytes"] and hashlib.sha256(d).hexdigest()==x["sha256"],x["path"]
code=(r/"scoring.py").read_bytes();assert hashlib.sha256(code).hexdigest()=="cf1dfec7c724c96a2f0741c12aa893c0b4c45582a30fafcccb4af25ae5418b5f";ns={};exec(compile(code,"scoring.py","exec"),ns);b=json.loads((r/"baseline24.json").read_text());returned=passes=0
for c in b["cells"]:
 assert hashlib.sha256(c["task_payload_exact"].encode()).hexdigest()==c["task_payload_sha256"] and json.loads(c["task_payload_exact"])==c["task_payload_parsed"]
 if c["raw_answer"] is None:assert c["recorded_score"] is None;continue
 returned+=1;got=ns["score"](c["raw_answer"],c);assert got==c["recorded_score"],c["cell_id"];passes+=got.get("pass") is True
assert (len(b["cells"]),returned,passes,sum(b["holds"].values()))==(24,19,2,5);e=json.loads((r/"engines.json").read_text());assert len(e["local_placements"])==7 and len(e["cloud"]["memex_sol_low"])==13;fam=json.loads((r/"family/family.json").read_text());assert len(fam["episodes"])==30 and len({(x["case_id"],x["horizon"]) for x in fam["episodes"]})==30;assert sum(1 for x in (r/"family/continuity-events.jsonl").read_text().splitlines() if x.strip())==30
print("PASS: recursive integrity/no extras; exact payload identity; exact scorer hash; 19 score replays; 2 passes; 5 holds; 7 local placements; 13 Sol; 30 real case/horizon pairs and events")
