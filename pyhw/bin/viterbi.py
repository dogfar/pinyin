import json
import math
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

f=open('..\\src\\start_dict.txt','r',encoding='utf-8-sig')
start_dict=json.load(f)
f.close()

f=open('..\\src\\transition_dict.txt','r',encoding='utf-8-sig')
transition_dict=json.load(f)
f.close()

def getvalue(Dict,key):
	if not key in Dict:
		return 1e-40
	else:
		return Dict[key]
def getvalueplus(Dict,key1,key2):
	if not key1 in Dict:
		return 1e-200
	else:
		return getvalue(Dict[key1],key2)
def getpy_letter():
	infile=input()
	list_py=infile.split()
	return list_py

def getlist(key):
	return py2hz_dict[key]

def tryviterbi(List):
	if(len(List)==0):
		print('Invalid input!')
		return
	V=[{}]
	sd=start_dict['data']
	ed=emission_dict['data']
	td=transition_dict['data']
	prevlist=curlist=getlist(List[0])
	for state in curlist:
		score=math.log(max(getvalue(sd,state),start_dict['default']))+math.log(max(getvalue(ed[state],List[0]),emission_dict['default']))
		path=[state]
		V[0][state]=(score,path)
	for t in range(1,len(List)):
		V.append({})
		prevlist=curlist
		curlist=getlist(List[t])
		for state in curlist:
			idx=prevlist[0]
			score=-1e100
			for s0 in prevlist:
				score0=V[t-1][s0][0]+math.log(getvalueplus(td,s0,state))+math.log(getvalueplus(ed,state,List[t]))
				if score0>score:
					score=score0
					idx=s0
			newpath=V[t-1][idx][1].copy()
			newpath.append(state)
			V[t][state]=(score,newpath)
	return V

def solve(V):
	l=len(V)-1
	cnt=0
	for key in V[l]:
		if cnt==0:
			idx=key
			cnt+=1
		if V[l][key][0]>V[l][idx][0]:
			idx=key
	ans=V[l][idx][1]
	string="".join(ans)
	return string

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
	chinese=solve(tryviterbi(pyl))
	f.write(chinese+"\n")

file.close()
f.close()
