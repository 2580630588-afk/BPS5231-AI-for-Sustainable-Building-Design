"""Local-only study interface. Start: python app/serve.py (no upload)."""
from pathlib import Path
import sys,json,pickle,math,urllib.parse
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import analyze
import numpy as np
from experiment import PRODUCTS,make_case,polygon,read_csv
with (ROOT/'results/surrogate.pkl').open('rb') as f:B=pickle.load(f)
ROWS=read_csv(ROOT/'results/simulation_results.csv')
EXTRA=ROOT/'results/final_validation/simulation_results.csv'
if EXTRA.exists():ROWS+=read_csv(EXTRA)
NONRECT=ROOT/'results/nonrect_daylight/simulation_results.csv'
GRID_AUDIT=[]
if NONRECT.exists():
 new=read_csv(NONRECT)
 ROWS += [r for r in new if r['group']=='nonrect_daylight']
 GRID_AUDIT=[r for r in new if r['group']=='nonrect_grid_audit']
THERMAL_ROWS=[r for r in ROWS if r['group'] not in ['sensitivity','zoning_check','daylight_application']]
def coverage(shape):
 groups={}
 for r in THERMAL_ROWS:
  if r['shape']!=shape:continue
  k=(r['group'],float(r['area']),float(r['orientation']),float(r['wwr']))
  groups[k]=dict(role=r['group'],area=k[1],orientation=k[2],wwr=k[3],training=r['group'].startswith('train'))
 return [groups[k] for k in sorted(groups)]
def predict(data):
 shape=data.get('shape','rect2');A=float(data.get('area',900));o=float(data.get('orientation',0));w=float(data.get('wwr',.4))
 valid=['rect1','rect1.5','rect2','rect3','rect4','rect5','L','Lwide','triangle','pentagon','hexagon','circle24']
 if shape not in valid or not all(math.isfinite(x) for x in [A,o,w]) or not 100<=A<=3000 or not 0<=o<360 or not .1<=w<=.8:raise ValueError('Choose a supported plan form, area 100–3000 m², orientation 0–359°, and WWR 0.1–0.8.')
 rr=[make_case(shape,A,o,w,p,d,'interface') for p in PRODUCTS for d in [0,.6]];X=np.array([analyze.features(r) for r in rr]);p=B['model'].predict(X);geo=B['scaler'].transform(X[:1,:12]);dist=float(B['nearest'].kneighbors(geo)[0][0,0]);warn=[]
 if A<600 or A>1200:warn.append('Area is outside the 600–1200 m² training range. Other areas have only discrete tests and do not establish general validity.')
 if w<.2 or w>.6:warn.append('WWR is outside the 20%–60% training range.')
 if shape=='rect5':warn.append('Aspect ratio 5:1 exceeds the rectangular training range and is an extrapolation.')
 if shape=='Lwide':warn.append('This wide-arm L is an external-test variant; its outline was not used for training.')
 if dist>B['distance_threshold']:warn.append('Geometry features are far from the training cases. Run a new simulation before relying on the result.')
 if not shape.startswith('rect') and A!=900:warn.append('Nonrectangular training uses only 900 m². Other areas have discrete external-test evidence only.')
 if any(v<=0 for v in p):warn.append('A nonphysical prediction occurred. Do not use it for selection; run a new simulation.')
 out=[]
 for r,v in zip(rr,p):
  exact=next((x for x in ROWS if x['shape']==shape and abs(float(x['area'])-A)<1e-6 and abs(float(x['orientation'])-o)<1e-6 and abs(float(x['wwr'])-w)<1e-6 and x['product']==r['product'] and float(x['shade'])==r['shade'] and x['group'] not in ['sensitivity','zoning_check','daylight_application']),None)
  light=next((x for x in ROWS if x['group'] in ['daylight_application','independent_daylight','nonrect_daylight'] and x['shape']==shape and float(x['area'])==A and float(x['orientation'])==o and float(x['wwr'])==w and x['product']==r['product'] and float(x['shade'])==r['shade']),None)
  audit=next((x for x in GRID_AUDIT if x['shape']==shape and float(x['area'])==A and float(x['orientation'])==o and float(x['wwr'])==w and x['product']==r['product'] and float(x['shade'])==r['shade']),None)
  out.append(dict(product=r['product'],shade=r['shade'],q=float(v),total=float(v*A),saving=float(p[0]-v),saving_pct=float(100*(p[0]-v)/p[0]) if p[0]>0 else None,simulation=float(exact['cooling_kwh_th_m2']) if exact else None,da300=float(light['da300_mean_pct']) if light else None,da300_fine=float(audit['da300_mean_pct']) if audit else None,daylight_points=int(light['daylight_points']) if light else None,u=r['u'],shgc=r['shgc'],vt=r['vt']))
 tested=coverage(shape);exact_count=sum(x['simulation'] is not None for x in out)
 evidence='All six options have matching simulations, so prediction error can be checked directly.' if exact_count==6 else 'This input combination has no matching simulation; only other conditions of the same form have test evidence.' if any(not x['training'] for x in tested) else 'This input combination has no direct validation and is an exploratory prediction.'
 light_note='Daylight values are matching simulation results; 50% is only the study screen.' if all(x['da300'] is not None for x in out) else 'No daylight data are available. Only cooling can be compared, so no overall best option can be identified.'
 if all(x['da300_fine'] is not None for x in out):
  light_note=f"Nonrectangular daylight uses an area-weighted 4 m grid ({out[0]['daylight_points']} points); values in parentheses are the 2 m grid audit. DA300 is a weighted mean of the time reaching 300 lux, not the fraction of floor area that complies. The 50% threshold is only the study screen."
  if any((x['da300']>=50)!=(x['da300_fine']>=50) for x in out):
   warn.append('Daylight feasibility changes with grid resolution for at least one option, so the current screen is not stable.')
  if shape=='Lwide':light_note+=' The L-shape still uses the SplitFlux approximation; a grid audit cannot replace ray tracing or measurements.'
 return dict(shape=shape,area=A,vertices=polygon(shape,A),model=B['selected'],distance=dist,threshold=B['distance_threshold'],warnings=warn,status=evidence,evidence=evidence,daylight_note=light_note,coverage=tested,options=out)
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  path=urllib.parse.urlparse(self.path)
  try:
   if path.path=='/api/predict':data={k:v[0] for k,v in urllib.parse.parse_qs(path.query).items()};body=json.dumps(predict(data),ensure_ascii=False).encode();mime='application/json; charset=utf-8'
   elif path.path in ['/','/index.html']:body=(ROOT/'app/index.html').read_bytes();mime='text/html; charset=utf-8'
   else:self.send_error(404);return
   self.send_response(200);self.send_header('Content-Type',mime);self.end_headers();self.wfile.write(body)
  except Exception as e:
   self.send_response(400);self.send_header('Content-Type','application/json; charset=utf-8');self.end_headers();self.wfile.write(json.dumps({'error':str(e)},ensure_ascii=False).encode())
 def log_message(self,*args):pass
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);parser.add_argument('--open-browser',action='store_true');args=parser.parse_args()
 server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
 url=f'http://127.0.0.1:{args.port}/'
 print(f'Open {url} ; Ctrl+C to stop. Local only.',flush=True)
 if args.open_browser:
  import webbrowser
  webbrowser.open(url)
 server.serve_forever()
