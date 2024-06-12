import re

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
    apostrCount=0
    while i < len(chr):
        if(chr[i]!=' '):
            if(typeofchr(chr[i])==typeofchr(chr[i-1])):
                word+=chr[i]
            else:
                if(len(word)>=1):
                    tokens.append(word)
                word=chr[i]
            if(chr[i]=='"'):
                apostrCount+=1
        if chr[i]==' ':
            if(apostrCount%2==0):
                if(len(word)>0 and " " not in word):
                    tokens.append(word)
                word=""
            if(apostrCount%2==1):
                word+=chr[i]
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
            elif word in "+-*/=^" :#'''or word=="mayor" or word=="menor" or word=="igual"''':
                items.append(("operation",word))
            elif word in "()":
                items.append(("parentesis",word))
            elif word in "\n":
                items.append(("line",word))
            else:
                if(word[0]=='"'):
                    items.append(("string",word[1:-1]))
                else:
                    items.append(("expr",word))
    
    #negativeFix(items) ### DE MOMENTO ANDA ESTA NEGRADA
    #print(items)
    reserved=["mostrar","condicion","bucle","cerrar"]
    i=0
    while i< len(items):
        if(items[i][0]=="expr" and items[i][1] in reserved):
            items[i]=("action",items[i][1])
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
    
    #print(items)
    return items

