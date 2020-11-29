'''
Created on Nov 27, 2020

@author: jfairfie
'''
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
        self.next = None 
    
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
        print(self.name, self.category, self.type)

#Builds symbol table from root node of parse tree 
class TableBuilder:
    def __init__(self, root):
        self.root = root
        self.symbolTable = SymbolTable()
    
    def addSymbols(self):
        cursor = self.root 
        cursor = cursor.down
        branches = cursor.branches 
        
        for branch in branches:
            symbol = branch.left.returnType()
            if (symbol[0] == 'identifier'):
                if (branch.right):
#                     print(branch.right.returnType())
                    if (self.symbolTable.lookUpName(symbol[1])):
                        self.symbolTable.setAttribute(symbol[1], 'integer', None)
#                         print('found', symbol(1))
#                         self.symbolTable.setAttribute(symbol[1], None, 'identifier')
                    else:
                        self.symbolTable.insertSymbol(symbol[1], symbol[0], 'integer')
                else:
                    #Variable declaration but not initialization 
                    self.symbolTable.insertSymbol(symbol[1], symbol[0], 'unknown')
        self.symbolTable.printList()
                
    