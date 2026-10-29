from stacks_and_queues import DSAStack, DSACircularQueue

class EquationSolver:
    def solve(self, equation):
        postfix_queue = self._parseInfixtoPostfix(equation)
        result = self._evaluatePostfix(postfix_queue)
        return result 
    
    def _parseInfixtoPostfix(self, equation):
        postfix_queue = DSACircularQueue() # Stores the postfix expression
        operator_stack = DSAStack() # Temporarily stores operators
        tokens = equation.split(" ") # Split the equation string into tokens (numbers, operators, brackets)

        for token in tokens:
            try: # Check if the token is a number (operand)
                num_val = float(token)
                postfix_queue.enqueue(num_val) # Add numbers directly to the queue
            except ValueError: # If not a number, it's an operator or bracket
                if token == '(':
                    operator_stack.push(token) # Push '(' onto the stack
                elif token == ')':
                  #  Pop from the stack to the queue until the matching '(' is found
                 while not operator_stack.is_empty() and operator_stack.top() != '(':
                     postfix_queue.enqueue(operator_stack.pop())
                 if operator_stack.is_empty():
                        raise ValueError("Mismatched parentheses: No matching '('.")
                 operator_stack.pop() # Discard the '('
                else: # Token is an operator
                      # While stack has operators of higher or equal precedence, pop them to the queue
                     while (not operator_stack.is_empty() and
                           operator_stack.top() != '(' and
                           self._precedenceOf(operator_stack.top()) >= self._precedenceOf(token)):
                       postfix_queue.enqueue(operator_stack.pop())
                     operator_stack.push(token) # Push the current operator onto the stack

        # After all tokens are read, pop any remaining operators from the stack to the queue
        while not operator_stack.is_empty():
            if operator_stack.top() == '(':
                raise ValueError("Mismatched parentheses: Extra '(' found.")
            postfix_queue.enqueue(operator_stack.pop())
            
        return postfix_queue
    
    def _evaluatePostfix(self, postfixQueue):
        """Takes a postfix queue and evaluates it to a single float result"""
        
        operand_stack = DSAStack() # Use a stack to hold operands for evaluation
        
        while not postfixQueue.is_empty():
            term = postfixQueue.dequeue() # Get the next item (which is either a number or an operator) from the queue
            
            # Check if the term is a number (operand) or an operator
            if isinstance(term, float):
                operand_stack.push(term) # If it's a number, push it onto the stack
            else: # If it's an operator
                # Pop the top two operands from the stack
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                
                # Execute the operation and push the result back onto the stack
                result = self._executeOperation(term, op1, op2)
                operand_stack.push(result)
        
        # The final result is the only item left on the stack
        return operand_stack.pop()

    def _precedenceOf(self, theOp):
        """Returns the precedence level of a given operator"""

        if theOp == '+' or theOp == '-':
            return 1 
        elif theOp == '*' or theOp == '/':
            return 2 
        else:
            return 0 

    def _executeOperation(self, op, op1, op2):
        """Executes a single mathematical operation.Note the order: op1 is the first operand popped, op2 is the second"""

        if op == '+':
            return op1 + op2
        elif op == '-':
            return op1 - op2 
        elif op == '*':
            return op1 * op2 
        elif op == '/':
            # Add a check for division by zero for robust code
            if op2 == 0:
                raise ValueError("Division by zero.")
            return op1 / op2 
        else:
            raise ValueError(f"Unknown operator: {op}")


def test_EquationSolver():
    solver = EquationSolver()

    equation_1 = "2 + 9 * ( 1 - 5 )"
    result_1 = solver.solve(equation_1)
    print(f"Result of '{equation_1}' is {result_1}")

    equation_2 = "5 + 4 * 9"
    result_2 = solver.solve(equation_2)
    print(f"Result of '{equation_2}' is {result_2}")

    equation_3 = "100 * 4 + 24"
    result_3 = solver.solve(equation_3)
    print(f"Result of '{equation_3}' is {result_3}")

    equation_4 = "200 * ( 1 + 33 )"
    result_4 = solver.solve(equation_4)
    print(f"Result of '{equation_4}' is {result_4}")

    equation_5 = "150 * ( 2 + 20 ) / 18"
    result_5 = solver.solve(equation_5)
    print(f"Result of '{equation_5}' is {result_5}")

test_EquationSolver()

    






