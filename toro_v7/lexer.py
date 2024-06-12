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
            elif i==0:
                nfAux(tokens,i)
                i+=5
        i+=1
    #print(i)

def typeofchr(c):
    type=""
    if c in "0123456789.":
        type="number"
    elif c in "+-*/^":
        type="ope"
    elif c in "()":
        type="par"
    elif c in "#":
        type="comm"
    elif c in "\n":
        type="line"
    elif c in "=":
        type="equal"
    else:
        type="chr"
    #print((c,type))
    return type

def newLexer(text):
    chr=list(text)
    # TERMINA CON \N 
    if(chr[len(chr)-1]!='\n'):
        chr.append("\n")
    #ANULA LINEAS CON #
    i=0
    while i < len(chr):
        if(chr[i] == "#"):
            j=i
            while j < len(chr) and chr[j]!="\n":
                j+=1
            del chr[i:j]################## DE MOMENTO ESTÁ BIEN
            #i-=1
        i+=1
    tokens=[]
    #BUSCA PRIMER CARACTER VALIDO
    i=0
    word=chr[0]
    while chr[i] in " \n":
        i+=1
        word=chr[i]
    i+=1
    # ARMA LAS PALABRAS
    while i < len(chr):
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

    '''while i < len(tokens):
        if('\n' in tokens[i]):
            del tokens[i]
            i-=1
        else:
            break
        i+=1
    '''
    i=0
    #junta los \n\n en uno solo y los aledaños los elimina
    i=1
    while i < len(tokens):
        if('\n' in tokens[i]):
            tokens[i]='\n'
        if(tokens[i]=='\n' and tokens[i-1]=='\n'):
            del tokens[i]
            i-=1
        i+=1
    #print(tokens)
    # ARMA LOS TOKENS CON TIPO DE VALOR (FUNCIONES SON STRINGS DE MOMENTO)
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
    
    #negativeFix(items) ### DE MOMENTO ANDA ESTA NEGRADA
    #print(items)

    i=0
    while i< len(items):
        word=items[i][1]
        if word=="mostrar":####################### NEGRADA MAL PERO ANDA
            items.insert(i+1,("operation","+"))
            items.insert(i+1,("number","0"))
            i+=1
        i+=1
    
    i=0
    while i< len(items):
        word=items[i][1]
        if(word=="mayor" or word=="menor" or word=="igual"):
            
            if(word=="mayor"):
                items[i]=("operation",">")
            elif(word=="menor"):
                items[i]=("operation","<")
            elif(word=="igual"):
                items[i]=("operation",":")
        i+=1
    
    return items

