import sys
from parser_module import *
from lexer_module import *
from run_module import *
from treeVisual_module import *
       
def main():
    stack={}
    if(len(sys.argv)>1):
        ruta=sys.argv[1]
        if ruta.split('.')[1] == 'toro':
            try:
                with open(ruta, 'r') as archivo:
                    archivo=open(ruta,'r')
                    sourceCode=archivo.read()
                    tokenArray=newLexer(sourceCode)
                    my_parserNew(tokenArray)
                    tree=tokenArray[0]

                    printTreeVisual(tree,"")
                    runNew(tree,stack)
                    #print(stack)

            except FileNotFoundError:
                print("El archivo no existe.")
            except IOError as e:
                print("Error al abrir el archivo:", e)
        else:
            print("La extension debe ser ´.toro")
    else:
        while True:
            print("0 to exit > ",end="")
            text=input()
            if(text=="0"):
                break
            else:
                tokens=newLexer(text)
                
                my_parserNew(tokens)
                runNew(tokens[0],stack)


def test():
    stack={}
    text=input()
    #text+="+0"############ añadir al lexer
    tokenArray=newLexer(text)
    #print("\nTOKENS: "+str(tokenArray),end="\n\n")
    my_parserNew(tokenArray)
    tree=tokenArray[0]
    print("TREE: "+str(tree),end="\n\n")
    runNew(tree,stack)



main()
#test()