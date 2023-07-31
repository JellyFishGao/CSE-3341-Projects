Name: Zheyuan Gao

Files submitted:
Core.py: Enum file contains all the key words of the program.
Scanner.py: The language scanner to read tokens, identifiers, and constants.
Main.py: Program parser and executor to parse the input code and execute the whole program, print any outputs of the program. Also responsible for executing function declarations and function calls. 
README.txt: This text file

Special Features: N/A

Description of the interpreter: 
Every non-terminal classes will have a parse, print, and execute method and it will call other classes' methods based on the structure of the grammar.
Call stack implementation: 
Now, the program's stack is a stack of frames (stack of maps like in Project3). The main() function frame will be at the bottom of the stack and every time the a function is invoked in the main, a new frame for the function is added on the stack. The invocation of the functions are relying on these 2 data structures:
funcBodyMap: A dictionary to store the function name and its corresponding statement sequence when the func-decl is executing. Once the main() invoke a particular function, the body of the function will be retrived from the dictionary and start to execute.
funcFormalMap: A dictionary to store the function name and its corresponding formal parameters when the func-decl is executing. Once the main() invoke a particular function, the formal parmeters of the function will be retrived from the dictionary and been passed with the corresponding arguments values.

How I tested the interpreter and known bugs:
I used the test script and cases provided to test the interpretor. I also created several of my own test cases to make sure the interpretor works fine. Also, I used the correct test cases from Project 3 to test my interpreter. 
There are no known bugs. 


