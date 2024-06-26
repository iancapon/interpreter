import sys
from tparser import *
from lexer import *
from runner import *
from tree import *

if(len(sys.argv)>=2):#### leer programas
    archivo=open(sys.argv[1],'r')
    sourceCode=archivo.read()
    tokens,errors=lexer(sourceCode)
    if(errors > 0):
        errors=parser(tokens)
        if(errors > 0):
            visualize(tokens[0],"")
            stack={}
            runProgram(tokens[0],stack)
            #print(stack)
    if errors <= 0:
        print("ERROR")
else: ### consola
    stack={}
    while True:
        print("<t> ",end="")
        text=input()
        if(text!="exit"):
            tokens=lexer(text)
            parseLine(tokens[0])
            print(runProgram(tokens[0][0],stack))
        else:
            break

