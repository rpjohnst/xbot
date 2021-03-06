# -*- coding: utf-8 -*-
#BraceParser.py
class countError(Exception):
    def __init__(self, expr, msg):
        self.expr=expr
        self.msg=msg
    def __str__(self):
        return self.msg
def parseBraces(input):
    matchArray=[]
    lookingForConditionals=True
    conditionalArray=[]
    conditionalSyntax=["(",")"]
    matchSyntax=["{","}"]
    conditionalCount=0
    conditionalPosition=-1
    matchCount=0
    matchPosition=-1
    for position,letter in enumerate(input):
        if letter==conditionalSyntax[0] and lookingForConditionals:
            conditionalCount+=1
            if conditionalCount==1:
                conditionalPosition=position
        elif letter==conditionalSyntax[1] and lookingForConditionals:
            conditionalCount-=1
            if conditionalCount==0:
                conditionalArray.append(input[conditionalPosition+1:position])
        if letter==matchSyntax[0]:
            if conditionalCount!=0:
                continue
            lookingForConditionals=False
            matchCount+=1
            if matchCount==1:
                matchPosition=position
        elif letter==matchSyntax[1]:
            if conditionalCount!=0:
                continue
            matchCount-=1
            if matchCount==0:
                matchArray.append(input[matchPosition+1:position])
    if conditionalCount!=0:
        raise countError(input,"Unbalanced brackets!")
    elif matchCount!=0:
        raise countError(input,"Unbalanced parentheses!")
    return (conditionalArray, matchArray)
if __name__=="__main__":
    input="!if (dicks==true) AND (lasers==awesome) {superdicks;var dicks = false;} else {hyperdicks;var dicks = true;}"
    print parseBraces(input)
