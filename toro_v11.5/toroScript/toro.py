import sys
from tparser import *
from lexer import *
from runner import *
from tree import *

if(len(sys.argv)>=2):#### leer programas
    archivo=open(sys.argv[1],'r')
    sourceCode=archivo.read()
    tokens=lexer(sourceCode)
    #print(tokens)
    parser(tokens)
    visualize(tokens[0],"")
    stack={}
    runNew(tokens[0],stack)
    #print(stack)
    
else: ### consola
    stack={}
    while True:
        print("<t> ",end="")
        text=input()
        if(text!="0"):
            tokens=lexer(text)
            parser(tokens)
            print(runNew(tokens[0]["\n"][0],stack))
        else:
            break