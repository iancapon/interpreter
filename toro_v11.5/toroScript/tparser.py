def copy(array, a ,b):
    obj=[]
    a+=1
    while a < b:
        obj.append(array[a])
        a+=1
    return obj

def replace(array, section, a,b):
    del array[a:b+1] 
    array.insert(a, section ) 

def unbound(tokens):##### COSAS SUELTAS SIN MOTIVO, Y LA FLAG CERRAR
    i=0
    while i<len(tokens):
        if(type(tokens[i]) is tuple):
            if(tokens[i][0]!="line"):
                tokens[i]={tokens[i][0]:[tokens[i][1]]}
        i+=1
    return None

def unary_bind_right(op,tokens):
    if(True):
        i=0
        j=0
        newTokens=[]
        while i< len(tokens):
            if type(tokens[i]) is tuple:
                if(tokens[i][1]==op): ### CUANDO ENCUENTRO LA OPERACION
                    nextt=tokens[i+1] #### CHEQUEO A LA DERECHA
                    if(type(nextt) is tuple):
                        nextt={nextt[0]:[nextt[1]]}
                    di={"*"+op:[nextt]} ####### ARMO EL FORMATO
                        
                    newTokens.append(di) ## SUBO AL ARREGLO AUX
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
            tokens.append(word)### ACTUALIZO AL ARREGLO OBJETIVO

def left_right_bind(op,tokens):#v2
    if(True):
        i=0
        j=0
        newTokens=[]
        while i< len(tokens):
            if type(tokens[i]) is tuple:
                if(tokens[i][1]==op):###### ENCUENTRO LA OPERACION
                    prev=newTokens[j-1]## (IMPORTANTE, POR LA IZQ. USO EL NUEVO ARREGLO)
                    nextt=tokens[i+1]
                    
                    if(type(prev) is tuple):##### CATALOGO LO QUE LA ENVUELVE
                        prev={prev[0]:[prev[1]]}
                    if(type(nextt) is tuple):
                        nextt={nextt[0]:[nextt[1]]}
                    ##################################### ESPECIAL PARA LA COMA
                    if (list(prev.keys())[0]==","):
                        prev[","].append(nextt)
                    else:########################### SI NO ES COMA SE HACE ASÍ
                        di={op:[prev,nextt]} #### ARMO EL FORMATO
                        
                        newTokens.pop()
                        newTokens.append(di) ### AÑADO AL ARREGLO AUXILIAR
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
            tokens.append(word) ### ACTUALIZO EL ARREGLO OBJETIVO

def parse_rules(tokens):
    #### operacion unaria hacia la derecha
    #unary_bind("-",tokens)##### SIGUE SIN ANDAR BIEN LA BOSTA
    unary_bind_right("sin",tokens)
    unary_bind_right("cos",tokens)
    unary_bind_right("tan",tokens)
    unary_bind_right("atan",tokens)
    #### operadores binarios
    left_right_bind("^",tokens)
    left_right_bind("/",tokens)
    left_right_bind("*",tokens)
    left_right_bind("-",tokens)
    left_right_bind("+",tokens)
    #### operadores comparativos
    left_right_bind("mayor",tokens)
    left_right_bind("menor",tokens)
    left_right_bind("igual",tokens)
    #### igual
    left_right_bind("=",tokens)
    left_right_bind(",",tokens)######### PODRIA SER DISTINTO
    left_right_bind(":",tokens)
    ######## acciones
    unary_bind_right("mostrar",tokens)
    unary_bind_right("bucle",tokens)
    unary_bind_right("condicion",tokens)
    unary_bind_right("funcion",tokens)
    unary_bind_right("retorno",tokens)
    #COSAS SUELTAS, QUE NO CAMBIAN NADA O SON FLAGS (CIERRO)
    unbound(tokens)
    return tokens[0]

def parseLine(tokens):
    ##### PARSEA LINEA POR LINEA
    ##### PRIMERO ENCUENTRA LOS PARENTESIS
    i=0
    par_list=[]
    while i < len(tokens):
        if(tokens[i][0]=="parentesis"):
            if("(" in tokens[i][1]): #### ABRO PARENTESIS
                par_list.append([i,"x"])
            elif(")"in tokens[i][1]):#### cierro parentesis
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
                aux=copy(tokens,a,b) ### COPIO LO QUE VA DENTRO DEL PARENTESIS
                backtrack=len(aux)+1
                parse_rules(aux) ############### PARSEO DENTRO DEL PARENTESIS
                replace(tokens,aux[0],a,b) ### LO REEMPLAZO
                i-=backtrack
        i+=1
    parse_rules(tokens) ########### PARSEO POR FUERA DE LOS PARENTESIS 
    return None

def scopeBrackets(lines,start,end):
    ################# para encontrar los ifs/whiles/FUNCIONES
    i=0
    par_list=[]
    while i < len(lines):
        if(True):
            if((list(lines[i].keys()))[0] in start):############# abro "LLAVES"
                librito=[i,(list(lines[i].keys()))[0],"x"]
                par_list.append(librito)
            if(lines[i]=={"action":["cerrar"]} or (list(lines[i].keys()))[0] in end):############ cierro "LLAVES"
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
                ########################################## PONER LAS LINEAS DENTRO DE LA RAMA
                inside=copy(lines,a,b) ##### LO QUE VA DENTRO DEL CUERPO NUEVO (YA PARSEADO)
                putin=(list(lines[a].keys()))[0] ## LLAVE
                cond=lines[a][putin] ###### LA CONDICION (YA ESTÁ PARSEADA)

                lines[a][putin]=[] ## VACÍO EL CUERPO EN EL OBJETIVO
                
                lines[a][putin].append(cond[0]) ## CONDICION COMO UNA PARTE
                lines[a][putin].append({"\n":[]}) ## NUEVO CUERPO COMO OTRA
                
                for line in inside: ### AÑADO LINEA POR LINEA AL NUEVO CUERPO
                    lines[a][putin][1]["\n"].append(line)
                     
                if(list(lines[b].keys())[0]=="retorno"):############ PARA LAS FUNCIONES
                    lines[a][putin].append(lines[b])

                del lines[a+1:b+1] #### BORRO DEL CUERPO EXTERIOR
                i-=b-a
        i+=1
    return None

def fixFunctions(lines):
    for line in lines:
        if(list(line.keys())[0]=="*funcion"):
            args=line["*funcion"][0][":"][1]
            name=line["*funcion"][0][":"][0]["expr"][0]
            if(list(args.keys())[0]=="expr"):
                args=list( args["expr"][0] )
            else:
                args=[]
                ite=line["*funcion"][0][":"][1][","]
                for a in ite:
                    args.append(list(a.values())[0][0])
            #line["*funcion"][0][0]=(name,args)   
            
    return None

def parser(tokens):
    lines=[]
    i=0
    lines.append([])
    j=0
    ############################### VUELVO A SEPARAR EN LINEAS
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
    i=0
    for line in lines:##################### PARSEO CADA LINEA
        parseLine(line)
        tokens[0]["\n"].append(line[0])
    
    ############################# COMO LOS PARENTESIS, PERO CON LOS IF/WHILE/FUNCIONES
    scopeBrackets(tokens[0]["\n"],["*condicion","*bucle","*funcion"],["cerrar","*retorno"])
    fixFunctions(tokens[0]["\n"])

    return None