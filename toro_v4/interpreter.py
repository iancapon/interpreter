import re
#from parser_modules import *

def lexer(text):
    tokens=text.split(" ")
    items=[]
    for word in tokens:
        if re.match(r"[.0-9]",word) or (word[0]=="-" and re.match(r"[.0-9]",word[1:])):
            items.append(("number",word))
        elif word in "+-*/=^":
            items.append(("operation",word))
        else:
            items.append(("variable",word))
    return items

def my_bind(op,tokens):#v2
    if(op in "+-*/^="):
        i=0
        j=0
        newTokens=[]
        while i< len(tokens):
            if type(tokens[i]) is tuple:
                if(tokens[i][0]=='operation' and tokens[i][1]==op):
                    prev=newTokens[j-1]
                    nextt=tokens[i+1]
                    if(type(prev) is tuple):
                        prev=prev[1]
                    if(type(nextt) is tuple):
                        nextt=nextt[1]
                    #######
                    di={op:[prev,nextt]}
                    
                    newTokens.pop()
                    newTokens.append(di)
                    i+=2
                else:
                    newTokens.append(tokens[i])
                    i+=1
                    j+=1
            else:
                newTokens.append(tokens[i])
                i+=1
                j+=1
        tokens.clear()
        for word in newTokens:
            tokens.append(word)

def my_parser(tokens):#### operadores binarios
    my_bind("^",tokens)
    my_bind("/",tokens)
    my_bind("*",tokens)
    my_bind("-",tokens)
    my_bind("+",tokens)
    my_bind("=",tokens)
    return tokens[0]

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

def main():
    stack={}
    print("0 to exit > ",end="")
    text=input()
    while(text!="0"):
        tokenArray=lexer(text)
        if(tokenArray[0][1]=="print"):###### TEMPORARIO
            tokenArray.remove(tokenArray[0])
            tokenArray.append(("operation","+"))
            tokenArray.append(("number","0"))
        tree=my_parser(tokenArray)
        #print(tree)
        print(run(tree,stack))
        print("0 to exit > ",end="")
        text=input()
main()