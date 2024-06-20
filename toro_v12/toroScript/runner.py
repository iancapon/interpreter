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

def mult(a,b):
    if(type(a) is str and type(b) is float):
        b=int(b)
    elif(type(b) is str and type(a) is float):
        a=int(a)
    return a*b

def runProgram(tree,stack):
    leaf=0
    trunk=tree[0]
    branches=tree[1]
    
    if(trunk=="\n"):
        for branch in branches:
            runProgram(branch,stack)
            
    if(trunk=="subrutina"):
        stack[branches[0][1]]=((branches[1],branches[2][1][0]))

    if(trunk=="funcion"):
        stack[branches[0][1]]=[branches[1][1],branches[2],branches[3][1][0]]
        
    if(trunk=="condicion"):
            scope=copy(stack)
            cond=runProgram(branches[0],stack)
            if(cond==1):
                runProgram(branches[1],scope)
            matchV(stack,scope)
        
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

        elif(branches!="input"):
            leaf=stack.get(branches)
            if(leaf==None):
                leaf="ERROR"
            if type(leaf) is tuple:#### TENGO UNA SUB-RUTINA
                scope=copy(stack)
                runProgram(leaf[0],scope)
                leaf=runProgram(leaf[1],scope)
                matchV(stack,scope)
                

    if(trunk==":"):### EXPRESION CON ARGUMENTOS
        if(branches[0]=="input"):
            leaf="ERROR"
        elif(branches[0]!="input"):
            leaf=stack.get(branches[0][1])
            if(leaf==None):
                leaf="ERROR"
            if type(leaf) is list:#### TENGO UNA FUNCION
                scope=copy(stack)
                if type(leaf[0]) is list:### más de un argumento
                    varNames=(leaf[0])
                    varValues=(branches[1][1])
                    n=0
                    while n <  len(varNames):
                        scope[varNames[n][1]]=runProgram(varValues[n],stack)
                        n+=1#### argumento
                else:
                    scope[leaf[0]]=runProgram(branches[1],stack)#### argumento
                ##################
                runProgram(leaf[1],scope)#### programa
                leaf=runProgram(leaf[2],scope) #### retorno
                matchV(stack,scope)

    if(trunk=="+"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a+b
    if(trunk=="*"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=mult(a,b)
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