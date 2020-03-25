import json
import math
import jieba
import sys

file=open('..\\src\\12.txt','r',encoding='utf-8-sig')
txt=file.read()
s={}
for i in range(0,len(txt)):
	s[i]=txt[i]
file.close()

f=open('..\\src\\py2hz.txt','r',encoding='utf-8-sig')
py2hz_dict=json.load(f)
f.close()

f=open('..\\src\\emission_dict.txt','r',encoding='utf-8-sig')
emission_dict=json.load(f)
f.close()

f=open('..\\src\\transition_dict.txt','r',encoding='utf-8-sig')
transition_dict=json.load(f)
f.close()

f=open('..\\src\\triple_transition_dict.txt','r',encoding='utf-8-sig')
triple_transition_dict=json.load(f)
f.close()

def getvalue(Dict,key):
	if not key in Dict:
		return 1e-40
	else:
		return Dict[key]
def getvalueplus(Dict,key1,key2):
	if not key1 in Dict:
		return 1e-40
	else:
		return getvalue(Dict[key1],key2)

def getvaluefortd2(Dict,key1,key2):
	if not key1 in Dict:
		return getvalueplus(transition_dict['data'],key1[1],key2)*1e-25
	else:
		if not key2 in Dict[key1]:
			return 0.1*getvalueplus(transition_dict['data'],key1[1],key2)
		else:
			return getvalueplus(Dict,key1,key2)

def getlist(key):
	return py2hz_dict[key]

td2=triple_transition_dict['data']

def prefer(waitinglist,pylist):
	finalans=[]
	preferpoint=0
	for i in range(0,len(waitinglist)):
		prob=waitinglist[i][0]
		ans="".join(waitinglist[i][1])
		l1=jieba.lcut(ans,cut_all=True)
		l2=jieba.lcut(ans,cut_all=False)
		jiebascore1=sum([len(seq) for seq in l1])/len(l1)
		jiebascore2=len(l2)
		le=max([len(seq) for seq in l1])
		preferscore=(prob+1.7*len(waitinglist)*jiebascore1-0.2*len(waitinglist)*jiebascore2)
		finalans.append((ans,prob,preferscore,preferpoint))
	f2=sorted(finalans,key=lambda elem:elem[2],reverse=True)
	return f2[0][0]

def tryviterbi(List):
	if(len(List)<2):
		print('Invalid input!')
		return
	V=[{},{}]
	ed=emission_dict['data']
	td=transition_dict['data']
	preprev=prevlist=getlist(List[0])
	curlist=getlist(List[1])
	for state in curlist:
		for s0 in prevlist:
			V[1][s0+state]=[]
			score=math.log(getvalueplus(td2,s0+state,'total'))+math.log(getvalueplus(transition_dict,s0,state))
			path=[s0,state]
			V[1][s0+state].append((score,path))

	for t in range(2,len(List)):
		V.append({})
		preprev=prevlist
		prevlist=curlist
		curlist=getlist(List[t])
		for state in curlist:
			fivelist=[]
			for s0 in prevlist:
				V[t][s0+state]=[]	
				qaqlist=[]
				for sp in preprev:
					for i in range(0,len(V[t-1][sp+s0])):
						score0=V[t-1][sp+s0][i][0]+math.log(getvaluefortd2(td2,sp+s0,state))+1.5*math.log(getvalueplus(ed,state,List[t]))
						path=V[t-1][sp+s0][i][1]
						qaqlist.append((path,sp+s0,score0))

				fivelist=sorted(qaqlist,key=lambda elem:elem[2],reverse=True)
				for i in range(0,min(5,len(fivelist))):
					newpath=fivelist[i][0].copy()
					newpath.append(state)
					V[t][s0+state].append((fivelist[i][2],newpath))
	return V	

def solve(V,List):
	s="Invalid Input"
	if len(pyl)<2:
		return s
	l=len(V)-1
	cnt=0
	decision=[]
	for key in V[l]:
		for item in V[l][key]:
			decision.append(item)

	sl=sorted(decision,key=lambda item:item[0],reverse=True)

	waitinglist=[]
	for i in range(0,min(5,len(sl))):
		waitinglist.append(sl[i])

	return prefer(waitinglist,List)

outputjiebainformation=jieba.lcut("我是很弱的蒟蒻",cut_all=False)
print("加载完毕！")

path1=sys.argv[1]
path2=sys.argv[2]
file=open(path1,'r',encoding='gbk')
f=open(path2,'w',encoding='gbk')
chinese=""
for line in file.readlines():
	line=line.replace("\n","")
	line=line.replace("qv","qu")
	line=line.replace("xv","xu")
	line=line.replace("jv","ju");
	line=line.lower()
	pyl=line.split()
	chinese=solve(tryviterbi(pyl),pyl)
	f.write(chinese+"\n")

file.close()
f.close()
