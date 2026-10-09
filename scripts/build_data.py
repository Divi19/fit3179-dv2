import openpyxl, csv, collections, json
import sys
SRC=(sys.argv[1] if len(sys.argv)>1 else "raw")+"/"   # folder holding the original .xlsx files (run from repo root)
OUT="data/"
YEARS=[2009,2012,2015,2018,2021,2024]
STATE_ABBR={'New South Wales':'NSW','Victoria':'VIC','Queensland':'QLD','South Australia':'SA','Western Australia':'WA','Tasmania':'TAS','Northern Territory':'NT','Australian Capital Territory':'ACT'}
RENAME={25250:24700}   # Moreland -> Merri-bek (code changed in ASGS 2023 LGA edition)

def num(v):
    if isinstance(v,(int,float)) and not isinstance(v,bool): return v
    if isinstance(v,str):
        s=v.strip()
        if s.startswith('≥'): return float(s[1:])        # bounded value: use the bound
        if s.startswith('≤'): return float(s[1:])
    return None

def rows(fn, sheet):
    wb=openpyxl.load_workbook(SRC+fn, data_only=True, read_only=True)
    ws=wb[sheet]; ws.reset_dimensions()
    return [list(r)+[None]*50 for r in ws.iter_rows(values_only=True)]

# ---------- 1. AEDC by council, long format (charts 1-4) ----------
cent={}
with open("scripts/centroids.csv") as f:
    for r in csv.DictReader(f): cent[int(r['LGA_CODE24'])]=(float(r['lon']),float(r['lat']))
out=[]; state=None
for r in rows("lga-2009-24.xlsx","LGA One or more")[6:]:
    b,c=r[1],r[2]
    if isinstance(b,str) and b in STATE_ABBR: state=STATE_ABBR[b]; continue
    if isinstance(b,(int,float)) and float(b).is_integer():
        code=RENAME.get(int(b),int(b))
        lon,lat=cent.get(code,(None,None))
        if lon is None: continue                    # Norfolk Island etc. (not on the map)
        for k,y in enumerate(YEARS):
            valid=num(r[3+k]); n=num(r[9+2*k]); pct=num(r[10+2*k])
            out.append(dict(lga_code=code,lga_name=c,state=state,year=y,
                            children_assessed=int(valid) if valid is not None else '',
                            vulnerable_n=int(n) if n is not None else '',
                            vulnerable_pct=round(pct,1) if pct is not None else '',
                            lon=lon,lat=lat))
with open(OUT+"aedc_lga.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print("aedc_lga.csv", len(out), "rows,", len({o['lga_code'] for o in out}), "councils")

# ---------- 2. State trends: summary indicators (chart 5) + national domains (chart 6) ----------
wb=openpyxl.load_workbook(SRC+"state-and-territory-trends-(2009-2024).xlsx", data_only=True, read_only=True)
SHORT={'Developmentally vulnerable on one or more domains':'Vulnerable on 1+ domains',
       'Developmentally vulnerable on two or more domains':'Vulnerable on 2+ domains',
       'Developmentally on track on five domains':'On track on all 5 domains'}
summ=[]; dom=collections.defaultdict(lambda:[0,0])
for sn in wb.sheetnames[1:]:
    st=sn.split('. ')[-1].split('_')[0].replace('Table 11.','').replace('Table 15.','').strip()
    ws=wb[sn]; ws.reset_dimensions(); label=None
    for r in ws.iter_rows(values_only=True):
        r=list(r)+[None]*20
        if r[0] not in (None,''): label=r[0]
        if 'summary' in sn.lower():
            if isinstance(r[1],int) and isinstance(r[3],(int,float)):
                summ.append(dict(state=st,year=r[1],indicator=SHORT[label],pct=round(r[3],1),n=r[2],children=r[4]))
        else:
            if isinstance(r[1],int) and isinstance(r[6],(int,float)) and isinstance(r[8],(int,float)):
                dom[(label,r[1])][0]+=r[6]; dom[(label,r[1])][1]+=r[8]
with open(OUT+"aedc_states.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(summ[0])); w.writeheader(); w.writerows(summ)
print("aedc_states.csv", len(summ), "rows; states:", sorted({s['state'] for s in summ}))
DSHORT={'Physical health and wellbeing':'Physical health','Social competence':'Social competence',
        'Emotional maturity':'Emotional maturity','Language and cognitive skills (school-based)':'Language & thinking',
        'Communication skills and general knowledge':'Communication'}
domrows=[dict(domain=DSHORT[l],domain_full=l,year=y,vulnerable_pct=round(100*n/t,1)) for (l,y),(n,t) in sorted(dom.items())]
with open(OUT+"aedc_domains_national.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(domrows[0])); w.writeheader(); w.writerows(domrows)
print("domains 2021/2024:", [(d['domain'],d['year'],d['vulnerable_pct']) for d in domrows if d['year'] in (2021,2024)])

# ---------- 3. SEIFA: most vs least disadvantaged, on track on five (chart 7) ----------
seifa=[]; nat=collections.defaultdict(lambda:[0,0]); state=None
for r in rows("seifa-2009-24.xlsx","SEIFA On track five"):
    b,c=r[1],r[2]
    if isinstance(b,str) and b in STATE_ABBR: state=STATE_ABBR[b]; continue
    if isinstance(c,str) and (c.startswith('Quintile 1') or c.startswith('Quintile 5')):
        q='Most disadvantaged' if c.startswith('Quintile 1') else 'Least disadvantaged'
        for k,y in enumerate(YEARS):
            valid=num(r[3+k]); n=num(r[9+2*k]); pct=num(r[10+2*k])
            if y in (2021,2024) and pct is not None:
                seifa.append(dict(area=state,group=q,year=y,on_track_pct=round(pct,1)))
                nat[(q,y)][0]+=n; nat[(q,y)][1]+=valid
for (q,y),(n,t) in nat.items():
    seifa.append(dict(area='Australia',group=q,year=y,on_track_pct=round(100*n/t,1)))
with open(OUT+"aedc_seifa.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(seifa[0])); w.writeheader(); w.writerows(seifa)
print("seifa national:", {k:round(100*v[0]/v[1],1) for k,v in nat.items()})

# ---------- 4. NNPAS guidelines met, by age (chart 8) ----------
def find(rs,label,start=0):
    for i,r in enumerate(rs[start:],start):
        if isinstance(r[0],str) and r[0].strip()==label: return i,r
    raise KeyError(label)
g1=rows("CPASSDC01–02.xlsx","Table 1.3_Proportions"); g2=rows("CPASSDC01–02.xlsx","Table 2.3_Proportions")
AGES=['5–8','9–11','12–14','15–17']
guid=[]
_,r=find(g1,'Met physical activity recommendation'); guid.append(dict(age_group='2–5',guideline='3+ hours of play a day',pct=r[3]))
_,r=find(g2,'Met physical activity recommendation')
for k,a in enumerate(AGES): guid.append(dict(age_group=a,guideline='60+ min of moderate–vigorous activity a day',pct=r[1+k]))
with open(OUT+"nnpas_activity_guideline.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(guid[0])); w.writeheader(); w.writerows(guid)
print("guideline:", [(x['age_group'],x['pct']) for x in guid])

# ---------- 5. NNPAS minutes of activity by sex (chart 9) ----------
t5=rows("CPASSDC04–05.xlsx","Table 5.1_Means")
mins=[]
for sex,block in (('Boys','Males aged 5–17 years'),('Girls','Females aged 5–17 years')):
    bi=[i for i,r in enumerate(t5) if r[1]==block][0]
    _,r=find(t5,'Total moderate or vigorous physical activity (incl. active transport)',bi)
    _,s=find(t5,'All days',bi+15)   # screen time "All days" row sits in the screen block
    for k,a in enumerate(AGES):
        mins.append(dict(sex=sex,age_group=a,activity_min=round(r[1+k].total_seconds()/60)))
with open(OUT+"nnpas_activity_minutes.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(mins[0])); w.writeheader(); w.writerows(mins)
print("minutes:", [(m['sex'],m['age_group'],m['activity_min']) for m in mins])

# ---------- 6. NNPAS sleep vs screens before bed (chart 10) ----------
t12=rows("CPASSDC12.xlsx","Table 12.3_Proportions")
hdr=t12[5]; col={str(h).replace('(c)','').replace('(b)',''):i for i,h in enumerate(hdr) if h}
_,scr=find(t12,'Undertook sedentary screen activity'); _,bed=find(t12,'Total with screen-based device located in bedroom')
_,slp=find(t5,'Total sleep on night before interview(f)')
sl=[]
for k,a in enumerate(AGES):
    m=round(slp[1+k].total_seconds()/60)
    sl.append(dict(age_group=a,order=k,screens_before_bed_pct=scr[col[a]],screen_in_bedroom_pct=bed[col[a]],sleep_min=m,sleep_label=f"{m//60}h {m%60:02d}m"))
with open(OUT+"nnpas_sleep_screens.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(sl[0])); w.writeheader(); w.writerows(sl)
print("sleep:", sl)

# ---------- 7. NNPAS free sugars (chart 11) ----------
n2=rows("NNPASDC02.xlsx","Table 2.1_Means Persons"); m2=rows("NNPASDC02.xlsx","Table 2.2_MoEs Persons")
hdr=n2[5]; _,fs=find(n2,'Free sugars'); _,fm=find(m2,'Free sugars')
sug=[]
for a,lab,grp in (('2–4','2–4 yrs','Children'),('5–11','5–11 yrs','Children'),('12–17','12–17 yrs','Children'),('18 years and over','Adults 18+','Adults')):
    i=hdr.index(a); sug.append(dict(age_group=lab,group=grp,free_sugars_pct=fs[i],moe=fm[i]))
with open(OUT+"nnpas_free_sugars.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(sug[0])); w.writeheader(); w.writerows(sug)
print("sugars:", sug)
