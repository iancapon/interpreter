def copy(array, a ,b):
    obj=[]
    a+=1
    while a < b:
        obj.append(array[a])
        a+=1
    return obj

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

def printOp(tokens):
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
    my_bind("=",tokens)
    ##### funciones basicas
    printOp(tokens)
    return tokens[0]



def replace(array, section, a,b):
    del array[a:b+1] # {'()': section}
    array.insert(a, section ) 

def parseLine(tokens):
    ##### para encontrar los parentesisesSasesSen
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
    parse_left_right(tokens) ########### PARSEO POR FUERA DE LOS PARENTESIS YA ARMADOS


def my_parserNew(tokens):
    ############### separo en lineas
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
    tokens.append({"\n":[]})

    for line in lines:
        parseLine(line) ################ PARSEO CADA LINEA
        #if(line[len(line)-1]==None):
        #line.pop()
        tokens[0]["\n"].append(line[0])

    