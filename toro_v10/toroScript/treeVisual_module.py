def printTreeVisual(tree,sangria):
    key=(list(tree.keys()))
    space="-"*(len(str(key))+1)
    print(sangria+str(key)+"{")
    for branch in tree[key[0]]:
        if(type(branch)==str):
            print(sangria+space+branch+";")
        elif(type(branch)==tuple):
            print(sangria+space+str(branch)+";")
        else:
            printTreeVisual(branch,space+sangria)
    print(sangria+"}")