# hatstack proof of concept


class Interpreter():
    
    # methods with names starting with i are reserved for the interpreter's use
        
    def iload(self):
        self.stack.append( self.inp.pop() )
        
    def isave(self):
        self.out.append( self.stack.pop() )
        
    def iadd(self):
        val = self.stack.pop() + self.stack.pop()
        self.stack.append(val)
        
    def __init__(self):
        self.program = ""
        self.tokens = []
        self.inp = []
        self.out = []
        self.validate = []
        self.stack = []
        self.instructions = {
                "load": self.iload,
                "add": self.iadd,
                "save": self.isave
                }
    
    
    def load_program(self, program):
        self.program = program
        self.tokens = self.program.lower().split()
        
    def load_problem(self, problem = None):
        self.inp = [3, 9, 10, 5]
        self.validate = [15, 12]
        
    def run(self):
        ip = 0 # instruction pointer
        #token = self.tokens[ip]
        #self.instructions[token]()
        #return
        while ip < len(self.tokens):
            token = self.tokens[ip]
            self.instructions[token]()
            ip+=1
            
    def is_valid(self):
        limit = 100
        for i in range(limit):
            self.run()
            if len(self.inp) == 0:
                break
        if i == limit-1:
            print("Iteration limit reached.")
            return
        if str(self.validate) == str(self.out):
            print("Program successfully validated!")
        else:
            print("Output was incorrect. Your output:", self.out)
            
interp = Interpreter()
interp.load_problem()
interp.load_program("load\
                    load\
                    add\
                    save")
interp.is_valid()
print(interp.out)