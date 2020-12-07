''' 
@author: Joshua Fairfield 
'''

class Evaluator:
    def __init__(self, root, symbolTable):
        self.head = root.down 
        self.symbolTable = symbolTable

        
    def evaluate(self): 
        branches = self.head.branches
        for branch in branches:
            ''' Arithmetic '''
            if (branch.value == '<VarAssign>' or branch.value == '<IdentifierAssign>'):
                if (branch.right):
                    value = branch.returnData(self.symbolTable)
            if (branch.value == '<IfStmt>'):
                self.evaluateIfStmt(branch)
        self.symbolTable.outputFile()
    
    def evaluateIfStmt(self, branch):
        elifNodes = branch.elifBranches
        bool = branch.expression.returnExpression(self.symbolTable)
        boolBranch = None
        if (bool == True):
            boolBranch = branch
        
        if (bool == False):
            x = 0 
            while (bool == False and x < len(elifNodes)):
                if (elifNodes[x].value == '<else>'):
                    bool = True 
                    boolBranch = elifNodes[x]
                else:
                    bool = elifNodes[x].expression.returnExpression(self.symbolTable)
                    boolBranch = elifNodes[x]
                x += 1

        if (bool == True):
            for b in boolBranch.stmts.branches:
                if (b.value == '<VarAssign>' or b.value == '<IdentifierAssign>'):
                    if (b.right):
                        value = b.returnData(self.symbolTable)
                elif (b.value == '<IfStmt>'):
                    self.evaluateIfStmt(b)
        self.symbolTable.outputFile()