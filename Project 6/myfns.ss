;; An interpreter for a simple functional language "PLAN". 
; Written in Scheme Language
; Author: Zheyuan Gao

; Define myinterpreter function to take the program as input
(define (myinterpreter Program)
    (evalExpr (cadr Program) '())
) 

; Define evalExpr function to evaluate the expression
(define (evalExpr Expr Bindings)
    (cond
        ; Expr is an intger, return the integer
        ((integer? Expr) Expr)

        ; Expr is an Id, get its corresponding value
        ((symbol? Expr) (getValue Expr Bindings))

        ; Expr is a planIf, call the evaluate If function
        ((equal? (car Expr) 'planIf) 
            (evalPlanIf Expr Bindings)
        )

        ; Expr is a planAdd, call the evaluate Add function
        ((equal? (car Expr) 'planAdd) 
            (evalPlanAdd Expr Bindings)
        )

        ; Expr is a planMul, call the evaluate Mul function
        ((equal? (car Expr) 'planMul) 
            (evalPlanMul Expr Bindings)
        )

        ; Expr is a planSub, call the evaluate Sub function
        ((equal? (car Expr) 'planSub) 
            (evalPlanSub Expr Bindings)
        )

        ; Expr is a planLet, call the evaluate Let function
        ((equal? (car Expr) 'planLet) 
            (evalPlanLet (cadr Expr) (caddr Expr) (cadddr Expr) Bindings)
        )

        ; Expr is a function invocation, call the function execution
        (#t
            (evalFuncCall (car Expr) (cadr Expr) Bindings)
        )

    )
)

; Define the evalPlanIf function to evaluate the planIf case
(define (evalPlanIf Expr Bindings)
    ; Compare the first expression with 0
    (if (> (evalExpr (cadr Expr) Bindings) 0)
        ; Evalue the second expression if first expression > 0
        (evalExpr (caddr Expr) Bindings)
        ; Evalue the second expression if first expression not > 0
        (evalExpr (cadddr Expr) Bindings)
    )
)

; Define the evalPlanAdd function to evaluate the planAdd case
(define (evalPlanAdd Expr Bindings)
    ; Add the first expression and the second expression
    (+ (evalExpr (cadr Expr) Bindings) (evalExpr (caddr Expr) Bindings))
)

; Define the evalPlanMul function to evaluate the planMul case
(define (evalPlanMul Expr Bindings)
    ; Multiply the first expression and the second expression
    (* (evalExpr (cadr Expr) Bindings) (evalExpr (caddr Expr) Bindings))
)

; Define the evalPlanSub function to evaluate the planSub case
(define (evalPlanSub Expr Bindings)
    ; Substract the second expression from the first expression
    (- (evalExpr (cadr Expr) Bindings) (evalExpr (caddr Expr) Bindings))
)

; Define the getValue function to get the value binds to the Id
(define (getValue Expr Bindings)
    (cond
        ; Base case, bindings is empty, return null
        ((null? Bindings) #f)
        ; Check if the first element in the binding list is the Id pair we need
        ((equal? Expr (caar Bindings)) (cdar Bindings))
        ; Recurive call to search the rest of the list
        (#t (getValue Expr (cdr Bindings)))
    )
)

; Define the evalPlanLet function to evaluate the planLet case
(define (evalPlanLet id Expr1 Expr2 Bindings)  
    (cond
        ; The first expression is a symbol or integer, get its value
        ((symbol? Expr1)
            (evalExpr Expr2 
            (addToBindings Bindings id (evalExpr Expr1 Bindings)))
        )
        ((integer? Expr1)
            (evalExpr Expr2 
            (addToBindings Bindings id (evalExpr Expr1 Bindings)))
        )
        ; The first expression is not symbol or const, can not evaluate directly
        ; Add the binding of func name and func body to the binding list
        ((list? Expr1)
            (evalExpr Expr2 
            (addToBindings Bindings id Expr1))
        )
    )
)

; Define the addToBindings funtion to add (id.value) pairs to the binding list
(define (addToBindings Bindings id value)
    (cond
        ; Already have the value and add the binding directly
        ((integer? value)
            (cons (cons id value) Bindings)
        )
        ; Binding not finished yet
        ((not (equal? (car value) 'planFunction))
            (cons (cons id (evalExpr value Bindings)) Bindings)
        )
        ; The case is a function defination
        (#t
            (cons (cons id value) Bindings)
        )
    )
)

; Define the evalFuncCall funtion to execute the funtion call 
(define (evalFuncCall funcName FuncArgue Bindings)
    (evalExpr 
        ; Get the function Body
        (caddr (getValue funcName Bindings))
        ; Add the function parameters into the binding
        (addToBindings Bindings 
            ;Get the function formal parameter
            (cadr (getValue funcName Bindings))
            ;Get the function arguement
            FuncArgue
        )
    )
)

