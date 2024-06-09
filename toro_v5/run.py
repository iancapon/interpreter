import re

def run(tree,stack):
    ret=0
    if(type(tree) is str):
        ret= tree ####### paso a float los valores puramente numericos
        if re.match(r"[.0-9]",ret) or (ret[0]=="-" and re.match(r"[.0-9]",ret[1:])):
            ret= float(tree)
    else:
        op=list(tree.keys())[0]
        li=tree.get(op)
        a=run(li[0],stack)
        b=run(li[1],stack)
        if(op=="="):
            stack[a]=b
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
    return ret
