import re
import sys
from math import log

def parse2clsc(lscasm,lscasmf):
    err=0#set to 1 if a instruction has error
    #types of inst
    argn=["break","del","erase"]#no arg
    argi=["push"]#int
    argni=["add","find","hop","intp","cmp","mul","sub","div"]#no arg,int
    argns=["strp","asm"]#no arg,string
    argnil=["ret","jmp","jz"]#no arg,string,label
    argnid=["store"]#no arg,int,[int,int]
    #regex setup
    ren=re.compile('^\s*(#.*|)$')
    rei=re.compile('^\s*(\d+)\s*(#.*|)$')#first group
    res=re.compile('^\s*(["\'])((\\\\{2})*|(.*?[^\\\\](\\\\{2})*))\\1\s*(#.*|)$')#second group
    rel=re.compile('^\s*(\S+)\s*(#.*|)$')#first group
    red=re.compile('^\s*(\d+)\s*,\s*(\d+)\s*(#.*|)$')#first and second group
    #list of lines that may have an instruction
    lscasm=filter(lambda a: a != '', lscasm.split('\n'))
    for i in range(len(lscasm)):
        lscasm[i]=(lscasm[i].lstrip()+' ').split(' ',1)
        inst=lscasm[i][0].lower()
        arg=lscasm[i][1]
        if inst in argn:
            remn=ren.match(arg)
            if(remn):
                lscasm[i]=[inst]
            else:
                print("[Error] Line %d : "%(i)+inst+' '+arg)
                err=1
        elif inst in argi:
            remi=rei.match(arg)
            if(remi):
                lscasm[i]=[inst,[remi.group(1),'i']]
            else:
                print("[Error] Line %d : "%(i)+inst+' '+arg)
                err=1
        elif inst in argni:
            remn=ren.match(arg)
            remi=rei.match(arg)
            if(remn):
                lscasm[i]=[inst]
            elif(remi):
                lscasm[i]=[inst,[remi.group(1),'i']]
            else:
                print("[Error] Line %d : "%(i)+inst+' '+arg)
                err=1
        elif inst in argns:
            remn=ren.match(arg)
            rems=res.match(arg)
            if(remn):
                lscasm[i]=[inst]
            elif(rems):
                lscasm[i]=[inst,[rems.group(2),'s']]
            else:
                print("[Error] Line %d : "%(i)+inst+' '+arg)
                err=1
        elif inst in argnil:
            remn=ren.match(arg)
            remi=rei.match(arg)
            reml=rel.match(arg)
            if(remn):
                lscasm[i]=[inst]
            elif(remi):
                lscasm[i]=[inst,[remi.group(1),'i']]
            elif(reml):
                lscasm[i]=[inst,[reml.group(1),'l']]
            else:
                print("[Error] Line %d : "%(i)+inst+' '+arg)
                err=1
        elif inst in argnid:
            remn=ren.match(arg)
            remi=rei.match(arg)
            remd=red.match(arg)
            if(remn):
                lscasm[i]=[inst]
            elif(remi):
                lscasm[i]=[inst,[remi.group(1),'i']]
            elif(remd):
                lscasm[i]=[inst,[remd.group(1),'i'],[remd.group(2),'i']]
            else:
                print("[Error] Line %d : "%(i)+inst+' '+arg)
                err=1
        else:
            label=re.search("^\s*(\S*)\:\s*(#.*|)$",inst)
            remn=ren.match(arg)
            if(label and remn):
                lscasm[i]=['label',[label.group(1),'l']]
            else:
                print("[Error] Line %d : "%(i)+inst+' '+arg)
                err=1
        clscasmf=open(lscasmf+'.clscasm','w')
    if(err==1):
        return lscasm,err
    for i in lscasm:
        clscasmf.write(i[0]+'|')
        for j in i[1:]:
            clscasmf.write(j[0]+','+j[1]+'|')
        clscasmf.write('\n')
    clscasmf.close()
    return lscasm,err

def pushnum(n):#generates code that pushes n on the stack i think can optimise a bit?
    n=int(n)
    s=''
    t=0
    if(n<0):
        n=-n
        t=1
    if(n<9):
        return "a"+chr(0x61+n)+"S" if t==1 else chr(0x61+n)
    if(n%9!=0):
        s=chr(0x61+n%9)+"A" if n>8 else ""+s
    n/=9
    while(n>8):
        if(n%9==0):
            s="jM"+s
        else:
            s=chr(0x61+n%9)+"AjM"+s
        n/=9
    s=chr(0x61+n%9)+"jM"+s
    return "a"+s+"S" if t==1 else s

def parse2lsc(casm):
    lsc=[None]*len(casm)
    labels=[]
    #one to one translation 
    for i in range(len(casm)):
        if(len(casm[i])==1):
            if(casm[i][0]=="add"):
                lsc[i]="A"
            elif(casm[i][0]=="break"):
                lsc[i]="B"
            elif(casm[i][0]=="ret"):
                lsc[i]="C"
            elif(casm[i][0]=="del"):
                lsc[i]="D"
            elif(casm[i][0]=="erase"):
                lsc[i]="E"
            elif(casm[i][0]=="find"):
                lsc[i]="F"
            elif(casm[i][0]=="jmp"):
                lsc[i]="G"
            elif(casm[i][0]=="hop"):
                lsc[i]="H"
            elif(casm[i][0]=="intp"):
                lsc[i]="I"
            elif(casm[i][0]=="cmp"):
                lsc[i]="J"
            elif(casm[i][0]=="store"):
                lsc[i]="K"
            elif(casm[i][0]=="mul"):
                lsc[i]="P"
            elif(casm[i][0]=="strp"):
                lsc[i]="P"
            elif(casm[i][0]=="sub"):
                lsc[i]="S"
            elif(casm[i][0]=="div"):
                lsc[i]="V"
            elif(casm[i][0]=="jz"):
                lsc[i]="Z"
        elif(len(casm[i])==2):
            if(casm[i][0]=="push"):
                lsc[i]=pushnum(casm[i][1][0])
            elif(casm[i][0]=="add"):
                lsc[i]=pushnum(casm[i][1][0])+"A"
            elif(casm[i][0]=="ret"):
                if(casm[i][1][1]=='i'):
                    lsc[i]=pushnum(casm[i][1][0])+"C"
            elif(casm[i][0]=="find"):
                lsc[i]=pushnum(casm[i][1][0])+"F"
            elif(casm[i][0]=="jmp"):
                if(casm[i][1][1]=='i'):
                    lsc[i]=pushnum(casm[i][1][0])+"G"
            elif(casm[i][0]=="hop"):
                lsc[i]=pushnum(casm[i][1][0])+"H"
            elif(casm[i][0]=="intp"):
                lsc[i]=pushnum(casm[i][1][0])+"I"
            elif(casm[i][0]=="cmp"):
                lsc[i]=pushnum(casm[i][1][0])+"J"
            elif(casm[i][0]=="store"):
                lsc[i]=pushnum(casm[i][1][0])+"K"
            elif(casm[i][0]=="mul"):
                lsc[i]=pushnum(casm[i][1][0])+"M"
            elif(casm[i][0]=="strp"):
                lsc[i]=""
                for j in casm[i][1][0]:
                    lsc[i]+=pushnum(ord(j))+"P"
            elif(casm[i][0]=="sub"):
                lsc[i]=pushnum(casm[i][1][0])+"S"
            elif(casm[i][0]=="div"):
                lsc[i]=pushnum(casm[i][1][0])+"V"
            elif(casm[i][0]=="jz"):
                if(casm[i][1][1]=='i'):
                    lsc[i]=pushnum(casm[i][1][0])+"Z"
            elif(casm[i][0]=="asm"):
                lsc[i]=casm[i][1][0]
            elif(casm[i][0]=="label"):
                if(casm[i][1][0] in labels):
                    print "[Error] Duplicate label: "+casm[i][1][0]
                    return
                labels.append(casm[i][1][0])
                lsc[i]=''
        elif(len(casm[i])==3):
            if(casm[i][0]=="store"):
                lsc[i]=pushnum(casm[i][2][0])+pushnum(casm[i][1][0])+"K"

    #settling jumps and labels REALLY NOT OPTIMISED
    rjmpn=0
    instl=0
    for i in lsc:
        if(i==None):
            rjmpn+=1
        else:
            instl+=len(i)
    #instl+4*rjmpl*rjmpn<9**rjmpl
    rjmpl=int(log(instl)/log(9))+1
    while(instl+4*rjmpl*rjmpn>=9**rjmpl):
        rjmpl+=1#im lazy to newton rhapson lol
    rjmpl*=4
    ilen=0
    labellen=[]
    jmpslst=[]
    for i in range(len(lsc)):
        if(lsc[i]==None):
            ilen+=rjmpl
            jmpslst.append([i,ilen])
        elif(lsc[i]==''):
            labellen.append(ilen)
        else:
            ilen+=len(lsc[i])
    for i in jmpslst:
        if(casm[i[0]][0]=='ret'):
            lsc[i[0]]=pushnum(labellen[labels.index(casm[i[0]][1][0])])
            lsc[i[0]]+='n'*(rjmpl-len(lsc[i[0]])-1)
            lsc[i[0]]+='C'
        elif(casm[i[0]][0]=='jmp'):
            lsc[i[0]]=pushnum(labellen[labels.index(casm[i[0]][1][0])]-i[1])
            lsc[i[0]]+='n'*(rjmpl-len(lsc[i[0]])-1)
            lsc[i[0]]+='G'
        else:
            lsc[i[0]]=pushnum(labellen[labels.index(casm[i[0]][1][0])]-i[1])
            lsc[i[0]]+='n'*(rjmpl-len(lsc[i[0]])-1)
            lsc[i[0]]+='Z'
    return ''.join(lsc)

if(len(sys.argv)!=2):
    print("Format: python2 "+sys.argv[0]+" filename")
    exit()

lscasmf=sys.argv[1]
if(lscasmf[:-8]==".clscasm"):
    print "Invalid file"
    exit()

lscasm=open(lscasmf,'r').read()

casm,err=parse2clsc(lscasm,lscasmf)
if(err==1):
    exit()

lsc=parse2lsc(casm)
print lsc

