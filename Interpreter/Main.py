'''
Created on Nov 15, 2020

@author: Joshua
'''
from Parser import Parser
from SymbolTable import TableBuilder

Parse = Parser()
root = Parse.parse()
tableBuilder = TableBuilder(root)
tableBuilder.addSymbols()