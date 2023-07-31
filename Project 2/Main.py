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

  # Print out the program from the parse tree
  prog.print()

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


# StmtSeq class has two methods, parse() method to parse the statement sequence
# and print() method to print the statement sequence
class StmtSeq:
  # Parse method
  def parse(self, S, sc):
    # Create the declaration object
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
    # Check if there are more declaration to be printed
    if self.moreStmtSeq:
      self.newStmtSeq.print()


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


# Stmt class has two methods, parse() method to parse the statement 
# and print() method to print the statement 
class Stmt:
  # Parse method
  def parse(self, S, sc):
    self.stmt = None
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
      self.stmt = Decl()
      self.stmt.parse(S, sc)
    # Invalid use of statement
    else:
      print("ERROR: Expect keyword of a statement instead " + S.currentToken().name)
      sys.exit()
  
  # Print method print out the statement in somewhat neat format.
  def print(self):
    self.stmt.print()


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
      print("ERROR: Incorrect position for key word " + S.currentToken().name)
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
