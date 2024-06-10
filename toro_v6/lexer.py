import re
def nfAux(tokens,i):
    del tokens[i]
    tokens.insert(i,("operation","*"))
    tokens.insert(i,("parentesis",")"))
    tokens.insert(i,("number","1"))
    tokens.insert(i,("operation","-"))
    tokens.insert(i,("number","0"))
    tokens.insert(i,("parentesis","("))

def negativeFix(tokens):
    i=0
    while i< len(tokens):
        #print(tokens[i])
        if(tokens[i][1]=="-"):
            if(i>0):
                if(tokens[i-1][0]!="number" or tokens[i-1][0]!="string"):
                    nfAux(tokens,i)
                    i+=5
                elif(tokens[i-1][0]=="string" and tokens[i-1][1]=="aver"):
                    nfAux(tokens,i)
                    i+=5
            else:
                nfAux(tokens,i)
                i+=5
        i+=1

def lineFix(chr):
    if(chr[len(chr)-1]!='\n'):
        chr.append("\n")

def typeofchr(c):
    type=""
    if c in "0123456789.":
        type="number"
    elif c in "+-*/=^":
        type="ope"
    elif c in "()":
        type="par"
    elif c in "#":
        type="comm"
    elif c in "\n":
        type="line"
    else:
        type="chr"
    #print((c,type))
    return type

def newLexer(text):
    chr=list(text)
    lineFix(chr)
    tokens=[]
    i=0
    word=chr[0]
    while chr[i]==" ":
        i+=1
        word=chr[i]
    i+=1

    while i < len(chr):
        #word=chr[i]
        if(chr[i]!=' '):
            if(typeofchr(chr[i])==typeofchr(chr[i-1])):
                word+=chr[i]
            else:
                if(len(word)>=1):
                    tokens.append(word)
                word=chr[i]
        if chr[i]==' ':
            if(len(word)>0 and " " not in word):
                tokens.append(word)
            word=""
        i+=1
    if(len(word)>=1):
        tokens.append(word)
    
    i=0
    while i < len(tokens):
        if(tokens[i] in "#"):
            st=i
            while i < len(tokens) and tokens[i]!="\n":
                i+=1
            del tokens[st:i+1]################################ OJO ACÁ PUEDE ESTAR MAL
        i+=1
    
    items=[]
    i=-1
    for word in tokens:
        i+=1
        if len(word)>0:
            if re.match(r"[.0-9]",word):
                items.append(("number",word))
            elif word in "+-*/=^":
                items.append(("operation",word))
            elif word in "()":
                items.append(("parentesis",word))
            elif word in "\n":
                items.append(("line",word))
            else:
                items.append(("string",word))
    '''
    negativeFix(items) ### ESTO NO ANDA xdddd muy sofisticado en una funcion y todo pero nada bobo
    '''
    

    i=0
    while i< len(items):
        word=items[i][1]
        if word=="aver":####################### NEGRADA MAL PERO ANDA
            items.insert(i+1,("operation","+"))
            items.insert(i+1,("number","0"))
            i+=1
        i+=1
    
    
    return items

