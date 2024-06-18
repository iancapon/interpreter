def runProgram(tree,stack):
    leaf=0
    trunk=tree[0]
    branches=tree[1]
    
    if(trunk=="\n"):
        for branch in branches:
            runProgram(branch,stack)
    if(trunk=="mostrar"):
        print(runProgram(branches[0],stack))
    if(trunk=="="):
        a=branches[0][1]
        b=runProgram(branches[1],stack)
        stack[a]=b
    if(trunk=="number"):
        leaf=float(branches)
    if(trunk=="string"):
        leaf=branches
    if(trunk=="expr"):
        leaf=stack.get(branches)
        if(leaf==None):
            leaf="ERROR"
    if(trunk=="+"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a+b
    if(trunk=="*"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a*b
    if(trunk=="-"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a-b
    if(trunk=="/"):
        a=runProgram(branches[0],stack)
        b=runProgram(branches[1],stack)
        leaf=a/b
    
    
    return leaf