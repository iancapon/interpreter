from sys import *
from interpreter import *
import json

def printAst(program,space):
    print(space+program.type+":"+str(program.value))
    print(space+"hijos: "+str(len(program.children)))
    for node in program.children:
        print(space+"{")
        printAst(node,space+"~~~~")
    print(space+"}")
        
    return None

if __name__=="__main__":
    program=parse(argv[1])
    printAst(program,"")
    print(len(program.children[0].children))# EL ERROR ESTÁ EN EL AST
    