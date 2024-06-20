def tipo(c):
    if(c in "0123456789."):
        return "number"
    elif(c in "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ_"):
        return "letter"
    elif(c==' '):
        return "space"
    elif(c in "+-*/^%@!<>:=,"):
        return "ope"
    elif(c in "()"):
        return "par"
    elif(c in '"'):
        return "uppCommas"
    else:
        return "notValid"
def lexer(text):
    errors=1
    tokens=[]
    lines=text.split('\n')
    i=0
    while i < len (lines):
        if(len(lines[i])==0 or lines[i][0]=='#'):##### empty lines
            del lines[i]
            i-=1
        i+=1
    for line in lines:
        word=line[0]
        j=1
        while j < len(line):
            if((tipo(line[j])==tipo(line[j-1]) and tipo(line[j])!="ope" and tipo(line[j])!="par") or (tipo(line[j-1])=="letter" and tipo(line[j])=="number")):
                word+=line[j]
            else:
                tokens.append(word)
                word=line[j]
            j+=1
        tokens.append(word)
        tokens.append('\n')
    i=1
    while i < len(tokens):
        if(tokens[i]=="\n" and tokens[i-1]=="\n"):
            del tokens[i]
            i-=1
        i+=1
    i=0
    comillas=0
    marker=0
    l=0
    while i < len(tokens):############# LOS STRINGS SEGURO SIGUEN TENIENDO PROBLEMAS
        if(tokens[i]=='"'):
            comillas+=1
            marker=i
        if(comillas==0):
            if(" " in tokens[i]):
                del tokens[i]
                i-=1
        if(comillas==1):
            tokens[marker]+=tokens[i]
            l+=1
        if(comillas==2):
            del tokens[i-l+1:i+1]
            i-=l-1
            l=0
            comillas=0
        i+=1
    i=0
    marker=0
    flag=0
    while i < len(tokens):
        if(tokens[i]=='#' and flag==0):
            flag=1
            marker=i
        if(tokens[i]=='\n' and flag==1):
            del tokens[marker:i]
            i-=(i-marker)
            flag=0
        i+=1
    i=0
    
    #operations=[",",":","+","-","*","/","^","%","@","!","menor","mayor","igual","=","sin","cos","tan","atan"]
    infix=["+","-","*","/","^","%","menor","mayor","igual","=",":",","]
    prefix=["sin","cos","tan","atan"]
    reservedActions=["bucle","condicion","mostrar","cerrar","funcion","retorno","subrutina"]
    ###############
    while i < len(tokens):
        if(tokens[i] in infix):
            tokens[i]=("infix",tokens[i])
        elif(tokens[i] in prefix):
            tokens[i]=("prefix",tokens[i])
        elif(tokens[i] in reservedActions):
            tokens[i]=("action",tokens[i])
        elif(tipo(tokens[i][0])=="number"):
            tokens[i]=("number",tokens[i])
        elif(tipo(tokens[i][0])=="letter"):
            tokens[i]=("expr",tokens[i])
        elif(tipo(tokens[i][0])=="uppCommas"):
            tokens[i]=("string",tokens[i][2:])
        elif(tipo(tokens[i][0])=="par"):
            tokens[i]=("parentesis",tokens[i])
        elif(tokens[i] == '\n'):
            tokens[i]=("line",tokens[i])
        else:
            del tokens[i]
            i-=1
        i+=1
        
    i=0 
    while i< len(tokens):
        turn=False
        if(tokens[i][1]=="-"):
            if(i==0):
                turn=True
            else:
                if(tokens[i-1][0]!="number" and tokens[i-1][0]!="expr"):
                    turn=True
        if turn:
            tokens[i]=("prefix","--")############################################# EL NEGATIVO COMO PREFIJO
        i+=1
            
    return tokens,errors



