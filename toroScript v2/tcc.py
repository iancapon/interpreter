import sys

def main():
    ruta=sys.argv[1]
    src=[]
    ok=False
    if ruta.split('.')[1] == 'tcc':
        try:
            with open(ruta, 'r') as archivo:
                archivo=open(ruta,'r')
                sourceCode=archivo.read()
                parser=Parser()
                src, ok=parser.parse(sourceCode)
        except FileNotFoundError:
            print("El archivo no existe.")
        except IOError as e:
            print("Error al abrir el archivo:", e)
    else:
        print("La extension debe ser ´.tcc")

    if(ok):#### SI EL PARSE FUE EXITOSO PUEDO SEGUIR
        tokenizer=Tokenizer()
        for c in src:
            print(c)

class TokenNode:
    def __init__(self):
        self.types=["Variable","Number","Addition","Multiplication","Equal","Parenthesis","Action"]
        self.type=""
        self.value=""
        return None


class Tokenizer:
    def __init__(self):
        self.list=[]
        self.types=["Variable","Number","Addition","Multiplication","Equal","Parenthesis","Action"]
        self.chrType=["letter","Number","Addition","Multiplication","Equal","openParen","closeParen","separation","Action"]
        return None
    
    def createToken(self,type,value):
        tokenType=""
        if(type=="letter"):
            tokenType=self.types[0]
        elif(type=="Number"):
            tokenType=self.types[1]
        elif(type=="Addition"):
            tokenType=self.types[2]
        elif(type=="Multiplication"):
            tokenType=self.types[3]
        elif(type=="Equal"):
            tokenType=self.types[4]
        elif(type=="Action"):
            tokenType=self.types[3]
            
    def findToken(self,src):
        y=[]
        x=src[0]
        i=1
        tokenValue=""
        while i< len(src):
            y=src[i]
            if(x[0]==y[0]):
                tokenValue+=x[1]
            else:
                #token=TokenNode()
                token=self.createToken(x[0],tokenValue)
                self.list.append(token)
                tokenValue=""
            i+=1
        return self.list

class Parser:
    def __init__(self):
        self.chrType=["letter","Number","Addition","Multiplication","Equal","openParen","closeParen","separation","Action"]
        self.ok=True
        self.src=[]
        return None

    def isNumber(self,chr):
        ret=False
        specialChars="0123456789."
        if(chr in specialChars):
            ret=True
        return ret,self.chrType[1]

    def isLetter(self,chr):
        ret=False
        v=ord(chr)
        if(v>90):
            v-=32
        if(v<=90 and v>=65):
            ret=True
        return ret,self.chrType[0]

    def isSpecial(self,chr):
        ret=False
        specialChars=" ()+-*/,;=\n#" #### el HASH es el print
        if(chr in specialChars):
            ret=True
        type=""
        if(chr=="("):
            type=self.chrType[5]
        if(chr==")"):
            type=self.chrType[6]
        if(chr=="+"):
            type=self.chrType[2]
        if(chr=="-"):
            type=self.chrType[2]
        if(chr=="*"):
            type=self.chrType[3]
        if(chr=="/"):
            type=self.chrType[3]
        if(chr=="," or chr==";" or chr=="\n"):
            type=self.chrType[7]
        if(chr=="="):
            type=self.chrType[4]
        if(chr=="#"):
            type=self.chrType[8]
        return ret,type

    def isvalid(self,chr):
        ret,type=self.isNumber(chr)
        if(ret==False):
            ret,type=self.isLetter(chr)
        if(ret==False):
            ret,type=self.isSpecial(chr)
        return ret,type

    def parse(self,sourceCode):
        line=1
        for chr in sourceCode:
            if(chr!=" "):
                ret,type=self.isvalid(chr)
                if(ret ):
                    if (chr!='\n'):
                        self.src.append([type,chr])
                    else:
                        line+=1
                elif(ret==False):
                    print("Error, caracter invalido en linea "+str(line))
                    self.ok=False
                    break
        return self.src,self.ok
    

main()