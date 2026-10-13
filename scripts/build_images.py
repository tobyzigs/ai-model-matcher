# Parses the Artificial Analysis text-to-image leaderboard (saved as markdown in data/img.md)
# into app/images.json. Usage: python3 -I scripts/build_images.py
import re,json,datetime
md=open('data/img.md').read()
rows=[]
for line in md.splitlines():
    m=re.match(r'^\| (\d+) \| [^|]* \| (.*?) \| (\d+)[^|]* \| ([\d,]+) \| ([^|]*) \| ([^|]*) \|$',line)
    if not m: continue
    cell=m.group(2)
    maker=re.search(r'!\[(.*?) logo\]',cell); maker=maker.group(1) if maker else ''
    name=cell.split('<br>',1)[-1]
    name=re.sub(r'\s*\[!\[.*$','',name).replace('\\[','[').replace('\\]',']').strip()
    pr=re.search(r'\$([\d.]+)\s*/1k',m.group(6))
    rows.append({"rank":int(m.group(1)),"name":name,"maker":maker.replace('SpaceXAI','xAI'),"elo":int(m.group(3)),
        "votes":int(m.group(4).replace(',','')),"released":m.group(5).strip(),
        "p1k":float(pr.group(1)) if pr else None,"open":'huggingface.co' in cell or 'github.com' in cell})
assert len(rows)>=50, len(rows)
json.dump({"updated":datetime.date.today().isoformat(),"source":"https://artificialanalysis.ai/image/leaderboard/text-to-image","models":rows},open('app/images.json','w'),indent=0)
print(len(rows),rows[0],rows[-1])
