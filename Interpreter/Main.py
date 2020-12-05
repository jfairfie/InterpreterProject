'''
@author: Joshua
'''
from Parser import Parser
from SymbolTable import TableBuilder
from Evaluator import Evaluator
from PostFixConverter import inToPost
from LexicalAnalyzer import Lexer

# ''' Creating Parse Tree '''
Parse = Parser('TestProgram.txt')
root = Parse.parse()
root.printTree()
  
''' Creating Symbol Table '''
tableBuilder = TableBuilder(root)
tableBuilder.addSymbols()
# tableBuilder.printTable()
  
  
''' Running Evaluation '''
symbolTable = tableBuilder.returnTable()
eval = Evaluator(root, symbolTable)
eval.evaluate()