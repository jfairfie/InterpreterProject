'''
Created on Nov 25, 2020

@author: jfairfie
'''
#Returns equation in prefix notation 
def inToPost(tokens):
    reverse = []
    outputStack = []
    operatorStack = []  
    
    #Reversing infix notation    
    while (len(tokens) > 0):
        token = tokens.pop()
        reverse.append(token)
    
    while (len(reverse) > 0):
        token = reverse.pop()
        if (token[1].isdigit() or token[0] == 'identifier'):
            outputStack.append(token)
        elif (token[0] == 'operator'):
            if (len(operatorStack) == 0):
                operatorStack.append(token)
            #Operator stack is not empty )
            else:
                if (token[1] == '('):
                    operatorStack.append(token)
                elif (token[1] == ')'):
                    operator = operatorStack.pop()
                    while(operator[1] != '('):
                        outputStack.append(operator)
                        operator = operatorStack.pop()
                else:
                    if (precedence(token[1]) > precedence(operatorStack[len(operatorStack)-1][1])):
                        operatorStack.append(token)
                    else:
                        if (operatorStack[len(operatorStack)-1][1] != ')' and operatorStack[len(operatorStack)-1][1] != '('):
                            while (len(operatorStack) > 0 and operatorStack[len(operatorStack)-1][1] != '(' and operatorStack[len(operatorStack)-1][1] != ')'):
                                outputStack.append(operatorStack.pop())
                        operatorStack.append(token)
                    
                                      
    while (len(operatorStack) > 0):
        token = operatorStack.pop()
        outputStack.append(token)
        
    return outputStack

def postToPre(postList):
    preList = []
    while (len(postList) > 0):
        preList.append(postList.pop())
    return preList

def precedence(operator):
    if (operator == ')' or operator == '('):
        return 3
    if (operator == '*' or operator == '/' or operator == '%'):
        return 2
    if (operator == '+' or operator == '-'):
        return 1
    