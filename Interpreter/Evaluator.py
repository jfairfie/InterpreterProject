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
#                     print(branch.returnData(self.symbolTable))
                    value = branch.returnData(self.symbolTable)
            