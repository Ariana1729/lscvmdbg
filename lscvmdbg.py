import sys

heap=[None]*0x1fff
stack=[]
ip=0
cycles=0
codelen=0

def execvminst(op):
    global heap,stack,ip,codelen
    if op=='A':#Add
        t=stack.pop()
        stack[-1]+=t
    elif op=='B':#Break
        ip=codelen-1#basically terminates program
    elif op=='C':#C? its basically a return
        ip=stack.pop()-1
    elif op=='D':#Delete
        stack.pop()
    elif op=='E':#Erase
        stack[-1]=0
    elif op=='F':#F? its basically getting the nth element on the stack
        t=stack.pop()
        stack.append(stack[-t-1])
    elif op=='G':#G? its basically a jump
        ip+=stack.pop()
    elif op=='H':#H? its like kinda a swop instruction?
        t=stack.pop()
        stack.append(stack.pop(-t-1))
    elif op=='I':#Integer print
        sys.stdout.write('%d'%(stack.pop()))
    elif op=='J':#J? basically compares top 2 elements and append result of comparison
        t=stack.pop()
        stack.append(cmp(stack.pop(),t))
    elif op=='K':#K? basically stores in the 'heap'
        t=stack.pop()
        heap[t]=stack.pop()
    elif op=='M':#Mul
        t=stack.pop()
        stack[-1]*=t
    elif op=='P':#Print
        sys.stdout.write(chr(stack.pop()%128))
    elif op=='R':#R? basically clears the stack and kills program
        stack=[]
        ip=codelen
    elif op=='S':#Sub
        t=stack.pop()
        stack[-1]-=t
    elif op=='V':#V? divide
        t=stack.pop()
        stack[-1]/=t
    elif op=='Z':#Z? conditional jump
        t=stack.pop()
        if(stack.pop()==0):
            ip+=t
    elif op=='a':
        stack.append(0)
    elif op=='b':
        stack.append(1)
    elif op=='c':
        stack.append(2)
    elif op=='d':
        stack.append(3)
    elif op=='e':
        stack.append(4)
    elif op=='f':
        stack.append(5)
    elif op=='g':
        stack.append(6)
    elif op=='h':
        stack.append(7)
    elif op=='i':
        stack.append(8)
    elif op=='j':
        stack.append(9)
    return

def pad(s,n):
    return s+' '*(n-len(s))

def lscasm(op):
    global ip
    s=''
    ilen=10
    if op=='A':
        if(len(stack)==0):
            s="Add"
        elif(len(stack)==1):
            s=pad("Add",ilen)+"# Add %d -> ?"%(stack[-1])
        else:
            s=pad("Add",ilen)+"# Add %d -> %d"%(stack[-1],stack[-1]+stack[-2])
    elif op=='B':
        s="Break"
    elif op=='C':
        if(len(stack)==0):
            s="Ret"
        else:
            s=pad("Ret",ilen)+"# Ret %d"%(stack[-1])
    elif op=='D':
        s="Del"
    elif op=='E':
        s="Erase"
    elif op=='F':
        if(len(stack)==0):
            s="Find"
        else:
            try:
                s=pad("Find",ilen)+"# Find %d -> %d"%(stack[-1],stack[-2-stack[-1]])
            except:
                s=pad("Find",ilen)+"# Find %d -> ?"%(stack[-1])
    elif op=='G':
        if(len(stack)==0):
            s="Jmp"
        else:
            s=pad("Jmp",ilen)+"# Jmp %d -> %d"%(stack[-1],ip+stack[-1]+1)
    elif op=='H':
        if(len(stack)==0):
            s="Hop"
        else:
            try:
                s=pad("Hop",ilen)+"# Hop %d -> %d"%(stack[-1],stack[-2-stack[-1]])
            except:
                s=pad("Hop",ilen)+"# Hop %d -> ?"%(stack[-1])
    elif op=='I':
        if(len(stack)==0):
            s="Intp"
        else:
            s=pad("Intp",ilen)+"# Intp %d"%(stack[-1])
    elif op=='J':
        if(len(stack)==0):
            s="Cmp"
        elif(len(stack)==1):
            s=pad("Cmp",ilen)+"# Cmp %d,? -> ?"%(stack[-1])
        else:
            s=pad("Cmp",ilen)+"# Cmp %d,%d -> %d"%(stack[-2],stack[-1],cmp(stack[-2],stack[-1]))
    elif op=='K':
        if(len(stack)==0):
            s="Store"
        elif(len(stack)==1):
            s=pad("Store",ilen)+"# Store ?,%d"%(stack[-1])
        else:
            s=pad("Store",ilen)+"# Store %d,%d"%(stack[-1],stack[-2])
    elif op=='M':
        if(len(stack)==0):
            s="Mul"
        elif(len(stack)==1):
            s=pad("Mul",ilen)+"# Mul %d -> ?"%(stack[-1])
        else:
            s=pad("Mul",ilen)+"# Mul %d -> %d"%(stack[-1],stack[-1]*stack[-2])
    elif op=='P':
        if(len(stack)==0):
            s="Strp"
        else:
            s=pad("Strp",ilen)+"# Strp "+chr(stack[-1]%128)
    elif op=='R':
        s="Kill"
    elif op=='S':
        if(len(stack)==0):
            s="Sub"
        elif(len(stack)==1):
            s=pad("Sub",ilen)+"# Sub %d -> ?"%(stack[-1])
        else:
            s=pad("Sub",ilen)+"# Sub %d -> %d"%(stack[-1],stack[-2]-stack[-1])
    elif op=='V':
        if(len(stack)==0):
            s="Div"
        elif(len(stack)==1):
            s=pad("Div",ilen)+"# Div %d -> ?"%(stack[-1])
        else:
            s=pad("Div",ilen)+"# Div %d -> %d"%(stack[-1],stack[-2]/stack[-1])
    elif op=='Z':#Z? conditional jump
        if(len(stack)==0):
            s="Jz"
        elif(len(stack)==1):
            s=pad("Jz",ilen)+"# Jz %d -> %d  "%(stack[-1],ip+stack[-1]+1)+"(? taken)"
        else:
            s=pad("Jz",ilen)+"# Jz %d -> %d  "%(stack[-1],ip+stack[-1]+1)+("(Taken)" if stack[-2]==0 else "(Not taken)")
    elif op=='a':
        s="Push 0"
    elif op=='b':
        s="Push 1"
    elif op=='c':
        s="Push 2"
    elif op=='d':
        s="Push 3"
    elif op=='e':
        s="Push 4"
    elif op=='f':
        s="Push 5"
    elif op=='g':
        s="Push 6"
    elif op=='h':
        s="Push 7"
    elif op=='i':
        s="Push 8"
    elif op=='j':
        s="Push 9"
    return s

def execvm(code,dbg):
    global ip,cycles,codelen
    codelen=len(code)
    stepnum=1
    breaks=[]
    hist='h'
    while(True):
        if(ip==codelen):
            break
        if(dbg):
            stepnum-=1
            if(ip in breaks):
                print("Hit breakpoint %d at %d"%(breaks.index(ip)+1,ip))
            while(stepnum==0 or ip in breaks):
                stepnum=0
                print("-"*45+"stack")
                for i in range(8):
                    if(len(stack)<=i):
                        print("%d - NIL"%(i))
                    else:
                        print("%d - %d"%(i,stack[-1-i]))
                print("-"*46+"code")
                for i in range(ip-4,ip+5):
                    if(i<0 or i>=codelen):
                        print("%d"%(i)+" "*(15-len(str(i)))+"NIL")
                    elif(i==ip):
                        print(">%d"%(i)+" <"+code[i]+">"+" "*(10-len(str(i)))+lscasm(code[i]))
                    else:
                        print("%d"%(i)+" <"+code[i]+">"+" "*(11-len(str(i)))+lscasm(code[i]))
                print("[-] Input debugger instructions")
                inp=raw_input()
                if(inp==''):
                    inp=hist
                else:
                    hist=inp
                inp=inp.lower()
                if(inp[0]=='b'):
                    if(inp[1]==' '):
                        try:
                            inp=int(inp[2:])
                            if(inp in breaks):
                                print("[-] Breakpoint has already been added")
                            elif(inp<0 or codelen<=inp):
                                print("[-] Breakpoint is outside of code and cannot be added")
                            else:
                                breaks.append(inp)
                                print("[-] Added breakpoint %d at %d"%(len(breaks),inp))
                        except:
                            print("[Error] Invalid format")
                    elif(inp[1]=='d'):
                        try:
                            inp=int(inp[2:])
                            if(inp in breaks):
                                breaks.remove(inp)
                                print("[-] Breakpoint removed")
                            else:
                                print("[Error] No breakpoint at %d"%(inp))
                        except:
                            print("[Error] Invalid format")
                    elif(inp[1]=='l'):
                        for i in range(len(breaks)):
                            print("Breakpoint %d at %d"%(i+1,breaks[i]))
                elif(inp=='c'):
                    print("[-] Continuing execution")
                    stepnum=-1
                    break
                elif(inp=='h'):
                    print("[-] Debugger instructions:")
                    print("b [num] - add breakpoint at [num]")
                    print("bd [num] - deletes breakpoint at [num]")
                    print("bl - list breakpoints")
                    print("c - Continue")
                    print("q - quits debugger")
                    print("s - Steps 1 instruction")
                    print("s [num] - Steps [num] instructions")
                    print("xc - Prints code")
                    print("xc [a] [b] - Prints code[a:b]")
                    print("xh - Prints locations of elemnts in heap")
                    print("xh [a] [b] - Prints heap[a:b]")
                    print("xi - Prints code as lscasm")
                    print("xi [a] [b] - Prints code[a:b] as lscasm")
                    print("xs - Prints whole stack")
                    print("xs [a] - Prints top [a] elements of stack")
                    print("xs [a] [b] - Prints top [b] element starting from [a]") 
                elif(inp=='q'):
                    print("[-] Debugger stopped")
                    return
                elif(inp[0]=='s'):
                    try:
                        if(inp[2:4]=='0x'):
                            stepnum=int(inp[4:])
                        else:
                            stepnum=int(inp[2:])
                    except:
                        stepnum=1
                    print("[-] Stepping %d instructions"%(stepnum))
                elif(inp[0]=='x'):
                    if(inp[1]=='c'):
                        if(len(inp)<3):
                            for i in range(len(code)):
                                print("%d"%(i)+" "*(8-len(str(i)))+code[i])
                        else:
                            inp=inp[2:].split(' ')
                            try:
                                inp[1]=int(inp[1])
                                inp[2]=int(inp[2])
                                if(inp[1]>inp[2]):
                                    print("[Error] Upper bound lower than lower bound, swopping both")
                                    inp[1]^=inp[2]
                                    inp[2]^=inp[1]
                                    inp[1]^=inp[2]
                                if(inp[2]>len(code)):
                                    print("[Error] Upper bound is too large, code length is (%d)"%(len(code)))
                                    inp[2]=len(code)
                                for i in range(inp[1],inp[2]):
                                    print("%d"%(i)+" "*(8-len(str(i)))+code[i])
                            except:
                                print("[Error] Invaid format")
                    elif(inp[1]=='h'):
                        if(len(inp)<3):
                            for i in range(len(heap)):
                                if(heap[i]!=None):
                                    print("heap[%d]=%d"%(i,heap[i]))
                        else:
                            inp=inp[2:].split(' ')
                            try:
                                inp[1]=int(inp[1])
                                inp[2]=int(inp[2])
                                if(inp[1]>inp[2]):
                                    print("[Error] Upper bound lower than lower bound, swopping both")
                                    inp[1]^=inp[2]
                                    inp[2]^=inp[1]
                                    inp[1]^=inp[2]
                                print(heap[inp[1]:inp[2]])
                            except:
                                print("[Error] Invaid format")
                    elif(inp[1]=='i'):
                        if(len(inp)<3):
                            for i in range(len(code)):
                                print("%d"%(i)+" <"+code[i]+">"+" "*(11-len(str(i)))+lscasm(code[i]))
                        else:
                            inp=inp[2:].split(' ')
                            try:
                                inp[1]=int(inp[1])
                                inp[2]=int(inp[2])
                                if(inp[1]>inp[2]):
                                    print("[Error] Upper bound lower than lower bound, swopping both")
                                    inp[1]^=inp[2]
                                    inp[2]^=inp[1]
                                    inp[1]^=inp[2]
                                if(inp[2]>len(code)):
                                    print("[Error] Upper bound is too large, code length is (%d)"%(len(code)))
                                    inp[2]=len(code)
                                for i in range(inp[1],inp[2]):
                                    print("%d"%(i)+" <"+code[i]+">"+" "*(11-len(str(i)))+lscasm(code[i]))
                            except:
                                print("[Error] Invaid format")

                    elif(inp[1]=='s'):
                        if(len(inp)<3):
                            print(stack)
                        else:
                            inp=inp[2:].split(' ')
                            try:
                                if(len(inp)<1):
                                    print(stack)
                                elif(len(inp)==2):
                                    print(stack[-1-int(inp[1]):-1])
                                else:
                                    print(stack[-1-int(inp[1])-int(inp[2]):-1-int(inp[1])])
                            except:
                                print("[Error] Invaid format")

        try:
            execvminst(code[ip])
        except Exception as e:
            print("[Segfault]")
            print(e)
            break
        ip+=1
        cycles+=1
        if(cycles>0x800000):
            print("[-] Too many cycles")
            break
        if(ip<0 or ip>codelen):
            print("[-] Instruction pointer out of bound, ip = %d"%(ip))
            break
    print("")
    print("[-] Prgram terminated")
    if(dbg):
        print("[-] IP = %d"%(ip))
    hist='h'
    while(dbg):
        print("[-] Input debugger instructions")
        inp=raw_input()
        if(inp==''):
            inp=hist
        else:
            hist=inp
        inp=inp.lower()
        if(inp=='h'):
            print("[-] Debugger instructions:")
            print("q - quits debugger")
            print("xc - Prints code")
            print("xc [a] [b] - Prints code[a:b]")
            print("xh - Prints locations of elemnts in heap")
            print("xh [a] [b] - Prints heap[a:b]")
            print("xi - Prints code as lscasm")
            print("xi [a] [b] - Prints code[a:b] as lscasm")
            print("xs - Prints whole stack")
            print("xs [a] - Prints top [a] elements of stack")
            print("xs [a] [b] - Prints top [b] element starting from [a]") 
        elif(inp=='q'):
            print("[-] Debugger stopped")
            return
        elif(inp[0]=='x'):
            if(inp[1]=='c'):
                if(len(inp)<3):
                    for i in range(len(code)):
                        print("%d"%(i)+" "*(8-len(str(i)))+code[i])
                else:
                    inp=inp[2:].split(' ')
                    try:
                        inp[1]=int(inp[1])
                        inp[2]=int(inp[2])
                        if(inp[1]>inp[2]):
                            print("[Error] Upper bound lower than lower bound, swopping both")
                            inp[1]^=inp[2]
                            inp[2]^=inp[1]
                            inp[1]^=inp[2]
                        if(inp[2]>len(code)):
                            print("[Error] Upper bound is too large, code length is (%d)"%(len(code)))
                            inp[2]=len(code)
                        for i in range(inp[1],inp[2]):
                            print("%d"%(i)+" "*(8-len(str(i)))+code[i])
                    except:
                        print("[Error] Invaid format")
            elif(inp[1]=='h'):
                if(len(inp)<3):
                    for i in range(len(heap)):
                        if(heap[i]!=None):
                            print("heap[%d]=%d"%(i,heap[i]))
                else:
                    inp=inp[2:].split(' ')
                    try:
                        inp[1]=int(inp[1])
                        inp[2]=int(inp[2])
                        if(inp[1]>inp[2]):
                            print("[Error] Upper bound lower than lower bound, swopping both")
                            inp[1]^=inp[2]
                            inp[2]^=inp[1]
                            inp[1]^=inp[2]
                        print(heap[inp[1]:inp[2]])
                    except:
                        print("[Error] Invaid format")
            elif(inp[1]=='i'):
                if(len(inp)<3):
                    for i in range(len(code)):
                        print("%d"%(i)+" <"+code[i]+">"+" "*(11-len(str(i)))+lscasm(code[i]))
                else:
                    inp=inp[2:].split(' ')
                    try:
                        inp[1]=int(inp[1])
                        inp[2]=int(inp[2])
                        if(inp[1]>inp[2]):
                            print("[Error] Upper bound lower than lower bound, swopping both")
                            inp[1]^=inp[2]
                            inp[2]^=inp[1]
                            inp[1]^=inp[2]
                        if(inp[2]>len(code)):
                            print("[Error] Upper bound is too large, code length is (%d)"%(len(code)))
                            inp[2]=len(code)
                        for i in range(inp[1],inp[2]):
                            print("%d"%(i)+" <"+code[i]+">"+" "*(11-len(str(i)))+lscasm(code[i]))
                    except:
                        print("[Error] Invaid format")

            elif(inp[1]=='s'):
                if(len(inp)<3):
                    print(stack)
                else:
                    inp=inp[2:].split(' ')
                    try:
                        if(len(inp)<1):
                            print(stack)
                        elif(len(inp)==2):
                            print(stack[-1-int(inp[1]):-1])
                        else:
                            print(stack[-1-int(inp[1])-int(inp[2]):-1-int(inp[1])])
                    except:
                        print("[Error] Invaid format")
    return

def init():
    global heap,stack,ip,cycles,codelen
    if(len(sys.argv)==2):
        code=open(sys.argv[1],'r').read()
    else:
        print("[-] Enter vm code")
        code=raw_input()
    print("[-] [R]unning or [D]ebugging code?")
    inp=raw_input()
    while True:
        debug=0
        if(inp=='D' or inp=='d'):
            debug=1
        execvm(code,debug)
        '''
        print("[-] Rerun? Y/N")
        inp=raw_input()
        while(inp=='Y' or inp=='y'):
            execvm(code,debug)
            print("[-] Rerun? Y/N")
            inp=raw_input()
        '''
        print("[-] Continue? Y/N")
        inp=raw_input()
        if(inp=='N' or inp=='n'):
            print("[-] Debugger stopped")
            break
        print("[-] Reuse code? Y/N")
        inp=raw_input()
        if(inp=='N' or inp=='n'):
            print("Enter vm code")
            code=raw_input()
        print("[R]unning or [D]ebugging code?")
        inp=raw_input()
        heap=[None]*8000
        stack=[]
        ip=cycles=0
    return

init()

