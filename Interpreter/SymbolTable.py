'''
@author: jfairfie
'''
import sys

class SymbolTable:
    #Symbol table uses a simple linked list
    def __init__(self):
        self.front = None 
    
    def insertSymbol(self, name, category, type):
        if (self.front == None):
            self.front = Symbol(name, category, type)
        else: 
            head = self.front 
            
            while (head.next):
                head = head.next
                
            head.next = Symbol(name, category, type)
        
    def emptyAll(self):
        self.front = None
        
    #Returns symbol node of linked list
    def lookUpName(self, name):
        head = self.front
        while (head != None):
            if (head.name == name):
                return head
            head = head.next
        return None
    
    #Removes symbol 
    def removeSymbol(self, name):
        if (self.front == None):
            return 
        elif (self.front.next == None and self.front.returnName() == name):
            self.front = None 
    
    #Sets attribute of either type or category
    def setAttribute(self, name, Type, Category):
        if (Type != None):
            node = self.lookUpName(name)
            node.setType(Type)
        
        if (Category != None):
            node = self.lookUpName(name)
            node.setCategory(Category)
    
    #Function creates output file for symbol table 
    def outputFile(self):
        head = self.front
        output = open('output.txt', 'w+')
        output.write('---Symbol Table---')
        while (head != None):
            output.write('\n' + head.returnName() + ' ' + head.returnType() + ' ' + head.returnCategory())
            head = head.next
        output.close()
            
    #Function simply prints symbol table (linked list)
    def printList(self):
        head = self.front 
        while (head != None):
            head.printData()
            head = head.next
    
        
class Symbol:
    #Name - name 
    #Category - variable, procedure, etc. 
    #Type - type checking 
    def __init__(self, name, category, type):
        self.type = type
        self.name = name 
        self.category = category
        self.value = None
        self.next = None 
    
    def insertValue(self, value):
        self.value = value
    
    def returnValue(self):
        return self.value
    
    def returnCategory(self):
        return self.category
    
    def setCategory(self, category):
        self.category = category 
    
    def returnName(self):
        return self.name
     
    def returnType(self):
        return self.type
    
    def setType(self, type):
        self.type = type 
    
    def insertAfter(self, link):
        self.next = link
    
    def printData(self):
        print(self.name, self.category, self.type, self.value)
    
#Builds symbol table from root node of parse tree 
class TableBuilder:
    def __init__(self, root):
        self.root = root
        self.symbolTable = SymbolTable()
    
    def printTable(self):
        self.symbolTable.printList()
    
    def addSymbols(self):
        #Visiting Program 
        cursor = self.root 
        #Vising stmts 
        cursor = cursor.down
        branches = cursor.branches 
        
        #Going to statement branches 
        for branch in branches:
            if (branch.value == '<VarAssign>' or branch.value == '<IdentifierAssign>'):
                symbol = branch.left.returnType()
                if (branch.value == '<IdentifierAssign>' and self.symbolTable.lookUpName(symbol[1]) == None):
                    sys.exit('Error:: variable not declared')
                
                if (self.symbolTable.lookUpName(symbol[1]) == None):
                    self.symbolTable.insertSymbol(symbol[1], symbol[0], None)
                name = symbol[1]
                
                if (branch.right):
                    cursor = branch.right
                    
                    list = []
                    
                    #Taking potentially nested list and turning into flat list
                    self.output = []
                    list = cursor.returnType()
                    self.removeNested(list)
                    list = self.output
                    check = None
                    for x in range(len(list)):
                        if (type(list[x]) == int or type(list[x]) == float):
                            check = type(list[x])
                    
                    if (check == None):
                        if (self.symbolTable.lookUpName(list[0]) != None):
                            if (self.symbolTable.lookUpName(list[0]).returnType() == 'Integer'):
                                check = type(1)
                            elif (self.symbolTable.lookUpName(list[0]).returnType() == 'Float'):
                                check = type(1.0)
                        else:
                            sys.exit('Error:: symbol ' + str(list[0]) + ' not initialized')
                        
                    for symbol in list:
                        if (type(symbol) == str):
                            if (self.symbolTable.lookUpName(symbol) == None):
                                sys.exit('Variable ' + str(symbol) + ' unknown symbol') 
                            elif (self.symbolTable.lookUpName(symbol) != None and self.symbolTable.lookUpName(symbol).returnType() == None):
                                sys.exit ('Variable ' + str(symbol + ' is not initialized'))
                            
                            if (self.symbolTable.lookUpName(symbol).returnType() == 'Integer'):
                                symbol = 1
                            elif (self.symbolTable.lookUpName(symbol).returnType() == 'Float'):
                                symbol = 1.0
                        
                        if (type(symbol) != check):
                            sys.exit('Error:: cannot have ' + str(check) + ' in a ' + str(type(symbol)) + ' expression')
        
                    if (check == int):
                        self.symbolTable.setAttribute(name, 'Integer', None)
                    elif (check == float):
                        self.symbolTable.setAttribute(name, 'Float', None)
        #Purpose of output file is just to show what has happened 
        self.symbolTable.outputFile()
    
    def removeNested(self, l):
        for item in l:
            if (type(item) == list):
                self.removeNested(item)
            else:
                self.output.append(item[1])
                
    '''
    Returns what kind of type an expression is, 
    Integer, Double, etc. 
    '''
    def evaluateExpr(self, root):
        cursor = root
        if (root.value == '<VarAssign>' or root.value == '<IdentifierAssign>'):
            if (root.right):
                cursor = cursor.right 
                if (cursor.left.value == '<constant>'):
                    token = cursor.left.returnType()
#                     print(type(token[1]), token[1])
            else:
                return None
            return 'Integer'
    
    def returnTable(self):
        return self.symbolTable