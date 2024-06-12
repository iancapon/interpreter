def copy(array, a ,b):
    obj=[]
    a+=1
    while a < b:
        obj.append(array[a])
        a+=1
    return obj

def my_bind(op,tokens):#v2
    if(op in "+-*/^=><:"):
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

def insertPrintTokens(tokens):
    if(type(tokens[0]) is tuple):
        tokens[0]={"print":copy(tokens,0,len(tokens)-1)}
        del tokens[1:]

def parse_left_right(tokens):
    
    #### operadores binarios
    my_bind("^",tokens)
    my_bind("/",tokens)
    my_bind("*",tokens)
    my_bind("-",tokens)
    my_bind("+",tokens)
    #### operadores comparativos
    my_bind(">",tokens)
    my_bind("<",tokens)
    my_bind(":",tokens)
    #### igual
    my_bind("=",tokens)
    #### funciones basicas
    #############################################################################printOp(tokens)
    return tokens[0]



def replace(array, section, a,b):
    del array[a:b+1] # {'()': section}
    array.insert(a, section ) 

def parseLine(tokens):
    ##### PARSEA LINEA POR LINEA
    ##### PRIMERO ENCUENTRA LOS PARENTESIS
    i=0
    par_list=[]
    while i < len(tokens):
        if(tokens[i][0]=="parentesis"):
            if(tokens[i][1]=="("):
                par_list.append([i,"x"])
            if(tokens[i][1]==")"):#### cierro parentesis
                backtrack=0
                pc=len(par_list)
                a=0
                b=0
                while True:
                    pc-=1
                    if(par_list[pc][1]=="x"):
                        par_list[pc][1]=i
                        a=par_list[pc][0]
                        b=i
                        break
                aux=copy(tokens,a,b)
                backtrack=len(aux)+1
                parse_left_right(aux) ############### PARSEO DENTRO DEL PARENTESIS
                replace(tokens,aux[0],a,b)
                i-=backtrack
        i+=1
    parse_left_right(tokens) ########### PARSEO POR FUERA DE LOS PARENTESIS 

    ########################################## ANTES ESTABA DENTRO DE PARSE_LEFT_RIGHT
    insertPrintTokens(tokens)#############################################################printOp(tokens)

def rearrangeScope(lines,start,end):
    ##### para encontrar los else/ifs/whiles
    i=0
    par_list=[]
    while i < len(lines):
        if(type(lines[i]) is list):
            #print(lines[i][0][1])
            if(lines[i][0][1] == start[0] or lines[i][0][1] == start[1]):#### abro "LLAVES"
                librito=[i,lines[i][0][1],"x"]
                #print(librito)
                par_list.append(librito)
                #print(len(par_list))
            if(lines[i][0][1]==end):#### cierro "LLAVES"
                backtrack=0
                pc=len(par_list)
                a=0
                b=0
                while True:
                    pc-=1
                    if(par_list[pc][2]=="x"):
                        par_list[pc][2]=i
                        a=par_list[pc][0]
                        b=i
                        break
                ########################################### ARMAR RAMA DE IF/WHILE
                cond=copy(lines[a],-1,len(lines[a]))
                del cond[0]
                cond.insert(-1,("operation","="))
                cond.insert(-1,("number","0"))
                parseLine(cond)#parse_left_right(cond)
                typeOfCond=par_list[pc][1]
                cond[0][typeOfCond]=cond[0]["="]
                del cond[0]["="]
                cond[0][typeOfCond][1]={"\n":[]}
                ########################################## PONER LAS LINEAS DENTRO DE LA RAMA
                inside=copy(lines,a,b)
                putin=cond[0][typeOfCond][1]["\n"]
                for line in inside:
                    putin.append(line)
                ########################################### INSERTO DENTRO DEL ARBOL 
                lines[a]=cond[0]################# LA RAMA CON EL IF/WHILE
                del lines[a+1:b+1]
                i-=b-a
        i+=1

def my_parserNew(tokens):
    ############### SEPARO EN LINEAS
    lines=[]
    i=0
    lines.append([])
    j=0
    while i<len(tokens):
        if(tokens[i][0]!="line"):
            lines[j].append(tokens[i])
        else:
            lines[j].append(tokens[i])
            lines.append([])
            j+=1
        i+=1
    lines.pop()
    tokens.clear()
    tokens.append({"\n":[]})###### CUERPO DEL PROGRAMA
    ############################### DEJO EL [] DE TOKENS VACIO PARA LLENAR CON EL ARBOL
    for line in lines:
        if(line[0][1] == "condicion" or line[0][1] == "cerrar" or line[0][1] == "bucle"):
            tokens[0]["\n"].append(line)###### DEJO SIN PARSEAR LAS LINEAS CON IF/WHILE 
        else:                           ######                         (CABECERA Y CIERRE)
            parseLine(line) ########### PARSEO LAS DEMAS LINEAS, INCLUSO DENTRO DE IF/WHILE'S 
            tokens[0]["\n"].append(line[0])
    
    rearrangeScope(tokens[0]["\n"],["condicion","bucle"],"cerrar")#### ENCONTRAR LOS IF/WHILE
                                    ##### IGUAL QUE CON LOS PARENTESIS, SUBDIVIDO EL DOMINIO
                                    ##### DE A POCO, SIN MUCHA RECURSIVIDAD.