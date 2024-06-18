def topof(stack):
    l=len(stack)
    if(l>0):
        return stack[l-1]
    else:
        return ("empty","null")

def power(x):
    bPower={"+":10,"*":20,"-":10,"/":20,"\n":1,"null":0,"=":5,"mostrar":5}
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
        elif(tokens[i][0]=="operation" or tokens[i][0]=="line"):
            while(power(tokens[i]) < power(topof(stack))):
                output.append(stack.pop())
            if (power(tokens[i]) > power(topof(stack))):
                stack.append(tokens[i])
            del tokens[i]
            i-=1
        elif(tokens[i][0]=="parentesis"):
            if(tokens[i][1]=="("):
                stack.append(tokens[i])
            elif(tokens[i][1]==")"):
                while(topof(stack)[1]!="("):
                    output.append(stack.pop())
                stack.pop()
            del tokens[i]
            i-=1
        elif(tokens[i][0]=="action"):
            stack.append(tokens[i])
            del tokens[i]
            i-=1
        i+=1
    i=0
    while len(stack)>0:
        output.append(stack.pop())
    
    ########################## EJECUTO, O ARMO ARBOL
    i=0
    while i < len(output):
        if(output[i][0]=="operation"):
            branch=(output[i][1],[output[i-2],output[i-1]])
            del output[i-2:i+1]
            i-=2
            output.insert(i,branch)

        elif(output[i][0]=="line" or output[i][0]=="action"):
            branch=(output[i][1],[output[i-1]])
            del output[i-1:i+1]
            i-=1
            output.insert(i,branch)
        i+=1
    tokens.append(output[0])
    
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
    i=0
    while i<len(lines):
        if(len(lines[i])>0):
            tokens[0][1].append(lines[i][0][1][0])
        i+=1