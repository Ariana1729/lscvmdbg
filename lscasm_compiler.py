import re
import sys

def parse(lscasm,lscasmf):
    err=0#set to 1 if a instruction has error
    #types of inst
    argn=["break","del","erase"]#no arg
    argi=["push"]#int
    argni=["add","find","hop","intp","cmp","mul","sub","div"]#no arg,int
    argns=["strp"]#no arg,string
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
                lscasm[i]=[inst,remi.group(1)]
            else:
                print("[Error] Line %d : "%(i)+inst+' '+arg)
                err=1
        elif inst in argni:
            remn=ren.match(arg)
            remi=rei.match(arg)
            if(remn):
                lscasm[i]=[inst]
            elif(remi):
                lscasm[i]=[inst,remi.group(1)]
            else:
                print("[Error] Line %d : "%(i)+inst+' '+arg)
                err=1
        elif inst in argns:
            remn=ren.match(arg)
            rems=res.match(arg)
            if(remn):
                lscasm[i]=[inst]
            elif(rems):
                lscasm[i]=[inst,rems.group(2)]
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
                lscasm[i]=[inst,remi.group(1)]
            elif(reml):
                lscasm[i]=[inst,reml.group(1)]
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
                lscasm[i]=[inst,remi.group(1)]
            elif(remd):
                lscasm[i]=[inst,remd.group(1),remd.group(2)]
            else:
                print("[Error] Line %d : "%(i)+inst+' '+arg)
                err=1
        clscasmf=open(lscasmf+'.clscasm','w')
    for i in lscasm:
        for j in i:
            clscasmf.write(j)
            clscasmf.write('|')
        clscasmf.write('\n')
    clscasmf.close()
    return err

if(len(sys.argv)!=2):
    print("Format: python2 "+sys.argv[0]+" filename")
    exit()
lscasmf=sys.argv[1]
if(lscasmf[:-8]==".clscasm"):
    print "Invalid file"
    exit()

lscasm=open(lscasmf,'r').read()
print parse(lscasm,lscasmf)
