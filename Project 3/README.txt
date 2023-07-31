Name: Zheyuan Gao

Files submitted:
Core.py: Enum file contains all the key words of the program.
Scanner.py: The language scanner to read tokens, identifiers, and constants.
Main.py: Program parser and executor to parse the input code and execute the whole program, print any outputs of the program. Also responsiable for null reference error checking and input file error checking. 
README.txt: This text file

Special Features: N/A

Description of the interpreter: 
Every non-terminal classes will have a execute method and it will call other classes' execute method based on the structure of the grammar. Whenever an id is used, the type will be checked. And the program will start from the top of the stack (ensure variable hiding) and all the way down to the base of the stack and then the static. Once found, based on the type, the int variable will represent the value the key paris to. The ref variable's pair value will be the index on the heap, and the program will get the actual value from the heap. 
Variable tracking are done by 4 date structures:
Static: 
A dictionary {var: value} to store the global variables.
Stack: 
A stack(actually a list in python but simulating the behavior of stack) of dictionaries to store the local variables. For every LBRACE in the token stream, a new dictionary (scope) been pushed on the stack and for everu RBRACE, a dictionary (scope) is poped from the stack. The dictionary on stack are of the form {var: value} and 
Heap:
A list of int to store the reference value of the reference variables.
RefList: 
A list of list of int to keep track of the ref variables in different scope. Same to stack, a list is pushed on the RefList for every LBRACE and popped off from the RefList for every RBRACE. The "refExist" method will check if the given variable as parameter exists in current or outer scopes. This will keep track of the variables' type during execution.  

How I tested the interpreter and known bugs:
I used the test script and cases provided to test the interpretor. I also created several of my own test cases to make sure the interpretor works fine. 
There are no known bugs. 

