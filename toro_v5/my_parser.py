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

def parse_left_right(tokens):#### operadores binarios
    my_bind("^",tokens)
    my_bind("/",tokens)
    my_bind("*",tokens)
    my_bind("-",tokens)
    my_bind("+",tokens)
    my_bind("=",tokens)
    return tokens[0]

def copy(array, a ,b):
    obj=[]
    a+=1
    while a < b:
        obj.append(array[a])
        a+=1
    return obj

def replace(array, section, a,b):
    del array[a:b+1] # {'()': section}
    array.insert(a, section ) 

def my_parser(tokens):
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
                parse_left_right(aux) 
                replace(tokens,aux[0],a,b)
                i-=backtrack
                #print(backtrack)
        i+=1
    parse_left_right(tokens) 
    #print(par_list)