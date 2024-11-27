class Instruction_Manager:
    def __init__(self,instru):
        self.instru = instru #initialising instruction
        self.state = "UNFETCHED" #state is set to unfetched as initially no instruction is fetched
        self.instrtype = "NULL"  #instruction type is set to NULL examples->I,R,J Types
        self.op = 'NULL' #opcode is set to NULL
        self.regs = [] #empty list of registers 
        self.imm = 'NULL' #immediate is set to NULL
        self.shamt = 'NULL' #Shift amount used in R type instruction
        self.targetaddr  = "NULL" #Target address is set to NULL
        self.result = -1 #The default initial value of result is set to -1
        self.loader = 'NULL' #the loader is set to NULL
        self.to_Branch = False #The branch is set to False as initially branch is not taken, Made true when required
        
    def __str__(self): # For printing the object 
        return (f'{self.instru}  : {self.state}') #prints the instruction and it's state
    
    def Fetched(self): #After fetching initialised to fetched
        self.state = "FETCHED" #State is set to fetched
        
    def isFetched(self):
        if(self.state == "FETCHED"): #if the state is fetched return true else false
            return True
        else:
            return False
        
    def Decoded(self,command,opcode_map): #Decodes the instruction by it's op code
        self.state = "DECODED" #Once the instruction arrives at this stage, it gets 
        self.instrtype = command[0] #A string that contains decoded information
        if(command[:3]!='JAL'): #if it is not JAL, as it is defined differently for JAL
            if(self.instrtype=='R'): #R type instruction
                self.regs.append(command[7:12])#rs->Appending into the registers 7:12->0th index is the instruction type and the rest is the instruction
                self.regs.append(command[12:17])#rt->Appending into the registers->12:17
                self.regs.append(command[17:22])#rd->Appending into the registers->17:22
                self.shamt = command[22:27]#shift amount->Appending into the registers->22:27
                self.op = opcode_map[command[1:7]][0]#operation->Using opcode mapper
            elif(self.instrtype == 'I'): #I type instruction
                self.regs.append(command[7:12])#rs->Appending into the registers 7:12->0th index is the instruction type and the rest is the instruction
                self.regs.append(command[12:17])#rt->Appending into the registers->12:17
                self.regs.append("NULL")#there is no rd for I type instructions
                self.imm = command[17:]#Immediate field for I type instruction
                self.op = opcode_map[command[1:7]][0]#operation>Using opcode mapper
            elif(self.instrtype=='M'): #M type->As Mul is not R type
                self.regs.append(command[7:12])#rs->Appending into the registers 7:12->0th index is the instruction type and the rest is the instruction
                self.regs.append(command[12:17])#rt->Appending into the registers->12:17
                self.regs.append(command[17:22])#rd->Appending into the registers->17:22
                self.shamt = command[22:27]#shift amount->Appending into the registers->22:27
                self.op = opcode_map[command[1:7]][0]#operation->Using opcode mapper
            elif(self.instrtype=='J'): #J type instruction
                self.targetaddr = command[1:]#Target address is now set to 31 bits except the first bit as it is J
                self.regs.append('NULL')#Add NULL into the register as there is no rs
                self.regs.append("NULL")#Add NULL into the register as there is no rt
                self.regs.append("NULL")#Add NULL into the register as there is no rd
                self.op = 'jump' #updating the op to jump

    def isDecoded(self): #Function to check if it is decoded
        if(self.state == "DECODED"): #if decoded return true else false
            return True
        else:
            return False
    
    def Executed(self,result): #Changing the state to executed
        self.state = "EXECUTED"
        self.result = result
        
    def isExecuted(self): #Function to check if it is Executes
        if(self.state == "EXECUTED"): #if executed return true else false
            return True
        else:
            return False    
    
    def Mem_Accessed(self): #Changing the state to Mem accessed
        self.state = "MEMACCESSED"

    def isMem_Accessed(self): #Function to check if it is Accessed by memory
        if(self.state == "MEMACCESSED"): #if decoded return true else false
            return True
        else:
            return False
        
    def Writtenback(self): #It is then written back into the register memory
        self.state = "WRITTENBACK"

    def isWrittenback(self): #Function to check if it is Written back into memory
        if(self.state == "WRITTENBACK"): #if write back return true else false
            return True
        else:
            return False
def Instru_Fetch(Instru_memory,PC): #Returning each line of Instruction
    if(PC<len(Instru_memory)):
        return Instru_memory[PC]
    else: 
        return -1 #else return -1

def binaryToDecimal(val, bits): #converting binary into decimal
    if val & (1<<(bits-1)):  # High bit set indicates its a negative value
        return -(2**bits-val)
    return val  # Positive value.

def Instru_Decode(instruction,opcode_map,Reg_memory,LUIN): #Least unfetched instruction->LUIN
    command = '' #empty string command
    instr_string = instruction.instru #32-bit instruction->1 line from the machine code
    opcode = instr_string[0:6]#opcode initialised to first 6 bits
    List = ["000000","011100","00011"]
    if(opcode == List[0]):#if opcode is 000000
        command += 'R'#Rtype
        funct = instr_string[-6:]#function field last 6 bits
        # command += opcode_map[funct][0]
        command += funct #adding function field to command(empty string)
        rs  = instr_string[6:11]#rs is the 6 to 11 bits of the instruction
        rt  = instr_string[11:16]#rt is the 11 to 16 bits of the instruction
        rd  = instr_string[16:21]#rd is the 16 to 21 bits of the instruction
        shamt = instr_string[21:26]#shift amount is the 21 to 26 bits of the instruction
        # if(opcode_map[funct][0]!='sll')  
        command += rs + rt + rd + shamt #final all of them are added to the command string
    elif(opcode == List[1]): #if opcode is 011100
        command += 'M' #For M type
        command += opcode #Adding opcode into the command
        rs = instr_string[6:11] #rs is the 6 to 11 bits of the instruction
        rt = instr_string[11:16]#rt is the 11 to 16 bits of the instruction
        rd = instr_string[16:21]#rd is the 16 to 21 bits of the instruction
        command += rs + rt + rd #final all of them are added to the command string
    elif(opcode_map[opcode][1]=='I'): # for I type
        command += 'I'  #For I type
        command += opcode #Adding opcode into the command
        rs  = instr_string[6:11]#rs is the 6 to 11 bits of the instruction
        rt  = instr_string[11:16]#rt is the 11 to 16 bits of the instruction
        imm = instr_string[16:]#rd is the 16 to 32 bits of the instruction
        print(f'instr: {instr_string}') # print the instruction
        print(f'imm:   {imm}') #print the 16 to 32 bits that is immediate field
        command += rs + rt + imm
    elif(opcode_map[opcode][1]=='J'): #For J type
        if(opcode==List[2]): #00011->opcode
            command+='JAL' #It is JAL
            command+=instr_string[6:] #adding the bits after 6 bits in the command
            Reg_memory['$ra'] = LUIN #If JAL, used for return so ra
        else:
            command += 'J' #J type added
            # command += opcode
            trgt = instr_string[6:]
            command += trgt #Target is also added(26 bits)
    return command #Example-> R rs rt rd shamt function
def Execute(instruction,Reg_memory): #Execute
    non_Jtype = False #If it is J type then true
    result2 = 0
    if(instruction.instrtype != 'J'): #If not J type
        non_Jtype = True 
        print(instruction.regs[0])
        rs = Reg_memory[int(instruction.instru[6:11],2)] #Register memory is updated with the 6 to 11 bits rs
        rt = Reg_memory[int(instruction.instru[11:16],2)] #Register memory is updated with the 6 to 11 bits rt
        op = instruction.op #Opcode
        print(rs,rt,op) #Printing rs,rt,op
        if(instruction.instrtype == 'R'): #If the instruction is add type
            rd = int(instruction.regs[2],2) # 16:21 bits converting into decimal
            if(op == 'add'): #if opcode is add
                result2  = rs + rt #Then result is addition of the registers
            elif(op == 'sub'): #if iocode is subtract
                result2 = rs - rt #Then result is subtraction
            elif(op=='slt'): #If opcode is slt
                if(rs<rt): #if rs<rt then 1 else 0
                    result2=1
                else:
                    result2=0    
        elif(instruction.instrtype == 'I'): #For I type instruction
            imm = binaryToDecimal(int(instruction.imm,2),16) #Converting binary integer into decimal,sign extend 
            print(imm)
            # print(type(imm),type(rs))
            if(op == 'lw' or op =='sw'): #if opcode is lw or sw
                result2 = rs + imm #result is the addition of rs and imm
            elif(op=='addi'): #if opcode is addi
                result2 = rs + imm ##result is the addition of rs and imm
            elif(op=='beq'): #if opcode is beq
               if(rs==rt):
                   result2 = 1 #result is set to 1 else 0
               else:
                   result2 = 0
            elif(op=='bne'): #opposite of beq for bne
                if(rs!=rt):
                    result2= 1
                else:
                    result2= 0
        elif(instruction.instrtype == 'M'): #For M type
            rd = instruction.regs[2] 
            result2  = rs * rt #Multiplication of 2 values in registers 
    if(non_Jtype):
        return result2#If it is non Jtype then return the result else not
    return -1
def Mem_Access(instruction,Data_memory,Reg_memory,result): # Mem access function 
    loader = 0 #Loader initialised to 0
    if(instruction.instrtype=='I'): #If I type instruction
        if(instruction.op == 'lw'): 
            loader = Data_memory[result] #load the result from the data memory into loader
        elif(instruction.op=='sw'):
            Data_memory[result] = Reg_memory[int(instruction.regs[1],2)]#Storing the result from data memory into register memory 
    return (Data_memory,loader) #returns the data memory and the loader

def Writeback(instruction,Reg_memory,result,loader): #Write back function
    if(instruction.instrtype == 'R'): #R type
        Reg_memory[int(instruction.regs[2],2)] = result #Writing back into the memory for R type
    elif(instruction.op=='lw'):
        Reg_memory[int(instruction.regs[1],2)] = loader #Writing back into the memory for lw type
    elif(instruction.op=='addi'):
        Reg_memory[int(instruction.regs[1],2)] = result #Writing back into the memory for I(addi) type
    return Reg_memory
def mapper(): #Mapper 
    opcodef = open('opcodemapper.txt') #opening both the mappers to form the dictionaries
    regcodef = open('regcodemapper.txt')
    opcode_map ={}
    regcode_map = {}     
    for instru in opcodef: #Instruction in opcodemapper
        myinstru = instru.split()
        if myinstru[1]=='R': #If R type
            opcode_map[myinstru[3]]=(myinstru[0],myinstru[1]) #function->Add,R
        elif myinstru[1]=='I': #For I type
            opcode_map[myinstru[2]]=(myinstru[0],myinstru[1]) #function->I type
        elif myinstru[1]=='J': 
            opcode_map[myinstru[2]] = (myinstru[0],myinstru[1]) #For J type
        elif myinstru[1]=='M':
            opcode_map[myinstru[2]]=(myinstru[0],myinstru[1]) #For M type
    for reg in regcodef:
        print(reg) #print register
        myreg = reg.split()  #the reg is split
        print(myreg)
        if(len(myreg)>=2): #if length in more than or equal to 2 
            print(myreg[1],myreg[0])
            regcode_map[myreg[1]]=myreg[0]         
    opcodef.close #closing the mapper
    regcodef.close
    return (opcode_map,regcode_map) #returning both of them

Reg_memory = [] #empty register list
for i in range(32):
    Reg_memory.append(0) #all 0's in reg memory
Data_memory = {} #Data memory empty dictionary
p = mapper()
opcode_map = p[0] #opcode mapper
for x in range(25):
    Data_memory[4*x]=0#memory contains 4 bits(1 word or instruction)
print('Choose an option:')
print('1.Sorting')
print('2.Fibonacci')
i = int(input()) #choose 1 or 2
Sort_list=[]
if(i==1):
    input_file = open('Bubble_sort.txt') #machine code for sorting
elif(i==2):
    input_file=open('fibonacci.txt')
if(i==1): #if sorting
    x = int(input())#Number of numbers to be sorted
    Reg_memory[9] = x
    p = input().split() #taking input of the numbers from the user
    v = 0
    for l in p:
        if(v==x):
            break
        z = int(l)
        Sort_list.append(z)
    k = 0
    if(len(Sort_list)<8): #Maximum limit is 8 to take the input from the user
        for ele in Sort_list:
            Data_memory[4*k] = ele #the data memory is update
            k+=1
    Reg_memory[10] = 0
    Reg_memory[11] = 40
    
Instru_memory = [Instruction_Manager(instruction[0:len(instruction)-1]) for instruction in input_file] #Each instruction
LUIN = 0
clock_cycles = 0 #clock cycles is set to 0
while LUIN < len(Instru_memory):
    myinstr = Instru_Fetch(Instru_memory,LUIN) #fetching the instruction
    myinstr.Fetched() #fetched the instruction
    command = Instru_Decode(myinstr,opcode_map,Reg_memory,LUIN) #Decode the instruction
    print(command) #print the command decoded
    myinstr.Decoded(command,opcode_map) #decoded the instruction
    result = Execute(myinstr,Reg_memory) #Execute the instruction
    myinstr.Executed(result) #execution completed
    print(f'result{result}') #print the result
    if(myinstr.instrtype=='J'): #For J type instruction
        print(myinstr.targetaddr) #Target address
        print(int(myinstr.targetaddr,2)) #converting into decimal the target address
        to_set_LUIN = int(myinstr.targetaddr,2) - 1048576 - 1 #----------------------------------------
    if(myinstr.op=='lw'):
        Reg_memory[int(myinstr.instru[11:16],2)] = Data_memory[result] #for lw loading from the memory
    elif(myinstr.op=='sw'):
        Data_memory[result] = Reg_memory[int(myinstr.instru[11:16],2)]  #storing to the memory
    if(myinstr.instrtype=='R'): #If R type
       Reg_memory[int(myinstr.instru[16:21],2)] = result #The final result from R type
    elif(myinstr.instrtype=='I'): #If I type
        if(myinstr.op=='addi'): #If opcode is related ot addi
            Reg_memory[int(myinstr.instru[11:16],2)] = result  #The final result from I(addi) type
    LUIN = LUIN + 1 #LUIN is incremented by 1
    clock_cycles+=5 #clock_cycles increased by 5 as it is non pipelined
    if(myinstr.op=='beq'): #For Beq instruction
        imm = binaryToDecimal(int(myinstr.imm,2),16)  #converting the immediate field into 16 bit field
        if(result ==1): #if result is 1, the LUIN is added to imm
            LUIN += imm
    elif(myinstr.op=='bne'): #for bnwe instruction
        imm = binaryToDecimal(int(myinstr.imm,2),16) #converting the immediate field into 16 bit field
        if(result ==1): #if the result is 1 then LUIN is added to immediate
            LUIN += imm
    elif(myinstr.op=='jump'): #for jump instruction
        LUIN = to_set_LUIN+1 #LUIN is incremented for jump in this situation,assigns target address
    print(f"LUIN: {LUIN}") #printing 
print(f'Register Memory:{Reg_memory}') #printing the register memory
print(f'Data Memory: {Data_memory}') #printing the data memory
i = 0
print(f'clock cycles: {clock_cycles}') #total number of clock cycles