'''
Created on Nov 25, 2020

@author: jfairfie
'''
from LexicalAnalyzer import Lexer
import sys
import PostFixConverter

class Parser():
    def __init__(self):
        self.root = ProgramNode()
    
    def parse(self):
        f = open('TestProgram.txt')
        tokenList = f.read().splitlines()
        
        for tList in tokenList:
            Lex = Lexer(list(tList))
            token = Lex.lex()
            
            while (token != 'EOF'):
                self.root.insert(token, Lex)
                token = Lex.lex()
        
        #Returns root of parse tree 
        return self.root
    
#First Node 
class ProgramNode:
    def __init__(self):
        self.value = '<Program>'
        self.down = StmtsNode()
        self.level = 0

    def insert(self, token, tokenStream):
        self.down.insert(token, tokenStream, self.level+1)
    
    def printTree(self):
        print(self.value)
        self.down.printTree()
        
class StmtsNode: 
    def __init__(self):
        self.value = '<stmts>'
        self.branches = []
    
    ''' IMPORTANT INSERT '''
    def insert(self, token, tokenStream, level):
        self.level = level
        #Variable initialization 
        if (token[1] == 'var'):
            assignNode = AssignNode()
            token = tokenStream.lex()
            assignNode.insert(token, tokenStream, self.level+1)
            self.branches.append(assignNode)
        #Arithmetic Operations 
        elif (token[0] == 'identifier'):
            assignNode = AssignNode()
            assignNode.changeValue('<IdentifierAssign>')
            assignNode.insert(token, tokenStream, self.level+1)
            self.branches.append(assignNode)
        else:
            sys.exit('Error:: syntax error, invalid statement ' + token[1])
    ''' ===============  '''
    def printTree(self):
        print(' ' * self.level, self.value)
        for branch in self.branches:
            branch.printTree()
               

#Generic node, can be <identifier>, or <constant> etc
class Node:
    def __init__(self, type, token, level):
        self.level = level
        self.type = type 
        self.value = '<' + type + '>'
        if (token[0] == type):
            self.data = token[1]
        else:
            sys.exit('Error:: expected ' + type + ' instead of ' + token[0])
    
    def returnType(self):
        return (self.type, self.data)
    
    def evaluateExpr(self):
        return self.data
    
    def printTree(self):
        print(' ' * self.level, self.value)
        print(' ' * (self.level + 1), self.data)

#Variable assignment 
class AssignNode:
    def __init__(self):
        self.value = '<VarAssign>'
        self.left = None 
        self.down = None 
        self.right = None 
    
    def changeValue(self, value):
        self.value = value
    
    def insert(self, token, tokenStream, level):
        self.level = level
        self.left = Node('identifier', token, self.level+1)
        token = tokenStream.lex()
        if (token == 'EOF'):
            return 
        else:
            #Checking that = is present after identifier 
            if (token[1] == '='):
                self.down = Node('operator', token, self.level+1)
            else:
                sys.exit('Error:: expected = after identifier')
                
            tokenList = []
            #Inserting <term> after = 
            token = tokenStream.lex()
            while (token != 'EOF'):
                tokenList.append(token)
                token = tokenStream.lex()
            postList = PostFixConverter.inToPost(tokenList)
            termNode = TermNode()
            termNode.insert(postList, self.level+1)
            termNode.evaluateExpr()
            self.right = termNode
    
    def printTree(self):
        print(' ' * self.level, self.value)
        if (self.left):
            self.left.printTree()
        if (self.down):
            self.down.printTree()
        if (self.right):
            self.right.printTree()        

#<term> -> <identifier>|<constant> {<operator> <term>}
class TermNode:
    def __init__(self):
        self.value = '<Term>'
        self.down = None
        self.left = None
        self.right = None
    
    def returnType(self):
        if (self.left != None):
            return self.left.returnType()
    
    def insert(self, tokenList, level):
        self.level = level
        self.tokenList = tokenList
        while (len(tokenList) > 0):
            if (self.right and self.left):
                return
            token = tokenList.pop()
            if (token[0] == 'operator'):
                if (self.down == None):
                    self.down = Node('operator', token, self.level+1)
                elif (self.left == None):
                    termNode = TermNode()
                    termNode.down = Node('operator', token, self.level+2)
                    termNode.insert(tokenList, level+1)
                    self.left = termNode
                elif (self.right == None):
                    termNode = TermNode()
                    termNode.down = Node('operator', token, self.level + 2)
                    termNode.insert(tokenList, level+1)
                    self.right = termNode
            elif (token[0] == 'identifier' or token[0] == 'constant'):
                if (self.left == None):
                    self.left = Node(token[0], token, self.level + 2)
                elif (self.right == None):
                    self.right = Node(token[0], token, self.level + 2)
                else:
                    tokenList.append(token)
                    return
        
    def evaluateExpr(self):
        if (len(self.tokenList) > 0):
            sys.exit('Error:: missing operator(s)')

        if (self.right == None and self.left == None):
            sys.exit('Error:: invalid expression missing identifier/constant')
        
        if (self.down != None and (self.right == None or self.left == None)):
            sys.exit('Error:: invalid expression missing identifier/constant')
            
        
        if (self.down):
            if (self.down.evaluateExpr() == '('):
                sys.exit('Error:: missing parentheses')
            elif (self.down.evaluateExpr() == ')'):
                sys.exit('Error:: missing parentheses')
        
        
    def printTree(self):
        print(' ' * self.level, self.value)
        if (self.right):
            self.right.printTree()
        if (self.down):
            self.down.printTree()
        if (self.left):
            self.left.printTree()