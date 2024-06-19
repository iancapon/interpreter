import sys
from tparser import *
from lexer import *
from runner import *
from tree import *

if(len(sys.argv)>=2):#### leer programas
    archivo=open(sys.argv[1],'r')
    sourceCode=archivo.read()
    tokens=lexer(sourceCode)
    parser(tokens)
    visualize(tokens[0],"")
    #print(tokens[0][1])
    stack={}
    runProgram(tokens[0],stack)
    
else: ### consola
    stack={}
    while True:
        print("<t> ",end="")
        text=input()
        if(text!="0"):
            tokens=lexer(text)
            parser(tokens)
            print(runProgram(tokens[0][1][0],stack))
        else:
            break