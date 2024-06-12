import re

def runNew(tree,stack):
    ret=0
    if(type(tree) is str):
        ret= tree ####### paso a float los valores puramente numericos
        if re.match(r"[.0-9]",ret) or (ret[0]=="-" and re.match(r"[.0-9]",ret[1:])):
            ret= float(tree)
    else:
        op=list(tree.keys())[0]
        li=tree.get(op)
        if(op=='\n'):
            for line in li:
                #print()########### bien encaminado
                runNew(line,stack)
        elif(op=="print"):
            #print(li[0])
            print(runNew(li[0],stack))
        ##############
              
        elif(op=="condicion"):
            cond=runNew(li[0],stack)
            if(cond==1):
                runNew(li[1],stack)
        ################
        elif(op=="bucle"):
            while(runNew(li[0],stack) == 1):# god no?
                runNew(li[1],stack)
        else:############ OPERACIONES BINARIAS
            a=runNew(li[0],stack)
            b=runNew(li[1],stack)
            if(op=="="):
                stack[a]=(b)
                ret="valor de "+str(b)+" asignado a variable "+a

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

