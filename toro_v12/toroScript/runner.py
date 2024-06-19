import math, re

def copy(dict):
    obj={}
    dicList=list(dict.items())
    i=0
    while i < len(dicList):
        obj[dicList[i][0]]=dicList[i][1]
        i+=1
    return obj

def matchV(x,y):
    dicList=list(y.items())
    i=0
    while i < len(dicList):
        if(dicList[i][0] in list(x.keys())):
            x[dicList[i][0]]=dicList[i][1]
        i+=1

def runProgram(tree,stack):
    leaf=0
    trunk=tree[0]
    #print("...")
    #print(tree)
    branches=tree[1]
    
    if(trunk=="\n"):
        for branch in branches:
            runProgram(branch,stack)
            
    if(trunk=="funcion"):
        stack[branches[0][1]]=((branches[1],branches[2][1][0]))
        
    if(trunk=="condicion"):
            scope=copy(stack)
            cond=runProgram(branches[0],stack)
            if(cond==1):
                runProgram(branches[1],scope)
            matchV(stack,scope)
        ################
        
    if(trunk=="bucle"):
        scope=copy(stack)
        while(runProgram(branches[0],scope) == 1):# god no?
            runProgram(branches[1],scope)
        matchV(stack,scope)
        
    if(trunk=="mostrar"):
        print(runProgram(branches[0],stack))
    if(trunk=="="):
        a=branches[0][1]
        b=runProgram(branches[1],stack)
        stack[a]=b
        
    if(trunk=="number"):
        leaf=float(branches)
    if(trunk=="string"):
        leaf=branches
    if(trunk=="expr"):
        if(branches=="input"):
            leaf=input().strip()
            if re.match(r'[+|-]?[0-9]*\.[0-9]+', leaf) or re.match(r'[+|-]?[0-9]+',leaf):
                leaf=float(leaf)
        else:
            leaf=stack.get(branches)
            if(leaf==None):
                leaf="ERROR"
            if type(leaf) is tuple:#### TENGO UNA FUNCION
                scope={}
                runProgram(leaf[0],scope)
                leaf=runProgram(leaf[1],scope)
    if(trunk=="+"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a+b
    if(trunk=="*"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a*b
    if(trunk=="-"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a-b
    if(trunk=="/"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a/b
    if(trunk=="%"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a%b
    if(trunk=="^"):
        #print("xd")
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=pow(a,b)
    if(trunk=="mayor"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a>b
    if(trunk=="menor"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a<b
    if(trunk=="igual"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a==b
    if(trunk=="cos"):
        a=runProgram(branches[0],stack)
        #b=runProgram(branches[1],stack)
        leaf=math.cos(a)
    if(trunk=="sin"):
        a=runProgram(branches[0],stack)
        #b=runProgram(branches[1],stack)
        leaf=math.sin(a)
    if(trunk=="tan"):
        a=runProgram(branches[0],stack)
        #b=runProgram(branches[1],stack)
        leaf=math.tan(a)
    if(trunk=="atan"):
        a=runProgram(branches[0],stack)
        #b=runProgram(branches[1],stack)
        leaf=math.atan(a)
    if(trunk=="--"):
        a=runProgram(branches[0],stack)
        #b=runProgram(branches[1],stack)
        leaf=(-1)*a
    
    
    return leaf