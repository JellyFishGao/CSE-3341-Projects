Name: Zheyuan Gao

Files submitted:
Core.py: Enum file contains all the key words of the program.
Main.py: Program parser to parse the input code and output the whole program. Also responsible for syntax error and semantic error checking.
 Scanner.py: The language scanner to read tokens, identifiers, and constants.
README.txt: This text file

Special Features: N/A

Description of the parser: 
The program parsing is depend purely on the grammar provided. I created a class for every non-terminals in the grammar. And all the classes have two methods, parse and print. The parse method check the tokens one by one and recognized if the expected tokens are in the right place by the grammar. Also, it will created new classes based on the grammar and call their parse method. The print will print the terminals with indentation. Once it finds a non-terminal, it will call the print method of that non-terminal. These process follows the recursive decent parsing. But there is not a actually tree data structure exist in the code, the process of non-terminals calling other non-terminals' parse methods establish a parsing tree structure. 
The semantic check is done by the semantic check class, which is a stack data structure represented by two lists of lists. One keep track of the int id and another keep track of the ref id. Whenever the current token is a LBRACE, a new list is created at the right end of both the two lists of lists. All the new id declared in the scope will be stored in the new lists based on their data type. Whemever the current token is RBRACE, the right end lists will be poped from both the two lists of lists. The semantic check is done by checking the ids storen in the semantic check class.

How I tested the parser and known bugs:
I used the test script and cases provided to test the parser. I also created several of my own test cases to make sure the parser works fine. 
There are no known bugs. 

