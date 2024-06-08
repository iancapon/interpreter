def getl(array,index):
    ret=None
    if(index>=0 and index<len(array)):
        ret=array[index]
    return ret
def askToJoin(tokens,i,token):
    powers={"+":1, "-":1, "*":3, "/":3}
    mybp=int(powers.get(token[1]))+1
    nextbp=0
    if(i+1<len(tokens)):
        nextbp=int(powers.get(tokens[i+1][1]))
    return mybp>nextbp

def copyArray(arr,a,b):
    li=[]
    #b=len(arr)
    x=a
    while a < b:
        li.append(arr[a])
        a+=1
    return li
def bind_expr(tree,tokens,i,max): ##### capaz ya anda
    ni=i+1
    if(i>len(max)):########### queda todo el proceso guardado acá
        max.append(tree)###### cuando sale de la recursion, i decrece, pero no se sobreescribe
                        ###### esto lo evita
    while i< len(tokens)-1:
        token=tokens[i]
        ntoken=tokens[i+1]
        ptoken=tokens[i-1]
        if token[0]=="operation":
            if(askToJoin(tokens,ni,token)):
                if(len(tree)==0):
                    left=ptoken[1]
                    right=ntoken[1]
                    tree[token[1]]=[left,right]
                else:
                    left=tree
                    right=ntoken[1]
                    ntree={}
                    ntree[token[1]]=[left,right]
                    tree=ntree.copy()        
            else:
                a=i+1
                b=len(tokens)
                ntokens=copyArray(tokens,a,b)
                ntree={}
                nmax=[]
                i+=bind_expr(ntree,ntokens,1,nmax)
                if(len(tree)==0):
                    left=ptoken[1]
                    right=nmax[len(nmax)-1]
                    tree[token[1]]=[left,right]
                else:
                    left=tree
                    right=ntree[1]
                    nexttree={}
                    nexttree[token[1]]=[left,right]
                    tree=nexttree.copy() 
                break
        i+=bind_expr(tree,tokens,i+1,max)
        break
    return ni

def pratt_parser(tokens):
    #operacion:-> diccionario con llave "+-*/", elemento array entre left y right
    #dentro del elemento puede haber otra operacion
    arbol={}
    max=[]
    bind_expr(arbol,tokens,1,max) # { "+" : [ 10 , { "*" : [ 20 , 30 ] } ] }
    arbol=max[len(max)-1].copy()
    return arbol