# hatstack proof of concept
import sys

class Token():
    def __init__(self):
        self.line = 0
        self.position = 0
        self.file = ""
        self.type = ""
        # types include instruction, alias, label, literal

class Function():
    # sort of a mini interpreter
    def __init__(self):
        self.ip = 0
        self.labels = {}
        self.mem = {}
        self.tokens = []

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
        self.last_val = val
        self.stack.append(val)
        self.ip+=1

    def i_sub(self):
        val = self.pop(self.stack) - self.pop(self.stack)
        self.last_val = val
        self.stack.append(val)
        self.ip+=1

    def i_mul(self):
        val = self.pop(self.stack) * self.pop(self.stack)
        self.last_val = val
        self.stack.append(val)
        self.ip+=1

    def i_div(self):
        val = self.pop(self.stack) // self.pop(self.stack)
        self.last_val = val
        self.stack.append(val)
        self.ip+=1

    def i_mod(self):
        val = self.pop(self.stack) % self.pop(self.stack)
        self.last_val = val
        self.stack.append(val)
        self.ip+=1

    def i_jump(self):
        self.ip+=1
        label = self.tokens[self.ip]
        self.ip = self.labels[label]

    def i_jez(self):
        self.ip+=1
        if self.pop(self.stack) != 0:
            self.ip+=1
            return
        label = self.tokens[self.ip]
        self.ip = self.labels[label]

    def i_jlz(self):
        self.ip+=1
        if not self.pop(self.stack) < 0:
            self.ip+=1
            return
        label = self.tokens[self.ip]
        self.ip = self.labels[label]

    def i_jgz(self):
        self.ip+=1
        if not self.pop(self.stack) > 0:
            self.ip+=1
            return
        label = self.tokens[self.ip]
        self.ip = self.labels[label]

    def i_load(self):
        self.ip+=1
        alias = self.tokens[self.ip]
        if alias not in self.mem:
            self.mem[alias] = 0 # maybe should throw an error?
        self.stack.append(self.mem[alias])
        self.ip+=1
        
    def i_loadi(self):
        self.ip+=1
        alias = self.pop(self.stack)
        if alias not in self.mem:
            self.mem[alias] = 0
        self.stack.append(self.mem[alias])
        
    def i_savei(self):
        self.ip+=1
        alias = self.pop(self.stack)
        self.mem[alias] = self.pop(self.stack)

    def i_save(self):
        self.ip+=1
        alias = self.tokens[self.ip]
        self.ip+=1
        self.mem[alias] = self.pop(self.stack)
        
    def i_push(self):
        self.ip+=1
        self.stack.append( int(self.tokens[self.ip]) )
        self.ip+=1
        
    def i_dump(self):
        self.dump()
        self.ip+=1
    
    def i_del(self):
        self.pop(self.stack)
        self.ip+=1
        
    def i_exit(self):
        self.exit = True
        
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
        self.functions = {}
        self.function_stack = []
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
                "save": self.i_save,
                "savei": self.i_savei,
                "load": self.i_load,
                "loadi": self.i_loadi,
                "dump": self.i_dump,
                "push": self.i_push,
                "del": self.i_del,
                "exit": self.i_exit,
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
        #self.inp = [3, 9, 10, 5]
        #self.validate = [15, 12]
        #self.inp = [9,7,20,13]
        self.inp = [0,9,12,7,24]
        self.validate = [1,1]
        
    def run(self):
        self.ip = 0
        #while self.ip < 4:
            #print(len(self.tokens))
        while self.ip < len(self.tokens):
            #print(self.ip)
            if self.exit:
                break
            token = self.tokens[self.ip]
            self.instructions[token]()
            
    def run_empty(self):
        for i in range(3):
            self.run()
            if len(self.inp) == 0 or self.exit:
                break
            
    def is_valid(self):
        if str(self.validate) == str(self.out):
            print("Program successfully validated!")
        else:
            print("Output was incorrect.")
            self.dump()
            
    def dump(self):
        print("in:", self.inp)
        print("out:", self.out)
        print("expected:", self.validate)
        print("stack:", self.stack)
        print("lables:", self.labels)
        print("aliases:", self.mem)
        print("ip:", self.ip)
        print("last value", self.last_val)

if __name__ == "__main__":
    program = ""
    if len(sys.argv) == 1:
        program = "insert.hat"
        #program = "fib.hat"
    else:
        program = sys.argv[1]
    interp = Interpreter()
    interp.load_problem()
    interp.load_program(program)
    #interp.run_empty()
    #print(interp.tokens)
    interp.run()
    #interp.is_valid()
    #interp.dump()