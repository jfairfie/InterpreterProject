'''
@author: Joshua
'''

import sys 
class Lexer():
    #Characters stores each character of input string 
    characters = [] 
    index = 0 
    lexeme = ''
    
    #Input: char[] source_code, 
    def __init__(self, source_code):
        self.characters = source_code 
    
    #Runs lexical analysis
    def lex(self):
        self.lexeme = ''
        
        if (len(self.characters) > 0):
            char = self.getCurrentChar()
        elif ('\n'):
            return 'EOF'
        else:
            return 'EOF'
        
        while (char == ' '):
            if (len(self.characters) > 1):
                self.characters = self.characters[1:len(self.characters)]
                char = self.getCurrentChar()
            else:
                return 'EOF'
        
        #Checking if character is operator/comment 
        if (self.lookup(char) != None):
            while (self.lookup(char)):
                self.characters = self.characters[1:len(self.characters)]
                self.lexeme += char 
                if (self.lexeme == '(' or self.lexeme == ')'):
                    token = self.lookup(self.lexeme)
                    return (token[0], token[1])
                char = self.getCurrentChar()
                #Looks for comment and returns 'EOF' if found 
                if (self.lookup(self.lexeme)[0] == 'comment'):
                    return 'EOF'
            
            token = self.lookup(self.lexeme)
            return (token[0], token[1])
        
        #Checking if character is constant 
        elif (char.isdigit() or char == '.'):
            if (char == '.'):
                comma = True 
            else:
                comma = False 
            while (char.isdigit() and len(self.characters) > 0):
                self.lexeme += char
                self.characters = self.characters[1:len(self.characters)]
                char = self.getCurrentChar()
                if (char == '.' and comma == False):
                    self.lexeme += char
                    self.characters = self.characters[1:len(self.characters)]
                    char = self.getCurrentChar()
                    comma = True
                elif (char == '.' and comma == True):
                    sys.exit('Error:: double contains too many periods')
            if (char.isalpha() and len(self.characters) > 0):
                sys.exit('Error, number cannot precede number in naming identifiers')
            
            if (comma == True):
                return ('constant', float(self.lexeme))
            else:
                return ('constant', int(self.lexeme))
        #Checking if character is identifier or keyword
        elif (char.isalpha() or char == '_'):
            while ((char.isalpha() or char.isdigit() or char == '_') and len(self.characters) > 0):
                self.lexeme += char 
                self.characters = self.characters[1:len(self.characters)]
                char = self.getCurrentChar()
            if (self.keywordLookup(self.lexeme) != None):
                token = self.keywordLookup(self.lexeme)
                return(token[0], token[1])
            else:
                return('identifier', self.lexeme)
        
    def getCurrentChar(self):
        if (len(self.characters) == 0):
            return 'EOF'
        char = self.characters[0]
        return char

    #Input: char character 
    #Checks if cha    racter is operator, using dictionary 
    def lookup(self, character):
        operatorDict = {'+':['operator', '+'], '-':['operator', '-'], '/':['operator', '/'], '*':['operator','*'], 
                        '(':['operator','('], ')':['operator',')'], '{':['operator','{'], '}':['operator','}'],
                        '=':['operator','='], '//':['comment','//'], '*=':['operator', '*='], '+=':['operator','+='],
                        '-=':['operator','-='], '/=':['operator','/='], '%':['operator', '%'], '==':['operator', '=='], 
                        '<':['operator','<'], '>':['operator','>'], '<=':['operator','<='], '>=':['operator','>=']}
        
        #Returns key, else returns None 
        try:
            return operatorDict[character]
        except Exception:
            return None
        
    def keywordLookup(self, keyword):
        keywordDict = {'var':['keyword', 'var'], 'if':['keyword','if'], 'print':['keyword','print'], 
                       'endif':['keyword', 'endif'], 'else':['keyword','else'], 'elif':['keyword', 'elif'], 
                       'and':['keyword','and'], 'or':['keyword','or']}
        
        try:
            return keywordDict[keyword]
        except Exception:
            return None