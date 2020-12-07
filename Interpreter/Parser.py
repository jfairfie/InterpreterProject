'''
@author: jfairfie
'''
from LexicalAnalyzer import Lexer
import sys
import PostFixConverter
import symbol

class Parser():
    def __init__(self, file):
        self.root = ProgramNode()
        self.file = file 
    
    #Parse creates a parse tree, returns the root of the tree 
    def parse(self):
        f = open(self.file)
        tokenList = f.read().splitlines()        
        
        for tList in tokenList:
            Lex = Lexer(list(tList))
            token = Lex.lex()
            
            while (token != 'EOF'):
                #Checking for function 
                self.root.insert(token, Lex)
                token = Lex.lex()
        
        f.close()
        
        return self.root
    
#First Node of Program 
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
    
    ''' === Reading Tokens to Insert ==='''
    def insert(self, token, tokenStream, level):
        self.level = level
        if (len(self.branches) > 0 and self.branches[len(self.branches)-1].value == '<IfStmt>' and self.branches[len(self.branches)-1].getInFunction() == True):
            branch = self.branches[len(self.branches)-1]
            branch.insert(token, tokenStream, level)
        elif (token[1] == 'if'):
            token = tokenStream.lex()
            expressNode = ExpressionNode()
            token = tokenStream.lex()
            expressNode.insert(token, tokenStream, level+1)
            ifNode = IfNode()
            ifNode.insertExpression(expressNode, level+1)
            self.branches.append(ifNode)
        elif (token[1] == 'elif'):
            self.branches[len(self.branches)-1].insert(token, tokenStream, level)
        #Variable initialization
        elif (token[1] == 'var'):
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

    def getInFunction(self):
        for branch in self.branches:
            if (branch.value == '<IfStmt>'):
                return branch.getInFunction()
        
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
    
    def returnData(self, symbolTable=None, symbol=None):
        return self.data
    
    def returnExpression(self, symbolTable = None):
        return self.data
    
    def returnType(self):
        return (self.type, self.data)
    
    def evaluateExpr(self):
        return self.data
    
    def printTree(self):
        print(' ' * self.level, self.value)
        print(' ' * (self.level + 1), self.data)

''' IF NODE '''
class IfNode:
    def __init__(self):
        self.value = '<IfStmt>'
        self.elifBranches = []
        self.stmts = None
        self.expression = None
        self.inFunction = True
    
    def insertExpression(self, expressionNode, level):
        self.expression = expressionNode
        self.level = level
        
    def insert(self, token, tokenStream, level):
        if (token[1] == 'endif'):  
            if (self.stmts == None):
                sys.exit('Error:: if statement contains no body')
            if (self.inFunction):
                self.inFunction = False 
            elif (self.inFunction == False):
                for branch in self.elifBranches:
                    branch.inFunction = False
        
        if (token[1] == 'elif'):
            self.inFunction = False 
            elifNode = IfNode()
            token = tokenStream.lex()
            expressionNode = ExpressionNode()
            token = tokenStream.lex()
            expressionNode.insert(token, tokenStream, level)
            elifNode.insertExpression(expressionNode, level)
            elifNode.value = '<elif>'
            self.elifBranches.append(elifNode)
        elif (token[1] == 'else'):
            self.inFunction = False 
            elseNode = IfNode()
            elseNode.value = '<else>'
            elseNode.level = self.level
            self.elifBranches.append(elseNode)
        elif(token[1] != 'endif'):
            #Insert elements into current function 
            if (self.inFunction == False):
                self.elifBranches[len(self.elifBranches)-1].insert(token, tokenStream, level)
            else:
                if (self.stmts == None):
                    self.stmts = StmtsNode()
                self.stmts.insert(token, tokenStream, level+1)
    
    def getInFunction(self):
        if (self.inFunction == True):
            return True
        for branch in self.elifBranches:
            if (branch.inFunction == True):
                return True
        
        return False
    
    def printTree(self):
        print('--- stmt ---')
        print(' ' * self.level, self.value)
        if (self.value != '<else>'):
            self.expression.printTree()
        for ifNode in self.elifBranches:
            ifNode.printTree()
        self.stmts.printTree()
        print('--- endstmt ---')
#ExpressionNode is for IfStmt expression 
#<Expression> -> <term> <operator> <term> {and|or <Expression>}
class ExpressionNode:
    def __init_(self):
        #Operator 
        self.value = '<Expression>'
        self.left = None 
        self.down = None 
        self.right = None
        #cont is continued expression 
        #contkey is either "and" or "or" 
        self.contKey = None
        self.cont = None 
    
    def returnExpression(self, symbolTable):
        #Operator, left side, right side 
        operator = self.down.returnType()[1]
        left = self.left 
        right = self.right 

        if (self.contKey):
            key = self.contKey.returnExpression(symbolTable)
            contExpression = self.cont.returnExpression(symbolTable)
        
        left = self.left.returnExpression(symbolTable)
        right = self.right.returnExpression(symbolTable)
        
        if (operator == '>'):
            if (self.cont):
                if (key == 'and'):
                    return left > right and contExpression
                elif (key == 'or'):
                    return left > right or contExpression
                else:
                    sys.exit('Error:: invalid expression in if stmt')
            else:
                return left > right
        elif (operator == '<'):
            if (self.cont):
                if (key == 'and'):
                    return left < right and contExpression
                elif (key == 'or'):
                    return left < right or contExpression
                else:
                    sys.exit('Error:: invalid expression in if stmt')
            else:
                return left < right
        elif (operator == '>='):
            if (self.cont):
                if (key == 'and'):
                    return left >= right and contExpression
                elif (key == 'or'):
                    return left >= right or contExpression
                else:
                    sys.exit('Error:: invalid expression in if stmt')
            else:
                return left >= right
        elif (operator == '<='):
            if (self.cont):
                if (key == 'and'):
                    return left <= right and contExpression
                elif (key == 'or'):
                    return left <= right or contExpression
                else:
                    sys.exit('Error:: invalid expression in if stmt')
            else:
                return left <= right
        elif (operator == '=='):
            if (self.cont):
                if (key == 'and'):
                    return left == right and contExpression
                elif (key == 'or'):
                    return left == right or contExpression
                else:
                    sys.exit('Error:: invalid expression in if stmt')
            else:
                return left == right
    
    def insert(self, token, tokenStream, level):
        self.level = level
        tokens = []
        
        ''' first <term> '''
        while (self.isComparison(token) == False):
            tokens.append(token)
            token = tokenStream.lex()
            if (token == 'EOF'):
                sys.exit('Error:: invalid syntax in if stmt')
            
            if (token[0] == 'keyword'):
                sys.exit('Error:: invalid syntax in if stmt')
        
        if (len(tokens) == 0):
            sys.exit('Error:: missing identifier or constant')
        
        termNode = TermNode()
        postList = PostFixConverter.inToPost(tokens)
        termNode.insert(postList, self.level+1)
        termNode.evaluateExpr()
        self.left = termNode
        tokens.clear()
        
        ''' Comparison Operator ''' 
        if (self.isComparison(token) == False):
            sys.exit('Error:: expected comparison operator')
        self.down = Node('operator', token, self.level+1)
        token = tokenStream.lex()

        ''' second <term> '''
        while (token[1] != 'and' and token[1] != 'or' and token[1] != ')'):
            tokens.append(token)
            token = tokenStream.lex()
            if (token == 'EOF'):
                sys.exit('Error:: syntax error in if stmt')
        
        if (len(tokens) == 0):
            sys.exit('Error:: missing identifier or constant')
        termNode = TermNode()
        postList = PostFixConverter.inToPost(tokens);
        termNode.insert(postList, self.level+1)
        termNode.evaluateExpr()        
        self.right = termNode

        if (token[1] == 'and' or token[1] == 'or'):
            self.contKey = Node('keyword', token, self.level+1)
            expressionNode = ExpressionNode()
            token = tokenStream.lex()
            expressionNode.insert(token, tokenStream, self.level+1)
            self.cont = expressionNode
        else:
            self.contKey = None 
            self.cont = None
    
        token = tokenStream.lex()
        
    
    def isComparison(self, token):
        if (token[1] == '<' or token[1] == '>' or token[1] == '==' or token[1] == '<=' or token[1] == '>='):
            return True 
        return False 
        
    def printTree(self):
        self.left.printTree()
        self.down.printTree()
        self.right.printTree()
        if (self.cont):
            self.contKey.printTree()
            self.cont.printTree()

#Variable assignment 
class AssignNode:
    def __init__(self):
        self.value = '<VarAssign>'
        self.left = None 
        self.down = None 
        self.right = None 
    
    def returnData(self, symbolTable):
        name = self.left.data 
        symbol = symbolTable.lookUpName(name)
        value = self.right.returnData(symbolTable, symbol)
        symbol.insertValue(value)
        return value
    
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
    
    def returnData(self, symbolTable, symbol):
        if (self.down != None):
            left = self.left.returnData(symbolTable, symbol)
            right = self.right.returnData(symbolTable, symbol)
            
            if (type(left) == str):
                left = symbolTable.lookUpName(left).returnValue()
                if (left == None):
                    sys.exit('Error:: uninitialized variable')
                
            if (type(right) == str):
                right = symbolTable.lookUpName(right).returnValue()
                if (right == None):
                    sys.exit('Error:: uninitialized variable')
            
            if (self.down.data == '+'):
                return left + right
            
            elif (self.down.data == '*'):
                return left * right 
            
            elif (self.down.data == '/'):
                if (symbol.returnType() == 'Integer'):
                    return right // left
                else:    
                    return right / left
        
            elif (self.down.data == '-'):
                return right - left
            
            elif (self.down.data == '%'):
                return right % left
        else:
            if (self.left):
                return self.left.returnData(symbolTable)
            else:
                return self.right.returnData(symbolTable)
    
    def returnExpression(self, symbolTable):
        if (self.down == None):
            if (self.left):
                if (self.right):
                    sys.exit('Error:: missing operator')
                value = self.left.data
                if (type(value) == str):
                    value = symbolTable.lookUpName(value)
                    if (value == None):
                        sys.exit('Error:: identifier not initialized')
                    else:
                        return value.returnValue()
                return value
            else:
                sys.exit('Error:: syntax error in if stmt expression')
        if (self.down):
            left = self.left.returnExpression(symbolTable)
            right = self.right.returnExpression(symbolTable)
            operator = self.down.data
            
            if (type(left) == str):
                left = symbolTable.lookUpName(left).returnValue()
            if (type(right) == str):
                right = symbolTable.lookUpName(right).returnValue()

            if (operator == '+'):
                return left + right
            elif (operator == '*'):
                return left * right
            elif (operator == '/'):
                return right // left 
            elif (operator == '-'):
                return right - left
            elif (operator == '%'):
                return right % left 
            else:
                sys.exit('Error:: unknown operator')
                
    
    #Returns an array of the types of data located in tree 
    #Used for creation of symbol table
    def returnType(self):
        tokenList = []
        if (self.left):
            token = self.left.returnType()
            if (token != None):
                tokenList.append(token)
        if (self.right):
            token = self.right.returnType()
            if (token != None):
                tokenList.append(token)
        return tokenList
    
    #Inserts data into node 
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
            elif (token[0] == 'identifier'):
                if (self.left == None):
                    self.left = Node(token[0], token, self.level + 2)
                elif (self.right == None):
                    self.right = Node(token[0], token, self.level + 2)
                else:
                    tokenList.append(token)
                    return
            elif (token[0] == 'constant'):
                if (self.left == None):
                    self.left = Node(token[0], token, self.level + 2)
                elif (self.right == None):
                    self.right = Node(token[0], token, self.level + 2)
                else:
                    tokenList.append(token)
                    return
    
    #Evaluates mathematical expression, ensuring syntax 
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