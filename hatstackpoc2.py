# hatstack v 2
import sys, re, json

class Token():
    def __init__(self):
        self.val = ""
        self.type = ""
        self.method = None
        self.line = 0
        
    def __str__(self):
        out = ["value:", self.val, "type:", self.type, "line:", str(self.line)]
        return " ".join(out)
    
class Function():
    
    def throw_error(self, message):
        if not self.error:
            self.error = True
            if root!=None:
                root.error=True
            print(message)
            
    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        else:
            self.throw_error("Stack empty, nothing to pop!")
            return 0
        
    def jump(self):
        self.ip+=1
        t = self.tokens[self.ip]
        #print("jump:",t.val)
        if t.val in self.labels:
            self.ip = self.labels[t.val]
        else:
            self.throw_error("'"+t.val+"' is an invalid label")
        
    def i_load(self):
        self.ip+=1
        alias = self.tokens[self.ip].val
        if alias not in self.aliases:
            self.aliases[alias] = 0
            #self.throw_error("'"+alias+"'  is not a recognized variable.")
            # add more checks for scope and so on
            self.ip+=1
            return
        self.stack.append(self.aliases[alias])
        self.ip+=1
        
    def i_loadi(self):
        self.ip+=1
        alias = self.pop()
        if alias not in self.aliases:
            self.aliases[alias] = 0
            # add more checks for scope and so on
        self.stack.append(self.aliases[alias])
        
    def i_save(self):
        self.ip+=1
        alias = self.tokens[self.ip].val
        self.ip+=1
        self.aliases[alias] = self.pop()
        
    def i_savei(self):
        self.ip+=1
        alias = self.pop()
        self.aliases[alias] = self.pop()
        
    def i_push(self):
        self.ip+=1
        self.stack.append( int(self.tokens[self.ip].val) )
        self.ip+=1
        
    def i_add(self):
        self.stack.append( self.pop() + self.pop() )
        self.ip+=1
        
    def i_sub(self):
        val = self.pop() - self.pop()
        self.stack.append( val )
        self.ip+=1
        
    def i_mul(self):
        self.stack.append( self.pop() * self.pop() )
        self.ip+=1
        
    def i_div(self):
        self.stack.append( self.pop() // self.pop() )
        self.ip+=1
        
    def i_mod(self):
        self.stack.append( self.pop() % self.pop() )
        self.ip+=1
        
    def i_jump(self):
        self.jump()
        
    def i_jgz(self):
        if self.pop() > 0:
            self.jump()
        else:
            self.ip+=2
            
    def i_jlz(self):
        if self.pop() < 0:
            self.jump()
        else:
            self.ip+=2
            
    def i_jez(self):
        if self.pop() == 0:
            self.jump()
        else:
            self.ip+=2
            
    def i_jnz(self):
        if self.pop() != 0:
            self.jump()
        else:
            self.ip+=2
        
    def i_call(self):
        None
        
    def i_endfunc(self):
        None
        
    def i_out(self):
        self.outbox.append(self.pop())
        self.ip+=1
        
    def i_in(self):
        if len(self.inbox) > 0:
            val = self.inbox.pop()
            #print(val, self)
            self.stack.append( val )
        else:
            #self.throw_error("Inbox empty, nothing to pop!")
            self.end=True
            if self.root!=None:
                root.end=True
        self.ip+=1
        
    def i_dump(self):
        print(self)
        self.ip+=1
        
    instructions = {
            "push": i_push,
            "out": i_out,
            "in": i_in,
            "save": i_save,
            "savei": i_savei,
            "load": i_load,
            "loadi": i_loadi,
            "add": i_add,
            "sub": i_sub,
            "mul": i_mul,
            "div": i_div,
            "mod": i_mod,
            "jump": i_jump,
            "jgz": i_jgz,
            "jlz": i_jlz,
            "jez": i_jez,
            "jnz": i_jnz,
            "dump": i_dump,
            "endfunc": i_endfunc,
            }
    
    def parse(self, tokens, start):
        tokens = tokens[:]
        self.tokens.clear()
        #print("parse", start)
        aliases = []
        i = 0
        while i + start < len(tokens):
            t = tokens[i + start]
            if t.val == "endfunc":
                i+=2
                break
            if t.type == "label":
                self.labels[t.val] = i
            elif t.type == "function":
                if self.root == None:
                    f = Function(t.val, self)
                else:
                    f = Function(t.val, self.root)
                self.functions[t.val] = f
                i += f.parse(tokens, i+start+1)
                continue
            elif t.type == "alias":
                aliases.append(t)
                
            i+=1
            #print(t)
            self.tokens.append(t)
        for alias in aliases:
            if alias.val in self.functions:
                alias.type = "function_tag"
                alias.method= self.i_call
            elif alias.val in self.labels:
                #print("found",alias.val)
                alias.type = "label_tag"
            
        #print("endparse")
        return i
        
    def __init__(self, name, root):
        self.name = name
        self.tokens = []
        self.inbox = root.inbox
        self.outbox = root.outbox
        self.ip = 0
        self.stack = root.stack
        self.aliases = {}
        self.labels = {}
        self.functions = {}
        self.root = root
        self.error = False
        self.end = False
        
    def __str__(self):
        out = ["name: ", self.name, "ip:", str(self.ip), "stack:", str(self.stack)]
        #out = ["inbox:", str(self.inbox), "outbox:", str(self.outbox) "stack: ", str(self.stack)]
        #out += ["aliases", str(self.aliases)]
        return " ".join(out)
    
    def dump_tokens(self):
        i = 0
        for token in self.tokens:
            print(token)
            print(i)
            i+=1
        
    def run(self):
        self.ip = 0
        #print("running:",self.name)
        
        while self.ip < len(self.tokens):
            t = self.tokens[self.ip]
            #print(t)
            if t.type == "instruction":
                #print(t)
                t.method(self)
            elif t.type == "label":
                self.ip+=1
            elif t.type == "function_tag":
                self.functions[t.val].run()
                self.ip+=1
            else:
                self.throw_error("'"+t.val+"' on line "+ str(t.line+1) + " is not an instruction")
            if self.error or self.end:
                break
        #print(self.ip)
        #print(self)
        return self.ip
    
class Interpreter(Function):
    def __init__(self):
        self.name = "interpreter"
        self.inbox = []
        self.outbox = []
        self.valid_outbox = []
        self.tokens = []
        self.ip = 0
        self.stack = []
        self.aliases = {}
        self.labels = {}
        self.functions = {}
        self.error = False
        self.end = False
        self.problem = None
        self.program = None
        self.root = None
        
    def __str__(self):
        out = ["inbox:", str(self.inbox), "outbox:", str(self.outbox), "valid:", str(self.valid_outbox), "stack: ", str(self.stack)]
        out += ["aliases", str(self.aliases)]
        out += ["labels", str(self.labels)]
        out += ["ip", str(self.ip)]
        return " ".join(out)
        
    def is_number(self, string):
        match = re.search("[0-9]",string)
        if match:
            if match.span()[0] == 0:
                return True
        return False
        
    def tokenize(self, tokens, line_num):
        #print(tokens)
        for token in tokens:
            t = Token()
            t.val = token
            t.line = line_num
            if token in self.instructions:
                t.type = "instruction"
                t.method = self.instructions[token]
            elif token[0]=="#":
                t.val = token[1:]
                t.type = "label"
            elif token[0]=="@":
                t.val = token[1:]
                t.type = "function"
            elif self.is_number(token):
                t.type = "literal"
            else:
                t.type = "alias"
            self.tokens.append(t)
        
    def create_problem(self, filename, inbox, valid_outbox):
        problem = {
                "inbox": inbox,
                "valid_outbox": valid_outbox
                }
        f = open(filename, "w")
        f.write(json.dumps(problem))
        f.close()
        
    def load_problem(self, filename):
        f = open(filename)
        problem = json.loads(f.read())
        self.inbox = problem["inbox"]
        self.inbox.reverse()
        self.valid_outbox = problem["valid_outbox"]
        f.close()
        
    def load_program(self, filename):
        f = open(filename)
        line_num = 0
        for line in f.readlines():
            comment = line.find("//")
            if comment != -1:
                line = line[:comment]
            line = line.lower().split()
            if len(line) == 0:
                line_num+=1
                continue
            self.tokenize(line, line_num)
            line_num+=1
        f.close()
        self.parse(self.tokens, 0)
        
    def validate(self):
        if str(self.outbox) == str(self.valid_outbox):
            print("Solution successfully validated!")
            return True
        else:
            print("Output is not correct.")
            return False
		
if __name__ == "__main__":
	
	interp = Interpreter()
	if len(sys.argv) > 2:
		interp.load_problem(sys.argv[1])
		interp.load_program(sys.argv[2])
	else:
		interp.load_problem("insert.prob")
		interp.load_program("insert.hat")
	#interp.load_program("functiontest.hat")
	#print(interp)
	#interp.dump_tokens()
	interp.run()
	#print(interp)
	interp.validate()
        
#interpreter.create_problem("fib.prob", [9], [1,1,2,3,5,8])