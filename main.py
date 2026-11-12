import json as J,os,urllib.request as u
V=(0,100,320,330,500,900,0);N=(-33,-31,-18,-14,14,18,31,33);K=(-17,-16,-15,-1,1,15,16,17);SL=((),(),(),(-17,-15,15,17),(-16,-1,1,16),K);M=100000
B=[0]*128;S=1;E=-1;U=[];D=0;L=40000;F=0
def st():
 global B,S,E,U;B=[0]*128;S=1;E=-1;U=[]
 for i,v in enumerate(map(int,'42356324')):B[i]=v;B[i+16]=1;B[i+96]=-1;B[i+112]=-v
st()
def at(q,y):
 for d in(15,17):
  t=q-y*d
  if not t&0x88 and B[t]==y:return 1
 for d in N:
  t=q+d
  if not t&0x88 and B[t]==2*y:return 1
 for d in K:
  t=q+d
  if not t&0x88 and B[t]==6*y:return 1
  while not t&0x88:
   p=B[t]
   if p:
    if p==5*y or p==(3*y if d*d in(225,289)else 4*y):return 1
    break
   t+=d
 return 0
def ic(y):
 for q in range(128):
  if not q&0x88 and B[q]==6*y:return at(q,-y)
 return 0
def gm(o=0):
 v=[]
 for q in range(128):
  if q&0x88:continue
  p=B[q]
  if not p or(p>0)!=(S>0):continue
  t=abs(p)
  if t==1:
   d=16*S;z=(S>0)*0x70;g=[];n=q+d
   if not n&0x88 and not B[n] and not o:
    g.append(n)
    if(q>>4)==1+5*(S<0):
     e=q+2*d
     if not B[e]:g.append(e)
   for dd in(d-1,d+1):
    e=q+dd
    if e&0x88:continue
    x=B[e]
    if x and(x>0)!=(S>0):g.append(e)
    elif e==E:g.append(e)
   for e in g:v+=[q|(e<<7)|(r<<14) for r in(5,4,3,2)] if(e&0x70)==z else[q|(e<<7)]
  else:
   for d in(N if t==2 else K if t==6 else SL[t]):
    e=q+d
    while not e&0x88:
     x=B[e]
     if x:
      if(x>0)!=(S>0):v.append(q|(e<<7))
      break
     if not o:v.append(q|(e<<7))
     if t%4==2:break
     e+=d
 return v
def mk(m):
 global S,E
 f=m&127;t=(m>>7)&127;r=(m>>14)&7;p=B[f];c=B[t];n=-1
 if abs(p)==1 and t==E:n=t-16 if S>0 else t+16;c=B[n]
 U.append((m,c,n,E))
 if n>=0:B[n]=0
 if p*p==36 and abs(t-f)==2:
  k=1 if t in(6,118) else -1;x=t+k;y=t-k;w=B[x];B[y]=w;B[x]=0
 if abs(p)==1 and abs(t-f)==32:E=(f+t)//2
 else:E=-1
 B[f]=0;B[t]=r*S if r else p;S=-S
 if ic(-S):um();return 0
 return 1
def um():
 global S,E
 m,c,n,e0=U.pop();f=m&127;t=(m>>7)&127;r=(m>>14)&7;S=-S;p=B[t];B[t]=0
 if p*p==36 and abs(t-f)==2:
  k=1 if t in(6,118) else -1;x=t+k;y=t-k;B[x]=B[y];B[y]=0
 B[f]=S if r else p
 if c:B[n if n>=0 else t]=c
 E=e0
def ev():
 s=0
 for q in range(128):
  p=B[q];t=abs(p)
  if p:s+=(V[t]+(6-abs((q&7)-3)-abs((q>>4)-3))*4)*(p//t)
 return s if S>0 else -s
def om(v):
 w=[]
 for m in v:
  f=m&127;t=(m>>7)&127;s=0;q=B[t]
  if q:s=10*V[abs(q)]-V[abs(B[f])]
  w.append((-s,m))
 return[m for _,m in sorted(w)]
def qs(a,b,y):
 global D,F;D+=1
 if D>=L:F=1;return 0
 c=ic(S);e=-M;n=0
 if not c:
  s=ev()
  if s>=b:return s
  e=s
  if s>a:a=s
 for m in om(gm(not c)):
  if not mk(m):continue
  n+=1;s=-qs(-b,-a,y+1);um()
  if F:return 0
  if s>e:e=s
  if s>=b:return s
  if s>a:a=s
 if c and not n:return -M+y
 return e
def sr(d,a,b,y):
 global D,F
 if d<=0:return qs(a,b,y)
 D+=1
 if D>=L:F=1;return 0
 c=ic(S);e=-M;z=0
 for m in om(gm()):
  if not mk(m):continue
  z+=1
  if d>=3 and z>3 and not c and not U[-1][1] and not(m>>14):
   s=-sr(d-2,-a-1,-a,y+1)
   if s>a:s=-sr(d-1,-b,-a,y+1)
  else:s=-sr(d-1,-b,-a,y+1)
  um()
  if F:return 0
  if s>e:e=s
  if s>a:a=s
  if a>=b:break
 if not z:return -M+y if c else 0
 return e
def rs():
 global D,L,F
 w=[]
 for m in gm():
  if mk(m):w.append(m);um()
 D=0;F=0;b=w[0];a=-M
 for m in om(w):
  mk(m);r=-sr(5,-M-1,M+1,1);um()
  if F:break
  if r>a:a=r;b=m
 return b
def uc(m):
 f=m&127;t=(m>>7)&127;r=(m>>14)&7
 return chr(97+f%8)+str(f//16+1)+chr(97+t%8)+str(t//16+1)+('nbrq'[r-2] if r else '')
def pu(x):
 f=ord(x[0])-97+(int(x[1])-1)*16;t=ord(x[2])-97+(int(x[3])-1)*16;r='nbrq'.index(x[4])+2 if len(x)==5 else 0
 return f|(t<<7)|(r<<14)
def cs(f,v,m=()):
 try:
  st()
  for x in m:mk(pu(x))
  y=uc(rs())
  if y in v:return y
 except:pass
 return v[0]
def po(x,p,b):return J.load(u.urlopen(u.Request(x+p,data=J.dumps(b).encode(),headers={'content-type':'application/json'})))
def mn():
 x=os.environ['MAKEFUN_ENV_URL']
 while 1:
  g=po(x,'/game',{})
  if g['status'][0]<'e':return
  while g['status'][0]=='y':g=po(x,'/move',{'game':g['game'],'move':cs(g['fen'],g['legal_moves'],g['moves'])})
if __name__=='__main__':mn()
