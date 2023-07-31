from Scanner import Scanner
from Core import Core
import sys

def main():
  # Initialize the scanner with the input file
  S = Scanner(sys.argv[1])

  # Initialize the semantic check 
  sc = SemanticCheck()
  # Initialize the program instance to start parsing
  prog = Prog()
  prog.parse(S, sc)

  # Print out the program from the parse tree (No longer needed for Project 3)
  # prog.print()

  # Initialize the scanner to scan the user input file 
  S2 = Scanner(sys.argv[2])
  # Initialize the executor for the programm
  E = executor()
  # Execute the program and produce the result
  prog.execute(E, S2, sc)

# Executor class simulate the memory of the program. It contains 3 fields:
# A map for gloable variables, a stack of dictionaries for local variables, and a
# list used as heap to store reference variables 
class executor:
  # Map string:int for global variables
  static = {}
  # Stack of dictionaries for local variable
  stack = []
  # List represent the heap of the program
  heap = []
  # stack to store all the ref variable of the program
  refList = []
  def refExist(self, id):
    for l in self.refList:
      for e in l:
        if e == id:
          return True
    return False



# Program class has two methods, parse() method to parse the program 
# and print() method to print the program
class Prog:

  # Parse method
  def parse(self, S, sc):
    # Initialize the declaration and statement instance the program might includes
    self.ds = DeclSeq()
    self.ss = StmtSeq()
    self.hasDs = False
    
    # Current token is not program, stop execute
    if S.currentToken() != Core.PROGRAM:
      print("ERROR: Expect keyword PROGRAM instead " + S.currentToken().name)
      sys.exit()
    # Move to check next token
    S.nextToken()

    # Current token is not left brace, stop execute
    if S.currentToken() != Core.LBRACE:
      print("ERROR: Expect keyword LBRACE instead " + S.currentToken().name)
      sys.exit()
    # Move to check next token
    S.nextToken()
    # Add a new scope of variables
    sc.addList()

    # If next token is not begin, then the decl-seq exists
    if S.currentToken() != Core.BEGIN:
      self.hasDs = True
      self.ds.parse(S, sc)
    
    # Current token is not begin, stop execute
    if S.currentToken() != Core.BEGIN:
      print("ERROR: Expect keyword BEGIN instead " + S.currentToken().name)
      sys.exit()
    # Move to check next token
    S.nextToken()

    # Current token is not left brace, stop execute
    if S.currentToken() != Core.LBRACE:
      print("ERROR: Expect keyword LBRACE instead " + S.currentToken().name)
      sys.exit()
    # Move to check next token
    S.nextToken()
    # Add a new scope of variables
    sc.addList()

    # Now parsing the stmt-seq
    self.ss.parse(S, sc)

    # Current token is not right brace, stop execute
    if S.currentToken() != Core.RBRACE:
      print("ERROR: Expect keyword RBRACE instead " + S.currentToken().name)
      sys.exit()
    # Move to check next token
    S.nextToken()
    # Discard a scope of id
    sc.remList()

    # Current token is not right brace, stop execute
    if S.currentToken() != Core.RBRACE:
      print("ERROR: Expect keyword RBRACE instead " + S.currentToken().name)
      sys.exit()
    # Move to check next token
    S.nextToken()
    # Discard a scope of id
    sc.remList()

    # Current token is not EOS, stop execute. If there is one, the program is done.
    if S.currentToken() != Core.EOS:
      print("ERROR: Expect keyword EOS instead " + S.currentToken().name)
      sys.exit()

  # Print method print out the program in somewhat neat format.
  def print(self):
    print("program {")
    # Check if there is decl-seq need to be printed
    if self.hasDs:
      self.ds.print()

    print("  begin {")
    # Print out the stmt-seq
    self.ss.print()
    print("  }")
    print("}")

  # Execute method to execute the program class
  def execute(self, E, S2, sc):
    # Check if there is decl-seq need to be executed
    if self.hasDs:
      E.refList.append([])
      self.ds.execute(E, S2, sc)
    
    # Add new a new scope for local variables
    E.stack.append({})
    # Execute the statement sequence of the program
    E.refList.append([])
    self.ss.execute(E, S2, sc)
    # Remove all the main function scope variables
    E.refList.pop()
    E.stack.pop()

  
# DeclSeq class has two methods, parse() method to parse the declaration sequence
# and print() method to print the declaration sequence
class DeclSeq:

  # Parse method
  def parse(self, S, sc):
    self.decl = Decl()
    self.decl.parse(S, sc)

    self.newDeclSeq = DeclSeq()
    self.moreDeclSeq = False
    # Check there is still more declaration
    if S.currentToken() != Core.BEGIN:
      self.moreDeclSeq = True
      self.newDeclSeq.parse(S, sc)
  
  # Print method print out the program in somewhat neat format.
  def print(self):
    self.decl.print()
    # Check if there are more declaration to be printed
    if self.moreDeclSeq:
      self.newDeclSeq.print()

  # Execute method to execute the DeclSeq class
  def execute(self, E, S2, sc):
    isGlobal = True
    # Execute the declaration of the program
    self.decl.execute(E, S2, sc, isGlobal)

    # Check if there is more decl-seq need to be executed
    if self.moreDeclSeq:
      self.newDeclSeq.execute(E, S2, sc)
    
    


# StmtSeq class has two methods, parse() method to parse the statement sequence
# and print() method to print the statement sequence
class StmtSeq:
  # Parse method
  def parse(self, S, sc):
    # Create the statement object
    self.stmt = Stmt()
    self.stmt.parse(S, sc)

    self.newStmtSeq = StmtSeq()
    self.moreStmtSeq = False
    # Check there is still more statements
    if S.currentToken() != Core.RBRACE:       
      self.moreStmtSeq = True
      self.newStmtSeq.parse(S, sc)
  
  # Print method print out the program in somewhat neat format.
  def print(self):
    self.stmt.print()
    # Check if there are more statements to be printed
    if self.moreStmtSeq:
      self.newStmtSeq.print()

  # Execute method to execute the StmtSeq class
  def execute(self, E, S2, sc):
    # Execute the statement of the program
    self.stmt.execute(E, S2, sc)

    # Check if there is more statements need to be executed
    if self.moreStmtSeq:
      self.newStmtSeq.execute(E, S2, sc)


# Decl class has two methods, parse() method to parse the declaration
# and print() method to print the declaration
class Decl:
  # Parse method
  def parse(self, S, sc):
    # The data type is int
    self.decl = None
    if S.currentToken() == Core.INT:
      self.decl = DeclInt()
      self.decl.parse(S, sc)
    # The data type is ref
    elif S.currentToken() == Core.REF:
      self.decl = DeclRef()
      self.decl.parse(S, sc)
    else:
      print("ERROR: Expect keyword INT or REF instead " + S.currentToken().name)
      sys.exit()

  # Print method print out the declaration in somewhat neat format.
  def print(self):
    self.decl.print()

  # Execute method to call execute method of the decl-int or decl-ref class
  def execute(self, E, S2, sc, isGlobal):
    self.decl.execute(E, S2, sc, isGlobal)



# DeclInt class has two methods, parse() method to parse the int declaration
# and print() method to print the int declaration
class DeclInt:
  # Parse method
  def parse(self, S, sc):
    
    # Current token is not INT, stop execute.
    if S.currentToken() != Core.INT:
      print("ERROR: Expect keyword INT instead " + S.currentToken().name)
      sys.exit()
    # Consume the INT token
    S.nextToken()

    # Parse the id-list
    self.idList = IdList()
    # Add the new ids for semantic check
    newId = []
    self.idList.parse(S, sc, newId, True)
    sc.addToCurrentInt(self.idList.getIdList())


    # Current token is not SEMICOLON, stop execute.
    if S.currentToken() != Core.SEMICOLON:
      print("ERROR: Expect keyword SEMICOLON instead " + S.currentToken().name)
      sys.exit()
    # Consume the semicolon token
    S.nextToken()
  
  # Print method print out the int declaration in somewhat neat format.
  def print(self):
    print("  int ", end = ' ') # Make the declaration in the same line
    self.idList.print()
    print(";")

  # Execute method to call execute of the id-list class
  def execute(self, E, S2, sc, isGlobal):
    self.idList.execute(E, S2, sc, isGlobal)


# DeclRef class has two methods, parse() method to parse the ref declaration
# and print() method to print the ref declaration
class DeclRef:
  # Parse method
  def parse(self, S, sc):

    # Current token is not REF, stop execute.
    if S.currentToken() != Core.REF:
      print("ERROR: Expect keyword REF instead " + S.currentToken().name)
      sys.exit()
    # Consume the REF token
    S.nextToken()

    # Parse the id-list
    self.idList = IdList()
    # Add the new ids for semantic check
    newId = []
    self.idList.parse(S, sc, newId, False)
    sc.addToCurrentRef(self.idList.getIdList())

    # Current token is not SEMICOLON, stop execute.
    if S.currentToken() != Core.SEMICOLON:
      print("ERROR: Expect keyword SEMICOLON instead " + S.currentToken().name)
      sys.exit()
    # Consume the semicolon token
    S.nextToken()
  
  # Print method print out the ref declaration in somewhat neat format.
  def print(self):
    print("  ref ", end = ' ') # Make the declaration in the same line
    self.idList.print()
    print(";")
  
  # Execute method to call execute of the id-list class
  def execute(self, E, S2, sc, isGlobal):
    E.refList[len(E.refList) - 1].extend(self.idList.getIdList())
    self.idList.execute(E, S2, sc, isGlobal)


# IdList class has two methods, parse() method to parse the id 
# and print() method to print the id 
class IdList:
  # Parse method
  def parse(self, S, sc, newId, isInt):
    self.newIdList = IdList()
    self.moreIdlist = False
    self.id = None
    self.newIds = newId
    self.dataType = isInt
    # Current token is not ID, stop execute.
    if S.currentToken() != Core.ID:
      print("ERROR: Expect keyword ID instead " + S.currentToken().name)
      sys.exit()
    # Consume the ID token
    S.nextToken()
    self.id = S.getID()
    # Semantic check if the variable is double declared
    if sc.repeatCheck(self.id, self.dataType):
      print("ERROR: Variable " + self.id + " already declared")
      sys.exit()
    self.newIds.append(self.id)

    # Current token is not COMMA, there is a new id-list.
    if S.currentToken() == Core.COMMA:
      self.moreIdlist = True
      # Consume the COMMA token
      S.nextToken()
      self.newIdList.parse(S, sc, self.newIds, self.dataType)

  # Print method print out the id in somewhat neat format.
  def print(self):
    print(self.id , end = ' ') # Make the declaration in the same line
    # There are more than one id in the same line 
    if self.moreIdlist:
      print(", ", end = ' ')
      self.newIdList.print()

  # Get Id method to return the id for semantic check
  def getIdList(self):
    return self.newIds

  # Execute method to store the declared variables in its corresponding position
  def execute(self, E, S2, sc, isGlobal):
    # Global variables are store in static dictionary 
    if isGlobal:
      # The variable is int, no need to keep track
      if self.dataType:
        E.static.update({self.id: 0})
      else:
        E.static.update({self.id: None})

    else:
      # Local variables are stored in stack
      # The variable is int, no need to keep track
      if self.dataType:
        # Add the new variable pair on the top dictionary of the stack
        E.stack[len(E.stack) - 1].update({self.id: 0})
      else:
        # Add the new variable pair on the top dictionary of the stack
        E.stack[len(E.stack) - 1].update({self.id: None})

    # There are more than one id in the same line 
    if self.moreIdlist:
      self.newIdList.execute(E, S2, sc, isGlobal)




# Stmt class has two methods, parse() method to parse the statement 
# and print() method to print the statement 
class Stmt:
  # Parse method
  def parse(self, S, sc):
    self.stmt = None
    self.isDecl = False
    #Check tht type of the statement
    if S.currentToken() == Core.ID: # Assign
      self.stmt = Assign()
      self.stmt.parse(S, sc)
    elif S.currentToken() == Core.IF: # If
      self.stmt = If()
      self.stmt.parse(S, sc)
    elif S.currentToken() == Core.WHILE: # Loop
      self.stmt = Loop()
      self.stmt.parse(S, sc)
    elif S.currentToken() == Core.OUTPUT: # Output
      self.stmt = Out()
      self.stmt.parse(S, sc)
    elif S.currentToken() == Core.INT or S.currentToken() == Core.REF: # Decl
      self.isDecl = True
      self.stmt = Decl()
      self.stmt.parse(S, sc)
    # Invalid use of statement
    else:
      print("ERROR: Expect keyword of a statement instead " + S.currentToken().name)
      sys.exit()
  
  # Print method print out the statement in somewhat neat format.
  def print(self):
    self.stmt.print()

  # Execute method call the execute functions of statements
  def execute(self, E, S2, sc):
    if self.isDecl:
      isGlobal = False
      # This is declaration of local variables
      self.stmt.execute(E, S2, sc, isGlobal)
    else:
      # These are not new declaration, let execute method of their classes to handle
      self.stmt.execute(E, S2, sc)


# Assign class has two methods, parse() method to parse the assignment 
# and print() method to print the assignment 
class Assign:
  # Parse method
  def parse(self, S, sc):
    # Current token is not ID, stop execute.
    if S.currentToken() != Core.ID:
      print("ERROR: Expect keyword ID instead " + S.currentToken().name)
      sys.exit()
    # Consume the ID token
    S.nextToken()
    # Get the id name
    self.id = S.getID()
    # Semantic check that id already declared
    if not sc.existCheck(self.id, False) and not sc.existCheck(self.id, True):
      print("ERROR: " + self.id + " must be declared before assignment")
      sys.exit()

    # Current token is not assign, stop execute.
    if S.currentToken() != Core.ASSIGN:
      print("ERROR: Expect keyword ASSIGN instead " + S.currentToken().name)
      sys.exit()
    # Consume the ASSIGN token
    S.nextToken()

    self.isInstance = False
    self.isShare = False
    self.isExpr = False
    self.sharedId = None
    self.expr = Expr()
    # Check the type of the assignment
    if S.currentToken() == Core.NEW: # new instance
      self.isInstance = True
      # Semantic check to check IDs were declared with appropriate type
      if sc.existCheck(self.id, False):
        # Consume the NEW token
        S.nextToken()
        # Consume the INSTANCE token
        S.nextToken()
      else:
        print("ERROR: " + self.id + " must be declared as ref type")
        sys.exit()
    elif S.currentToken() == Core.SHARE: # share id
      self.isShare = True
      # Consume the SHARE token
      S.nextToken()
      # Consume the ID token
      S.nextToken()
      self.sharedId = S.getID()
      #Semantic check to check both ids are declared with appropriate type
      if not sc.existCheck(self.id, False):
        print("ERROR: " + self.id + " must be declared as ref type")
        sys.exit()
      elif not sc.existCheck(self.sharedId, False):
        print("ERROR: " + self.sharedId + " must be declared as ref type")
        sys.exit()

    else: # expr
      self.isExpr = True
      self.expr.parse(S, sc)

    # Current token is not SEMICOLON, stop execute.
    if S.currentToken() != Core.SEMICOLON:
      print("ERROR: Expect keyword SEMICOLON instead " + S.currentToken().name)
      sys.exit()
    # Consume the SEMICOLON token
    S.nextToken()

  # Print method print out the Assign in somewhat neat format.
  def print(self):
    print("    " + self.id + " = ", end = ' ')
    if self.isInstance:
      print("new instance;")
    elif self.isShare:
      print("share " + self.sharedId + ";")
    elif self.isExpr:
      self.expr.print()
      print(";")

  # Execute method to assign new values to declared variables.
  def execute(self, E, S2, sc):
    # Two options, the id is ref or int
    if E.refExist(self.id): # id is reference type

      # Three options: expr, new instance, or shared id
      if self.isExpr: # expr
        # Get value of expr
        value = self.expr.execute(E, S2, sc)
        # Two options: id is in stack or static
        found = False
        i = len(E.stack) - 1

        # Check stack first to ensure the variable hiding mechanism
        while i >= 0 and not found:          
          if self.id in E.stack[i].keys():
            # Found in local stack
            found = True
            # Error check: ref id can not point to null when assign to expr
            if E.stack[i].get(self.id) == None:
              print("ERROR: Assign a value to null ref variable: " + self.id)
              sys.exit()
            # Update the value on heap
            E.heap[E.stack[i].get(self.id)] = value
          i -= 1

        if not found:
          # Error check: ref id can not point to null when assign to expr
          if E.static.get(self.id) == None:
            print("ERROR: Assign a value to null ref variable: " + self.id)
            sys.exit()
          # id must in global variables
          E.heap[E.static.get(self.id)] = value
      
      elif self.isInstance: # new instance
        # Two options: id is in stack or static
        found = False
        i = len(E.stack) - 1

        # Check stack first to ensure the variable hiding mechanism
        while i >= 0 and not found:          
          if self.id in E.stack[i].keys():
            # Found in local stack
            found = True
            # Add new position on heap
            E.heap.append(0)
            # Update the value associate with the key to the index of the new 
            # last element on heap
            E.stack[i].update({self.id: (len(E.heap) - 1)})  
          i -= 1

        if not found:
          # id must in global variables
          # Add new position on heap
          E.heap.append(0)
          E.static.update({self.id: (len(E.heap) - 1)})  
      
      elif self.isShare: # shared id
        # Check shared id's value first
        # Two options: shared id is in stack or static
        found = False
        i = len(E.stack) - 1
        # Get value of sharedId
        value = 0

        # Check stack first to ensure the variable hiding mechanism
        while i >= 0 and not found:          
          if self.sharedId in E.stack[i].keys():
            # Found in local stack
            found = True
            # Get the value of the sharedId
            value = E.stack[i].get(self.sharedId)
          i -= 1

        if not found:
          # shared id must in global variables
          # Get the value of the sharedId
          value = E.static.get(self.sharedId)

        # Check id's existence now
        # Two options: shared id is in stack or static
        found = False
        i = len(E.stack) - 1 

        # Check stack first to ensure the variable hiding mechanism
        while i >= 0 and not found:          
          if self.id in E.stack[i].keys():
            # Found in local stack
            found = True
            # Update the value of id
            E.stack[i].update({self.id: value})
          i -= 1

        if not found:
          # id must in global variables
          # Get the value of the sharedId
          E.static.update({self.id: value})
    
    else: # id is int type
      # Get value of expr
      value = self.expr.execute(E, S2, sc)
      # Two options: id is in stack or static
      found = False
      i = len(E.stack) - 1

      # Check stack first to ensure the variable hiding mechanism
      while i >= 0 and not found:          
        if self.id in E.stack[i].keys():
          # Found in local stack
          found = True
          # Update the value of the id key
          E.stack[i].update({self.id: value})
        i -= 1

      if not found:
        # id must in global variables
        E.static.update({self.id: value})
         

# Out class has two methods, parse() method to parse the out 
# and print() method to print the out 
class Out:
  # Parse method
  def parse(self, S, sc):
    # Current token is not OUTPUT, stop execute.
    if S.currentToken() != Core.OUTPUT:
      print("ERROR: Expect keyword OUTPUT instead " + S.currentToken().name)
      sys.exit()
    # Consume the OUTPUT token
    S.nextToken()

    # Current token is not LPAREN, stop execute.
    if S.currentToken() != Core.LPAREN:
      print("ERROR: Expect keyword LPAREN instead " + S.currentToken().name)
      sys.exit()
    # Consume the LPAREN token
    S.nextToken()

    # Parse the expr
    self.expr = Expr()
    self.expr.parse(S, sc)

    # Current token is not RPAREN, stop execute.
    if S.currentToken() != Core.RPAREN:
      print("ERROR: Expect keyword RPAREN instead " + S.currentToken().name)
      sys.exit()
    # Consume the RPAREN token
    S.nextToken()

    # Current token is not SEMICOLON, stop execute.
    if S.currentToken() != Core.SEMICOLON:
      print("ERROR: Expect keyword SEMICOLON instead " + S.currentToken().name)
      sys.exit()
    # Consume the SEMICOLON token
    S.nextToken()

  # Print method print out the statement in somewhat neat format.
  def print(self):
    print("    output(", end = ' ')
    self.expr.print()
    print(");")
  
  # Executor method print out the expression.
  def execute(self, E, S2, sc):
    value = self.expr.execute(E, S2, sc)
    print(value)


# If class has two methods, parse() method to parse the If statements
# and print() method to print the If statements
class If:
  # Parse method
  def parse(self, S, sc):
    # Current token is not IF, stop execute.
    if S.currentToken() != Core.IF:
      print("ERROR: Expect keyword IF instead " + S.currentToken().name)
      sys.exit()
    # Consume the IF token
    S.nextToken()

    # Parse the condition
    self.cond = Cond()
    self.cond.parse(S, sc)

    # Current token is not THEN, stop execute.
    if S.currentToken() != Core.THEN:
      print("ERROR: Expect keyword THEN instead " + S.currentToken().name)
      sys.exit()
    # Consume the THEN token
    S.nextToken()

    # Current token is not LBRACE, stop execute.
    if S.currentToken() != Core.LBRACE:
      print("ERROR: Expect keyword LBRACE instead " + S.currentToken().name)
      sys.exit()
    # Consume the LBRACE token
    S.nextToken()
    # Add a new scope of variables
    sc.addList()

    # Parse the stmt-seq
    self.ss = StmtSeq()
    self.ss.parse(S, sc)

    # Current token is not RBRACE, stop execute.
    if S.currentToken() != Core.RBRACE:
      print("ERROR: Expect keyword RBRACE instead " + S.currentToken().name)
      sys.exit()
    # Consume the RBRACE token
    S.nextToken()
    # Discard a scope of id
    sc.remList()

    self.haveElse = False
    self.elseSS = StmtSeq()
    # Check if there is else statement
    if S.currentToken() == Core.ELSE:
      self.haveElse = True
      # Consume the ELSE token
      S.nextToken()

      # Current token is not LBRACE, stop execute.
      if S.currentToken() != Core.LBRACE:
        print("ERROR: Expect keyword LBRACE instead " + S.currentToken().name)
        sys.exit()
      # Consume the LBRACE token
      S.nextToken()
      # Add a new scope of variables
      sc.addList()

      # Parse the stmt-seq in the else statement
      self.elseSS.parse(S, sc)

      # Current token is not RBRACE, stop execute.
      if S.currentToken() != Core.RBRACE:
        print("ERROR: Expect keyword RBRACE instead " + S.currentToken().name)
        sys.exit()
      # Consume the RBRACE token
      S.nextToken()
      # Discard a scope of id
      sc.remList()

  # Print method print out the if statements in somewhat neat format.
  def print(self):
    print("    if ", end = ' ')
    self.cond.print()
    print(" then {")
    print("  ", end = ' ')
    self.ss.print()
    if self.haveElse:
      print("    } else {")
      print("  ", end = ' ')
      self.elseSS.print()
      print("    }")
    else:
      print("    }")

  # Execute method execute the if statements.
  def execute(self, E, S2, sc):

    # The if statement have else block
    if self.haveElse:
      if self.cond.execute(E, S2, sc):
        # Create new layer of scope on stack
        E.stack.append({})
        E.refList.append([])
        # Execute the statement seq in if block
        self.ss.execute(E, S2, sc)
        # remove the if block scope on stack
        E.refList.pop()
        E.stack.pop()
      else:
        # Create new layer of scope on stack
        E.refList.append([])
        E.stack.append({})
        # Execute the statement seq in else block
        self.elseSS.execute(E, S2, sc)
        # remove the else block scope on stack
        E.refList.pop()
        E.stack.pop()

    else: # The if statement do not have else block
      if self.cond.execute(E, S2, sc):
        # Create new layer of scope on stack
        E.refList.append([])
        E.stack.append({})
        # Execute the statement seq in if block
        self.ss.execute(E, S2, sc)
        # remove the if block scope on stack
        E.refList.pop()
        E.stack.pop()


# Loop class has two methods, parse() method to parse the loop statements
# and print() method to print the loop statements
class Loop:
  # Parse method
  def parse(self, S, sc):
    # Current token is not WHILE, stop execute.
    if S.currentToken() != Core.WHILE:
      print("ERROR: Expect keyword WHILE instead " + S.currentToken().name)
      sys.exit()
    # Consume the WHILE token
    S.nextToken()

    # Parse the condition
    self.cond = Cond()
    self.cond.parse(S, sc)

    # Current token is not LBRACE, stop execute.
    if S.currentToken() != Core.LBRACE:
      print("ERROR: Expect keyword LBRACE instead " + S.currentToken().name)
      sys.exit()
    # Consume the LBRACE token
    S.nextToken()
    # Add a new scope of variables
    sc.addList()

    # Parse the stmt-seq
    self.ss = StmtSeq()
    self.ss.parse(S, sc)

    # Current token is not RBRACE, stop execute.
    if S.currentToken() != Core.RBRACE:
      print("ERROR: Expect keyword RBRACE instead " + S.currentToken().name)
      sys.exit()
    # Consume the RBRACE token
    S.nextToken()
    # Discard a scope of id
    sc.remList()
      
  # Print method print out the while statements in somewhat neat format.
  def print(self):
    print("    while", end = ' ')
    self.cond.print()
    print(" {")
    print("  ", end = ' ')
    self.ss.print()
    print("    }")
  
  # Execute method execute the while statements.
  def execute(self, E, S2, sc):
    # Create new layer of scope on stack
    E.stack.append({})
    E.refList.append([])

    while self.cond.execute(E, S2, sc):
      # Execute the statement seq in while block
      self.ss.execute(E, S2, sc)

    # remove the while block scope on stack
    E.refList.pop()
    E.stack.pop()


# Cond class has two methods, parse() method to parse the condition 
# and print() method to print the condition
class Cond:
  # Parse method
  def parse(self, S, sc):
    self.isNegation = False
    self.hasOr = False
    self.cond = Cond()
    self.cmpr = Cmpr()
    self.orCond = Cond()
    # First check if it is the negation
    if S.currentToken() == Core.NEGATION:
      self.isNegation = True
      # Consume the NEGATION token
      S.nextToken()

      # Current token is not LPAREN, stop execute.
      if S.currentToken() != Core.LPAREN:
        print("ERROR: Expect keyword LPAREN instead " + S.currentToken().name)
        sys.exit()
      # Consume the LPAREN token
      S.nextToken()

      # Parse the condition
      self.cond.parse(S, sc)

      # Current token is not RPAREN, stop execute.
      if S.currentToken() != Core.RPAREN:
        print("ERROR: Expect keyword RPAREN instead " + S.currentToken().name)
        sys.exit()
      # Consume the RPAREN token
      S.nextToken()
    else:
      # Parse the cmpr
      self.cmpr.parse(S, sc)

      # Check if there is or
      if S.currentToken() == Core.OR:
        self.hasOr = True
        # Consume the OR token
        S.nextToken()

        # Parse the condition
        self.orCond.parse(S, sc)
    
  # Print method print out the condition statements in somewhat neat format.
  def print(self):
    if self.isNegation:
      print("!(", end = ' ')
      self.cond.print()
      print(")", end = ' ')
    elif self.hasOr:
      self.cmpr.print()
      print(" or ", end = ' ')
      self.orCond.print()
    else:
      self.cmpr.print()

  # Execute method evaluate the condition and return a boolean value.
  def execute(self, E, S2, sc):
    result = False
    # Three options: negation, or , or comparision
    if self.isNegation: # Negation
      result = not self.cond.execute(E, S2, sc)
    elif self.hasOr: # Or
      result = self.cmpr.execute(E, S2, sc) or self.cond.execute(E, S2, sc)
    else: # Comparision
      result = self.cmpr.execute(E, S2, sc)
    return result


# Cmpr class has two methods, parse() method to parse the comparison 
# and print() method to print the comparison
class Cmpr:
  # Parse method
  def parse(self, S, sc):
    self.isEqual = False
    self.isLess = False
    self.isLessEqual = False

    # Parse the expr
    self.preExpr = Expr()
    self.preExpr.parse(S, sc)

    # Check for the type of comparison
    if S.currentToken() == Core.EQUAL:
      self.isEqual = True
      # Consume the EQUAL token
      S.nextToken()
    elif S.currentToken() == Core.LESS:
      self.isLess = True
      # Consume the LESS token
      S.nextToken()
    elif S.currentToken() == Core.LESSEQUAL:
      self.isLessEqual = True
      # Consume the LESSEQUAL token
      S.nextToken()

    # Parse the expr
    self.postExpr = Expr()
    self.postExpr.parse(S, sc) 

  # Print method print out the comparison in somewhat neat format.
  def print(self):
    self.preExpr.print()
    if self.isEqual:
      print(" == ", end = ' ')
    elif self.isLess:
      print(" < ", end = ' ')
    elif self.isLessEqual:
      print(" <= ", end = ' ')
    self.postExpr.print()

  # Execute method evaluate the comparison and return a boolean value.
  def execute(self, E, S2, sc):
    result = False
    # Three options: equal, less than , or equal or less than
    if self.isEqual: # equal
      result = self.preExpr.execute(E, S2, sc) == self.postExpr.execute(E, S2, sc)
    elif self.isLess: # less than
      result = self.preExpr.execute(E, S2, sc) < self.postExpr.execute(E, S2, sc)
    else: # equal or less than
      result = self.preExpr.execute(E, S2, sc) <= self.postExpr.execute(E, S2, sc)
    return result


# Expr class has two methods, parse() method to parse the expression 
# and print() method to print the expression
class Expr:
  # Parse method
  def parse(self, S, sc):
    self.isAdd = False
    self.isSub = False

    # Parse the term
    self.term = Term()
    self.term.parse(S, sc)

    self.expr = Expr()
    # Check the type of expression operator
    if S.currentToken() == Core.ADD:
      self.isAdd = True
      # Consume the Add token
      S.nextToken()
      # Parse the expression
      self.expr.parse(S, sc)
    elif S.currentToken() == Core.SUB:
      self.isSub = True
      # Consume the SUB token
      S.nextToken()
      # Parse the expression
      self.expr.parse(S, sc)
    
  # Print method print out the expression in somewhat neat format.
  def print(self):
    self.term.print()
    if self.isAdd:
      print(" + ", end = ' ')
      self.expr.print()
    elif self.isSub:
      print(" - ", end = ' ')
      self.expr.print()
  
  # execute method calculate the expression and return an int value.
  def execute(self, E, S2, sc):
    # Evaluate the term value
    result = self.term.execute(E, S2, sc)
    # Two options: Add or subtract
    if self.isAdd: # add
      result += self.expr.execute(E, S2, sc)
    elif self.isSub: # subtract
      result -= self.expr.execute(E, S2, sc)

    return result


# Term class has two methods, parse() method to parse the term 
# and print() method to print the term
class Term:
  # Parse method
  def parse(self, S, sc):
    self.isMult = False

    # Parse the factor
    self.factor = Factor()
    self.factor.parse(S, sc)

    self.term = Term()
    # Check if there is multiplication
    if S.currentToken() == Core.MULT:
      self.isMult = True
      # Consume the MULT token
      S.nextToken()
      # Parse the term
      self.term.parse(S, sc)
  
  # Print method print out the expression in somewhat neat format.
  def print(self):
    self.factor.print()
    if self.isMult:
      print(" * ", end = ' ')
      self.term.print()
  
  # execute method calculate the term and return an int value.
  def execute(self, E, S2, sc):
    # Evaluate the factor value
    result = self.factor.execute(E, S2, sc)
    if self.isMult: # multiply
      result *= self.term.execute(E, S2, sc)

    return result


# Factor class has two methods, parse() method to parse the factor 
# and print() method to print the factor
class Factor:
  # Parse method
  def parse(self, S, sc):
    self.isId = False
    self.isConst = False
    self.isExpr = False
    self.isInput = False

    self.id = None
    self.const = None
    self.expr = Expr()
    #Check the type of the factor
    if S.currentToken() == Core.ID:
      self.isId = True
      self.id = S.getID()
      # Perform semantic check 
      if not sc.existCheck(self.id, False) and not sc.existCheck(self.id, True):
        print("ERROR: " + self.id + " must be declared before assign to another value")
        sys.exit()
      # Consume the ID token
      S.nextToken()
    elif S.currentToken() == Core.CONST:
      self.isConst = True
      self.const = S.getCONST()
      # Consume the ID token
      S.nextToken()
    elif S.currentToken() == Core.LPAREN:
      self.isExpr = True
      # Consume the LPAREN token
      S.nextToken()
      # Parse the expression
      self.expr.parse(S, sc)
      # Current token is not RPAREN, stop execute.
      if S.currentToken() != Core.RPAREN:
        print("ERROR: Expect keyword RPAREN instead" + S.currentToken().name)
        sys.exit()
      # Consume the RPAREN token
      S.nextToken()
    elif S.currentToken() == Core.INPUT:
      self.isInput = True
      # Consume the INPUT token
      S.nextToken()
      # Current token is not LPAREN, stop execute.
      if S.currentToken() != Core.LPAREN:
        print("ERROR: Expect keyword LPAREN instead" + S.currentToken().name)
        sys.exit()
      # Consume the LPAREN token
      S.nextToken()
      # Current token is not RPAREN, stop execute.
      if S.currentToken() != Core.RPAREN:
        print("ERROR: Expect keyword RPAREN instead" + S.currentToken().name)
        sys.exit()
      # Consume the RPAREN token
      S.nextToken()
    else:
      print("ERROR: Expect a factor but incorrect position for keyword " + S.currentToken().name)
      sys.exit()
  
  # Print method print out the factor in somewhat neat format.
  def print(self):
    if self.isId:
      print(self.id, end = ' ')
    elif self.isConst:
      print(self.const, end = ' ')
    elif self.isExpr:
      print("(", end = ' ')
      self.expr.print()
      print(")", end = ' ')
    elif self.isInput:
      print("input()")
  
  # execute method calculate the factor and return an int value.
  def execute(self, E, S2, sc):
    result = 0
    # 4 options: id, const, expr, or input

    if self.isId: # id
      # 2 options: int or ref

      if E.refExist(self.id): # id is reference type
        # Two options: id is in stack or static
        found = False
        i = len(E.stack) - 1
        # Check stack first to ensure the variable hiding mechanism
        while i >= 0 and not found:          
          if self.id in E.stack[i].keys():
            # Found in local stack
            found = True
            # Get the value on the heap
            result = E.heap[E.stack[i].get(self.id)] 
          i -= 1

        if not found:
          # id must in global variables
          result = E.heap[E.static.get(self.id)]
      
      else: # id is int type
        # Two options: id is in stack or static
        found = False
        i = len(E.stack) - 1
        # Check stack first to ensure the variable hiding mechanism
        while i >= 0 and not found:          
          if self.id in E.stack[i].keys():
            # Found in local stack
            found = True
            # Get the value on the heap
            result = E.stack[i].get(self.id) 
          i -= 1

        if not found:
          # id must in global variables
          result = E.static.get(self.id)
    
    elif self.isConst: # Const
      result = self.const
    elif self.isExpr: # Expr
      result = self.expr.execute(E, S2, sc)
    elif self.isInput: # Input
      #Error check for .data file run out of values to use
      try:
        inputInt = S2.getCONST()
      except: 
        print("ERROR: All values in the .data file have already been used")
        sys.exit()
      result = inputInt
    
    return result


# SemanticCheck class used to keep track of the variable scope and their declaration type
class SemanticCheck:
  intLists = []
  refLists = []
  # Addlist method to add a new empty list of variable at the end of the list check to 
  # represent a new scope of the variable
  def addList(self):
    self.intLists.append([])
    self.refLists.append([])
  
  # Remlist method to remove the last element of the variable list to represent this scope
  # of vaiables are out of scope now
  def remList(self):
    self.intLists.pop()
    self.refLists.pop()

  # AddToCurrentInt method to add new int variable list in the last list of the lists
  def addToCurrentInt(self, intList):
    self.intLists[len(self.intLists) - 1].extend(intList)

  # AddToCurrentRef method to add new Ref variable list in the last list of the lists
  def addToCurrentRef(self, refList):
    self.refLists[len(self.refLists) - 1].extend(refList)
  
  # ExistCheck method check if the variable exist in the current scope or
  # outer scope
  def existCheck(self, id, isInt):
    if isInt:
      for l in self.intLists:
        for e in l:
          if e == id:
            return True
    else:
      for l in self.refLists:
        for e in l:
          if e == id:
            return True
    return False

  # RepeatCheck method check if the variable has been declared in its current scope
  def repeatCheck(self, id, isInt):
    if isInt:
      for e in self.intLists[len(self.intLists) - 1]:
        if e == id:
          return True
    else:
      for e in self.refLists[len(self.refLists) - 1]:
        if e == id:
          return True
    return False

if __name__ == "__main__":
    main()
