def visualize(tree,sangria):
    trunk=tree[0]
    if(trunk=="\n"):
        trunk="linea"
    branch=tree[1]
    print(sangria+"["+trunk+"]:")
    if type(branch) is list:
        for aux in branch:
            visualize(aux,sangria+4*" ")
    else:
        print(sangria+4*" "+"  <<"+str(branch)+">>")

