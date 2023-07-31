from Core import Core

# The code uses the (1) approach, read entire character stream from file and store the tokens in 
# the tokenList
tokenList = []
# List to store all the identifiers
identifierList = []
# List to store all the constants
constantList = []

class Scanner:
  # Constructor should open the file and find the first token
  def __init__(self, filename):
    # Open the file to read
    f = open(filename, "r")
    # While loop to read character until the end of the file
    while 1:
      # Read by character
      char = f.read(1)
      # Reached the end of the file, stop loop
      if not char:
        tokenList.append(Core.EOS)
        break
      # Char is a special character, return corresponding token
      if char == ';':
        tokenList.append(Core.SEMICOLON)
      elif char == ',':
        tokenList.append(Core.COMMA)
      elif char == '!':
        tokenList.append(Core.NEGATION)
      elif char == '+':
        tokenList.append(Core.ADD)
      elif char == '-':
        tokenList.append(Core.SUB)
      elif char == '*':
        tokenList.append(Core.MULT)
      elif char == '(':
        tokenList.append(Core.LPAREN)
      elif char == ')':
        tokenList.append(Core.RPAREN)
      elif char == '{':
        tokenList.append(Core.LBRACE)
      elif char == '}':
        tokenList.append(Core.RBRACE)
      # Char is =, peek next character y
      elif char == '=':
        prev = f.tell()
        y = f.read(1)
        if y != '=':
          # Reset the scanner position
          f.seek(prev)
          tokenList.append(Core.ASSIGN)
        else:
          tokenList.append(Core.EQUAL)
      # Char is <, peek next character y
      elif char == '<':
        prev = f.tell()
        y = f.read(1)
        if y != '=':
          # Reset the scanner position
          f.seek(prev)
          tokenList.append(Core.LESS)
        else:
          tokenList.append(Core.LESSEQUAL)
      # Char is a letter
      elif char.isalpha():
        prev = f.tell()
        string = ""
        while char.isalpha() or char.isdigit():
          # Append the letter or digit to string
          string = string + char
          # Read next char
          char = f.read(1)
          # Increment the previous character position
          prev += 1
        # Reset the scanner position
        f.seek(prev - 1)
        # Check if the string is a keyword
        if string == "program":
          tokenList.append(Core.PROGRAM)
        elif string == "begin":
          tokenList.append(Core.BEGIN)
        elif string == "end":
          tokenList.append(Core.END)
        elif string == "new":
          tokenList.append(Core.NEW)
        elif string == "int":
          tokenList.append(Core.INT)
        elif string == "define":
          tokenList.append(Core.DEFINE)
        elif string == "ref":
          tokenList.append(Core.REF)
        elif string == "instance":
          tokenList.append(Core.INSTANCE)
        elif string == "if":
          tokenList.append(Core.IF)
        elif string == "then":
          tokenList.append(Core.THEN)
        elif string == "else":
          tokenList.append(Core.ELSE)
        elif string == "while":
          tokenList.append(Core.WHILE)
        elif string == "or":
          tokenList.append(Core.OR)
        elif string == "and":
          tokenList.append(Core.AND)
        elif string == "input":
          tokenList.append(Core.INPUT)
        elif string == "output":
          tokenList.append(Core.OUTPUT)
        elif string == "share":
          tokenList.append(Core.SHARE)
        # The string is an identifier
        else:
          tokenList.append(Core.ID)
          identifierList.append(string)
      # Char is a digit
      elif char.isdigit():
        prev = f.tell()
        num = ""
        while char.isdigit():
          # Append the digit to the string
          num = num + char
          char = f.read(1)
          # Increment the previous character position
          prev += 1
        # Reset the scanner position
        f.seek(prev - 1)
        # Check if the number is in the range
        if 0 <= int(num) <= 255:
          tokenList.append(Core.CONST)
          constantList.append(int(num))
        else:
          print("ERROR: Constants out of range error")
          tokenList.append(Core.ERROR)
          break
      # Handle invaild characters error
      elif char in "~`@#$%^&_[]|:\"\'.?/":
        print("ERROR: invalid character error with:" + char)
        tokenList.append(Core.ERROR)
        break

    # Close the file to read
    f.close()

  # nextToken should advance the scanner to the next token
  def nextToken(self):
    tokenList.pop(0)

  # currentToken should return the current token
  def currentToken(self):
    return tokenList[0]

  # If the current token is ID, return the string value of the identifier
	# Otherwise, return value does not matter
  def getID(self):
    
    identifier = identifierList[0] 
    identifierList.pop(0)
    return identifier

  # If the current token is CONST, return the numerical value of the constant
	# Otherwise, return value does not matter
  def getCONST(self):
    
    constant = constantList[0] 
    constantList.pop(0)
    return constant
