import re
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
def runNew(tree,stack):
    ret=0
    if(type(tree) is str):
        ret= tree ####### paso a float los valores puramente numericos
        if re.match(r"[.0-9]",ret) or (ret[0]=="-" and re.match(r"[.0-9]",ret[1:])):
            ret= float(tree)
        
    elif(type(tree) is tuple):
        ret = runNew(tree[1],stack)
        if(ret in stack):
            ret= stack[ret]
        elif(ret[0]=="expr"):
            ret="Error de scope"
    else:
        op=list(tree.keys())[0]
        li=tree.get(op)
        if(op=='\n'):
            for line in li:
                runNew(line,stack)
        elif op=="expr" or op=="number":
            ret= runNew(li[0],stack)
            if(ret in stack):
                ret= stack[ret]
        elif(op=="print"):
            print(runNew(li[0],stack))
        ##############
        elif(op=="condicion"):
            scope=copy(stack)
            cond=runNew(li[0],stack)
            if(cond==1):
                runNew(li[1],scope)
            matchV(stack,scope)
        ################
        elif(op=="bucle"):
            scope=copy(stack)
            while(runNew(li[0],scope) == 1):# god no?
                runNew(li[1],scope)
            matchV(stack,scope)
        else:############ OPERACIONES BINARIAS
            a=runNew(li[0],stack)
            b=runNew(li[1],stack)
            if(op=="="):
                stack[a]=(b)
                #ret="valor de "+str(b)+" asignado a variable "+a

            else:
                aa=stack.get(a)
                bb=stack.get(b)
                if(aa!=None):
                    a=aa
                if(bb!=None):
                    b=bb
                if(op=='+'):
                    ret=a+b
                if(op=='-'):
                    ret=a-b
                if(op=='*'):
                    ret=a*b
                if(op=='/'):
                    ret=a/b
                if(op=='^'):
                    ret=pow(a,b)
                if(op==":"):
                    ret=False
                    if(a==b):
                        ret=True
                if(op=="<"):
                    ret=False
                    if(a<b):
                        ret=True
                if(op==">"):
                    ret=False
                    if(a>b):
                        ret=True

    return ret

