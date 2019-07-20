# hatstack proof of concept
import sys

class Interpreter():
    
    # methods with names starting with i are reserved for the interpreter's use
        
    def i_in(self):
        self.stack.append( self.pop(self.inp) )
        self.ip+=1
        
    def i_out(self):
        self.out.append( self.stack.pop() )
        self.ip+=1
        
    def i_add(self):
        val = self.pop(self.stack) + self.pop(self.stack)
        self.last_val 
        self.stack.append(val)
        self.ip+=1

    def i_sub(self):
        val = self.pop(self.stack) - self.pop(self.stack)
        self.last_val 
        self.stack.append(val)
        self.ip+=1

    def i_mul(self):
        val = self.pop(self.stack) * self.pop(self.stack)
        self.last_val 
        self.stack.append(val)
        self.ip+=1

    def i_div(self):
        val = self.pop(self.stack) // self.pop(self.stack)
        self.last_val 
        self.stack.append(val)
        self.ip+=1

    def i_mod(self):
        val = self.pop(self.stack) % self.pop(self.stack)
        self.last_val 
        self.stack.append(val)
        self.ip+=1

    def i_jump(self):
        self.ip+=1
        label = self.tokens[self.ip]
        self.ip = self.labels[label]

    def i_jez(self):
        self.ip+=1
        if self.last_val != 0:
            return
        label = self.tokens[self.ip]
        self.ip = self.labels[label]

    def i_jlz(self):
        self.ip+=1
        if not self.last_val < 0:
            return
        label = self.tokens[self.ip]
        self.ip = self.labels[label]

    def i_jgz(self):
        self.ip+=1
        if not self.last_val > 0:
            return
        label = self.tokens[self.ip]
        self.ip = self.labels[label]

    def i_load(self):
        self.ip+=1
        alias = self.tokens[self.ip]
        if alias not in self.mem:
            self.mem[alias]
        self.stack.append(self.mem[alias])

    def i_save(self):
        self.ip+=1
        alias = self.tokens[self.ip]
        self.ip+=1
        self.mem[alias] = self.pop(self.stack)

    def __init__(self):
        self.program = ""
        self.tokens = []
        self.inp = []
        self.out = []
        self.validate = []
        self.stack = []
        self.labels = {}
        self.mem = {}
        self.last_val = None
        self.ip = 0
        self.exit = False
        self.instructions = {
                "in": self.i_in,
                "add": self.i_add,
                "sub": self.i_sub,
                "mul": self.i_mul,
                "div": self.i_div,
                "mod": self.i_mod,
                "out": self.i_out,
                "jump": self.i_jump,
                "jez": self.i_jez,
                "jlz": self.i_jlz,
                "jgz": self.i_jgz,
                }
    
    def pop(self, source):
        if len(source) > 0:
            return source.pop()
        self.exit = True
        return 0

    def load_program(self, program):
        if program.find(".hat") != -1:
            f = open(program)
            program = f.read()
            f.close()
        self.program = program
        self.tokens = self.program.lower().split()
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            if token[0] == "#":
                self.labels[token[1:]] = i
                self.tokens.pop(i)
            i+=1
        
    def load_problem(self, problem = None):
        self.inp = [3, 9, 10, 5]
        self.validate = [15, 12]
        
    def run(self):
        self.ip = 0
        while self.ip < len(self.tokens):
            if self.exit:
                break
            token = self.tokens[self.ip]
            self.instructions[token]()
            
    def is_valid(self, simulate = True):
        limit = 3
        if simulate:
            for i in range(limit):
                self.run()
                if len(self.inp) == 0 or self.exit:
                    break
            if i == limit-1:
                print("Iteration limit reached.", self.inp)
                return
        if str(self.validate) == str(self.out):
            print("Program successfully validated!", self.out)
        else:
            print("Output was incorrect. Your output:", self.out)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Pass a valid program name.")
    else:
        interp = Interpreter()
        interp.load_problem()
        interp.load_program(sys.argv[1])
        interp.is_valid()