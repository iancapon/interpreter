import sys
from my_parser import *
from lexer import *
from run import *


def main():
    stack={}
    if(len(sys.argv)>1):
        ruta=sys.argv[1]
        if ruta.split('.')[1] == 'toro':
            try:
                with open(ruta, 'r') as archivo:
                    archivo=open(ruta,'r')
                    sourceCode=archivo.read()
                    sourceCode=sourceCode.split("\n")
                    for line in sourceCode:
                        if("#" not in line):
                            tokenArray=lexer(line)
                            fixNegativeSign(tokenArray,["yerba"])
                            printConf=False
                            if(tokenArray[0][1]=="yerba"):###### TEMPORARIO
                                tokenArray.remove(tokenArray[0])
                                tokenArray.append(("operation","+"))
                                tokenArray.append(("number","0"))
                                printConf=True
                            my_parser(tokenArray)
                            tree=tokenArray[0]
                            #print("TREE: "+str(tree),end="\n\n")
                            ret=(run(tree,stack))
                            if printConf:
                                print(ret)

            except FileNotFoundError:
                print("El archivo no existe.")
            except IOError as e:
                print("Error al abrir el archivo:", e)
        else:
            print("La extension debe ser ´.toro")
    else:
        print("0 to exit > ",end="")
        text=input()
        while(text!="0"):
            tokenArray=lexer(text)
            fixNegativeSign(tokenArray,["yerba"])
            if(tokenArray[0][1]=="yerba"):###### TEMPORARIO
                tokenArray.remove(tokenArray[0])
                tokenArray.append(("operation","+"))
                tokenArray.append(("number","0"))
            my_parser(tokenArray)
            tree=tokenArray[0]
            print(run(tree,stack))
            print("0 to exit > ",end="")
            text=input()
        
def test():
    stack={}
    text="( 10 + 20 ) * 3"
    tokenArray=lexer(text)
    
    print("\nTOKENS: "+str(tokenArray),end="\n\n")
    my_parser(tokenArray)
    tree=tokenArray[0]
    print("TREE: "+str(tree),end="\n\n")
    print("RESULT: "+str(run(tree,stack)))



#test()
main()