import re

def lexer(text):
    tokens=text.split(" ")
    items=[]
    for word in tokens:
        if re.match(r"[.0-9]",word):## or (word[0]=="-" and re.match(r"[.0-9]",word[1:])):  ##### POR CONSISTENCIA
            items.append(("number",word))
        elif word in "+-*/=^":
            items.append(("operation",word))
        elif word in "()":
            items.append(("parentesis",word))
        else:
            items.append(("string",word))
    
    return items

def fixNegativeSign(tokens,reserved):
    i=0
    neg=lexer("( 0 - 1 ) *")
    while i< len(tokens):############# MUUUY TEMPORAL
        fix=False
        if(tokens[i][1]=="-" and i==0):
            fix=True
        elif(tokens[i][1]=="-" and i>0):
            if (tokens[i-1][0]!= "number" or tokens[i-1][0]!="string"):
                fix=True
            elif(tokens[i-1][0]=="string" and tokens[i-1][1] in reserved):
                fix=True
        if fix==True:
            del tokens[i]
            j=0
            while j<len(neg):
                tokens.insert(i+j,neg[j])
                j+=1
            i+=j-1
        i+=1
    #print(tokens)
