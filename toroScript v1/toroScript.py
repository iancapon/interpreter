import sys

def main():
    ruta=sys.argv[1]
    if ruta.split('.')[1] == 'toro':
        try:
            with open(ruta, 'r') as archivo:
                archivo=open(ruta,'r')
                instance=Program()
                for line in archivo:
                    instance.parseLine(line.strip())
                instance.run()
        except FileNotFoundError:
            print("El archivo no existe.")
        except IOError as e:
            print("Error al abrir el archivo:", e)
    else:
        print("La extension debe ser ´.toro´")

class Program:
    def __init__(self):
        self.tokens=[]
        self.stack=[]
    def run(self):
        pc=0
        while(pc<len(self.tokens)):
            opcode=self.tokens[pc]
            if(opcode=="PUSH"):
                self.stack.append(self.tokens[pc+1])
                pc+=2
            elif(opcode=="POP"):
                print(self.stack.pop())
                pc+=1
            elif(opcode=="PRINT"):
                print(self.tokens[pc+1])
                pc+=2
            elif(opcode=="PRINT.TOP"):
                aux=self.stack.pop()
                print(aux)
                self.stack.append(aux)
                pc+=1
            elif(opcode=="ADD"):
                b=int(self.stack.pop())
                a=int(self.stack.pop())
                self.stack.append(a+b)
                pc+=1
            elif(opcode=="MUL"):
                b=int(self.stack.pop())
                a=int(self.stack.pop())
                self.stack.append(a*b)
                pc+=1
            elif(opcode=="DIV"):
                b=int(self.stack.pop())
                a=int(self.stack.pop())
                self.stack.append(int(a/b))
                pc+=1
            elif(opcode=="SUB"):
                b=int(self.stack.pop())
                a=int(self.stack.pop())
                self.stack.append(a-b)
                pc+=1
            elif(opcode=="JUMP.EQ.0"):
                if(int(self.stack[len(self.stack)-1])==0):
                    pc=self.jump(self.tokens[pc+1])
                else:
                    pc+=2
            elif(opcode=="JUMP.GT.0"):
                if(int(self.stack[len(self.stack)-1])>0):
                    pc=self.jump(self.tokens[pc+1])
                else:
                    pc+=2
            elif(opcode=="PEAK"):
                val=pc-int(self.tokens[pc+1])
                if(val>=0 and val <  len(self.stack)):
                    val=self.stack[val]
                    self.stack.append(val)
                pc+=2
            elif(opcode=="REPLACE"):
                val=pc-int(self.tokens[pc+1])
                if(val>=0 and val <  len(self.stack)):
                    self.stack[val]=self.stack[len(self.stack)-1]
                    self.stack.pop()
                pc+=2
            elif(opcode=="HALT"):
                pc=len(self.tokens)
            elif(opcode=="READ"):
                value= input(": ")
                self.stack.append(value)
                pc+=1
            else:
                pc+=1
    
    def jump(self,target):
        i=0
        while i< len(self.tokens):
            if(self.tokens[i]=="$" and self.tokens[i+1]==target):
                break
            i+=1
        return i
    
    def parseLine(self,line):
        aux=line.split(' ')
        i=0
        word=""
        while i< len(aux):
            word=aux[i]
            if(word=="%"):
                j=i+1
                word=""
                while aux[j] != "%" and j<len(aux):
                    word+=aux[j]+" "
                    j+=1
                i=j
            i+=1
            self.tokens.append(word)
        
main()