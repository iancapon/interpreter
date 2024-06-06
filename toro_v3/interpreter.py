import re

reserved_words=["mate", "yerba"]

def lexer(text):
    program=[]
    for line in text:
        if(line!=""):
            tokens=[]
            word=""
            rayita_count=0
            for c in line:
                if(c=="'" or c=='"'):
                    rayita_count+=1
                if(c==" " and rayita_count%2==0):
                    tokens.append(word)
                    word=""
                else:
                    word+=c
            tokens.append(word)
            items=[]
            for token in tokens:
                if (token[0]=="'" and token[-1]=="'") or (token[0]=='"' and token[-1]=='"'):
                    items.append(("string",token[1:-1]))
                elif re.match(r"[.a-zA-Z]+",token):####quizas esté aml
                    if token not in reserved_words:
                        items.append(("variable",token))
                    else:
                        if token == reserved_words[0]:
                            items.append(("declaration",token))
                        elif token == reserved_words[1]:
                            items.append(("print",token))
                elif token in "+-*/":
                    items.append(("operation",token))
                elif token == "=":
                    items.append(("equal",token))
                elif re.match(r"[.0-9]",token):
                    items.append(("number",token))
                elif token == "(":
                    items.append(("open_par",token))
                elif token == ")":
                    items.append(("close_par",token))
            program.append(items)

    return program

def ast(parent,line,index):
    if index==0:#############osea digamos separa las lineas
        parent.setSon(Node(line[index]))
        ast(parent.children[len(parent.children)-1],line,index+1)

    elif(index<len(line)):
        children=parent.children
        token=line[index]

        if token[0]=="operation":#### operaciones
            current=parent.getParent()
            left=current.children[0]
            print(left.value)
            current.children.pop()
            current.setSon(Node(line[index]))
            current.children[0].setSon(left)
            ast(current.children[0],line,index+1)

        else:
            parent.setSon(Node(line[index]))# TOKENS SIN CONDICIONES RARAS
            ast(children[0],line,index+1)
    
        


def parse(file):
    text=open(file,"r").read().split("\n")
    tokens_by_lines=lexer(text)

    body=Node(("body",None))
    for line in tokens_by_lines:
        ast(body,line,0)
    
    return body

def node(token):
    type,value=token
    children=[]
    return [type,value,children]

class Node:
    def __init__(self,token):
        self.type,self.value=token
        self.children=[]
        self.parent=None
        self.retorno=None
        
    def setSon(self,son):
        son.parent=self
        self.children.append(son)
    def getParent(self):
        return self.parent
        
    