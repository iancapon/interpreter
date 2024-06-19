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

def topof(stack):
    l=len(stack)
    if(l>0):
        return stack[l-1]
    else:
        return ("empty","null")

def power(x):
    bPower={"+":10,"*":20,"-":10,"/":20,"\n":1,"null":0,"=":5,"mostrar":5,"mayor":50,"menor":50,"igual":50,"^":30,"%":20,"--":45,"(":0,")":0,"sin":40,"cos":40,"tan":40,"atan":40}
    ret=bPower.get(x[1])
    if (ret!=None):
        return ret
    else:
        return 0

def parseLine(tokens):
    ########################### ARMO NOTACION POLACA INVERSA
    stack=[]
    output=[]
    i=0
    while i < len(tokens):
        if(tokens[i][0]=="expr" or tokens[i][0]=="number" or tokens[i][0]=="string"):
            output.append(tokens[i])
            del tokens[i]
            i-=1
        elif(tokens[i][0]=="parentesis"):
            if(tokens[i][1]=="("):
                stack.append(tokens[i])
            elif(tokens[i][1]==")"):
                while(topof(stack)[1]!="(" ):
                    output.append(stack.pop())
                stack.pop()
            del tokens[i]
            i-=1
        elif(tokens[i][0]=="infix"):
            while(power(tokens[i]) <= power(topof(stack))):
                output.append(stack.pop())
            if (power(tokens[i]) > power(topof(stack))):
                stack.append(tokens[i])
            del tokens[i]
            i-=1
        elif(tokens[i][0]=="prefix"):
            stack.append(tokens[i])
            del tokens[i]
            i-=1
        elif(tokens[i][0]=="action"):
            stack.append(tokens[i])
            del tokens[i]
            i-=1
        elif(tokens[i][0]=="line"):
            del tokens[i]
            i-=1
        i+=1
    i=0
    while len(stack)>0:
        output.append(stack.pop())
    ########################## EJECUTO, O ARMO ARBOL
    i=0
    while i < len(output):
        if(output[i][0]=="infix"):
            branch=(output[i][1],[output[i-2],output[i-1]])
            del output[i-2:i+1]
            i-=2
            output.insert(i,branch)
        elif(output[i][0]=="action" or output[i][0]=="prefix"):
            branch=(output[i][1],[output[i-1]])
            del output[i-1:i+1]
            i-=1
            output.insert(i,branch)
        i+=1
    tokens.append(output[0])
    
def scopeBrackets(lines,start,end):
    ################# para encontrar los ifs/whiles/FUNCIONES
    i=0
    par_list=[]
    while i < len(lines):
        if(len(lines[i])==0):
            del lines[i]
            i-=1
        elif(len(lines[i])>0):
            if(lines[i][0][0] in start):############# abro "LLAVES"
                librito=[i,lines[i][0][0],"x"]
                par_list.append(librito)
            if(lines[i]==("action","cerrar") or lines[i][0][0] in end):############ cierro "LLAVES"
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
                ########################################## PONER LAS LINEAS DENTRO 
                aux=[]
                x=a+1
                while x < b:
                    aux.append(lines[x][0])
                    x+=1

                lines[a][0][1].append(("\n",aux))############ ACÁ
                
                if(lines[i][0][0] == "retorno"):
                    lines[a][0][1].append(lines[x][0])####### PONER EL RETORNO
                    
                del lines[a+1:i+1] #### BORRO DEL CUERPO EXTERIOR
                i-=i-a
        i+=1
        
    return None
    
def parser(tokens):
    lines=[]
    i=0
    lines.append([])
    while len(tokens)>0:
        lines[i].append(tokens[0])
        if(tokens[0][0]=="line"):
            lines.append([])
            parseLine(lines[i])
            i+=1
        del tokens[0]
        
    tokens.append(("\n",[]))

    scopeBrackets(lines,["bucle","condicion","funcion"],["cerrar","retorno"])
    
    for l in lines:
        #print(l[0])
        tokens[0][1].append(l[0])
    #print((lines[1][0][1][1][1]))
        
    
   
        
    #tokens.append(("\n",lines))