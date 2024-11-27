class Instruction_Manager:
    
    def __init__(self,instru,indx):
        self.instru = instru
        self.indx=indx
        self.state = "UNFETCHED"
        self.instrtype = "NULL"
        self.op = 'NULL'
        self.regs = []
        self.imm = 'NULL'
        self.shamt = 'NULL'
        self.targetaddr  = "NULL"
        self.result = -1
        self.loader = 'NULL'
        self.to_Branch = False
        self.to_set_LUIN = -1
        
    def __str__(self):
        return (f'{self.instru}  : {self.state}')
    
    def Fetched(self):
        self.state = "FETCHED"
        
    def isFetched(self):
        if(self.state == "FETCHED"):
            return True
        else:
            return False
        
    def Decoded(self,command,opcode_map):
        self.state = "DECODED"
        self.instrtype = command[0]
        if(command[:3]!='JAL'):
            if(self.instrtype=='R'):
                self.regs.append(command[7:12])#rs
                self.regs.append(command[12:17])#rt
                self.regs.append(command[17:22])#rd
                self.shamt = command[22:27]
                self.op = opcode_map[command[1:7]][0]#operation
            elif(self.instrtype=='I'):
                self.regs.append(command[7:12])#rs
                self.regs.append(command[12:17])#rt
                self.regs.append("NULL")#there is no rd for I type instructions
                self.imm = command[17:]
                self.op = opcode_map[command[1:7]][0]#operation
            elif(self.instrtype=='M'):
                self.regs.append(command[7:12])#rs
                self.regs.append(command[12:17])#rt
                self.regs.append(command[17:22])#rd
                self.shamt = command[22:27]
                self.op = opcode_map[command[1:7]][0]#operation 
            elif(self.instrtype=='J'):
                self.targetaddr = command[1:]
                self.regs.append('NULL')#rs
                self.regs.append("NULL")#rt
                self.regs.append("NULL")#rd 
                self.op = 'jump'

    def isDecoded(self):
        if(self.state == "DECODED"):
            return True
        else:
            return False
    
    def Executed(self,result):
        self.state = "EXECUTED"
        self.result = result
        
    def isExecuted(self):
        if(self.state == "EXECUTED"):
            return True
        else:
            return False    
    
    def Mem_Accessed(self):
        self.state = "MEMACCESSED"

    def isMem_Accessed(self):
        if(self.state == "MEMACCESSED"):
            return True
        else:
            return False
        
    def Writtenback(self):
        self.state = "WRITTENBACK"

    def isWrittenback(self):
        if(self.state == "WRITTENBACK"):
            return True
        else:
            return False
def Instru_Fetch(Instru_memory,PC):
    if(PC<len(Instru_memory)):
        return Instru_memory[PC]
    else: 
        return -1
    

def binaryToDecimal(val, bits):
    if val & (1<<(bits-1)):  # High bit set indicates its a negative value
        return -(2**bits-val)
    return val  # Positive value.

def Instru_Decode(instruction,opcode_map,Reg_memory,LUIN):
    command = ''
    instr_string = instruction.instru
    opcode = instr_string[0:6]
    if(opcode == '000000'):
        command += 'R'#Rtype
        funct = instr_string[-6:]
        # command += opcode_map[funct][0]
        command += funct
        rs  =  instr_string[6:11]
        rt  = instr_string[11:16]
        rd  = instr_string[16:21]
        shamt = instr_string[21:26]
        # if(opcode_map[funct][0]!='sll')  
        command += rs + rt + rd + shamt
    elif(opcode=='011100'):
        command += 'M'
        command += opcode
        rs  =  instr_string[6:11]
        rt  = instr_string[11:16]
        rd = instr_string[16:21]
        command += rs + rt + rd
    elif(opcode_map[opcode][1]=='I'):
        command += 'I'
        command += opcode
        rs  =  instr_string[6:11]
        rt  = instr_string[11:16]
        imm = instr_string[16:]
        print(f'instr: {instr_string}')
        print(f'imm:   {imm}')
        command += rs + rt + imm
    elif(opcode_map[opcode][1]=='J'):
        if(opcode=="000011"):
            command+='JAL'
            command+=instr_string[6:]
            Reg_memory['$ra'] = LUIN
        else:
            command += 'J'
            # command += opcode
            trgt = instr_string[6:]
            command += trgt
    return command
def Execute(instruction,Reg_memory,source,Hazard_result):
    non_Jtype = False
    result2 = 0
    if(instruction.instrtype != 'J'):
        non_Jtype = True
        # print(instruction.regs[0])
        if(source==0):
            rs = Reg_memory[int(instruction.instru[6:11],2)]
            rt = Reg_memory[int(instruction.instru[11:16],2)]
        elif(source==1):
            rs = Hazard_result
            rt = Reg_memory[int(instruction.instru[11:16],2)]
        elif(source==2):
            rs = Reg_memory[int(instruction.instru[6:11],2)]
            rt = Hazard_result
        op = instruction.op
        print(rs,rt,op)
        if(instruction.instrtype == 'R'):
            rd = int(instruction.regs[2],2)
            if(op == 'add'):
                result2  = rs + rt
            elif(op == 'sub'):
                result2 = rs - rt
            elif(op=='slt'):
                if(rs<rt):
                    result2=1
                else:
                    result2=0    
        elif(instruction.instrtype == 'I'):
            imm = binaryToDecimal(int(instruction.imm,2),16)
            print(imm)
            print(type(imm),type(rs))
            if(op == 'lw' or op =='sw'):
                result2 = rs + imm
            elif(op=='addi'):
                result2 = rs + imm
            elif(op=='beq'):
               if(rs==rt):
                   result2 = 1
               else:
                   result2 = 0
            elif(op=='bne'):
                print(f'bne, {instruction}, rs: {rs}, rt:{rt}')
                if(rs!=rt):
                    result2= 1
                else:
                    result2= 0
        elif(instruction.instrtype == 'M'):   
            rd = instruction.regs[2]
            result2  = rs * rt
    if(non_Jtype):
        return result2
    return -1
def Mem_Access(instruction,Data_memory,Reg_memory,result):
    loader = 0
    if(instruction.instrtype=='I'):
        if(instruction.op == 'lw'):
            loader = Data_memory[result]
        elif(instruction.op=='sw'):
            Data_memory[result] = Reg_memory[int(instruction.regs[1],2)]
    return (Data_memory,loader)

def Writeback(instruction,Reg_memory,result,loader):
    if(instruction.instrtype == 'R'): 
        Reg_memory[int(instruction.regs[2],2)] = result
    elif(instruction.op=='lw'):
        Reg_memory[int(instruction.regs[1],2)] = loader 
    elif(instruction.op=='addi'):
        Reg_memory[int(instruction.regs[1],2)] = result
    return Reg_memory
    

def reg_initializer(Regcode_map,Reg_memory):
    for p in Regcode_map.values():
        Reg_memory[p] = 0
    return Reg_memory
def mapper():
    opcodef = open('opcodemapper.txt')
    regcodef = open('regcodemapper.txt')
    opcode_map ={}
    regcode_map = {}    
    for instru in opcodef:
        myinstru = instru.split()
        if myinstru[1]=='R':
            opcode_map[myinstru[3]]=(myinstru[0],myinstru[1])
        elif myinstru[1]=='I':
            opcode_map[myinstru[2]]=(myinstru[0],myinstru[1])
        elif myinstru[1]=='J': 
            opcode_map[myinstru[2]] = (myinstru[0],myinstru[1])
        elif myinstru[1]=='M':
            opcode_map[myinstru[2]]=(myinstru[0],myinstru[1])
    for reg in regcodef:
        print(reg)
        myreg = reg.split()
        print(myreg)
        if(len(myreg)>=2):
            print(myreg[1],myreg[0])
            regcode_map[myreg[1]]=myreg[0]         
    opcodef.close
    regcodef.close
    return (opcode_map,regcode_map)


Reg_memory = [0]*32
Data_memory = {}
p = mapper()
opcode_map = p[0]
for x in range(25):
    Data_memory[4*x]=0
print('Choose an option:')
print('1.Sorting')
print('2.Fibonacci')
i = int(input())
Sort_list=[]
if(i==1):
    input_file = open('Output.txt')
elif(i==2):
    input_file=open('fibonacci.txt')
if(i==1):
    
    x = int(input())
    Reg_memory[9] = x
    p = input().split()
    v = 0
    for l in p:
        if(v==x):
            break
        z = int(l)
        Sort_list.append(z)
    k = 0
    if(len(Sort_list)<8):
        for ele in Sort_list:
            Data_memory[4*k] = ele
            k+=1
    Reg_memory[10] = 0
    Reg_memory[11] = 40

Instru_memory = []
indx = 0
for instruction in input_file:
    Instru_memory.append(Instruction_Manager(instruction[0:len(instruction)-1],indx))
# Instru_memory = [Instruction_Manager(instruction[0:len(instruction)-1]) for instruction in input_file]
clock_cycles  = 0
PC = 0
IF_ID = ''
prevIF_ID = ''
ID_EX = ''
prevID_EX = ''
EX_MEM = ''
prevEX_MEM = ''
MEM_WB = '' 
prevMEM_WB = ''
Removed_instr = ''
LUIN = 0 #stands for 'latest unfetched instruction'
LFIN = -1 #'latest fetched instruction'
LDIN = -1 #'latest decoded instruction'
LEIN = -1 #'latest executed instruction'
LMIN = -1 #'latest mem_accessed instruction'
LWIN = -1 #'latest writtenback instruction'
end_fetching = False
end_decoding = False
end_executing = False
end_memaccessing = False
end_writingback = False
LUIN_stack = [0]

Running_instructions = []
should_run = True
Has_been_branched = 0
skip = False
total_num_stalls=0
num_stalls = 0
stall = False
jump = False
while(should_run):
    print(f'LUIN{LUIN} LUINstak[-1]{LUIN_stack[-1]} LFIN{LFIN} LDIN{LDIN} LEIN{LEIN} LMIN{LMIN} LWIN{LWIN}')
    if(LFIN==-1 and LUIN==LUIN_stack[-1]+1):
        LFIN = LUIN_stack[-1]
    if(LDIN==-1 and (LUIN==LUIN_stack[-1]+2 or LFIN==LUIN_stack[-1]+1)):
        LDIN = LUIN_stack[-1]
    if(LEIN ==-1 and (LUIN==LUIN_stack[-1]+3 or LFIN==LUIN_stack[-1]+2 or LDIN ==LUIN_stack[-1]+1)):
        LEIN = LUIN_stack[-1]
    if(LMIN==-1 and (LUIN==LUIN_stack[-1]+4 or LFIN==LUIN_stack[-1]+3 or LDIN==LUIN_stack[-1]+2 or LEIN==LUIN_stack[-1]+1)):
        LMIN = LUIN_stack[-1]
    if(LWIN==-1 and (LUIN==LUIN_stack[-1]+5 or LFIN==LUIN_stack[-1]+4 or LDIN==LUIN_stack[-1]+3 or LEIN==LUIN_stack[-1]+2 or LMIN==LUIN_stack[-1]+1)):
        LWIN = LUIN_stack[-1] 
    print(f'LUIN{LUIN} LUINstak[-1]{LUIN_stack[-1]} LFIN{LFIN} LDIN{LDIN} LEIN{LEIN} LMIN{LMIN} LWIN{LWIN}')
    if(LUIN < len(Instru_memory) and (not end_fetching)):
        if(LUIN==len(Instru_memory)-1):
            end_fetching=True
        myinstr = Instru_Fetch(Instru_memory,LUIN) #'myinstr' is an instance of 'Instruction_Manager'
        myinstr.Fetched()
        print(f'{myinstr} {LUIN} {clock_cycles}')
        Instru_memory[LUIN] = myinstr #the instruction's state is modified to 'FETCHED'
        Running_instructions.append(myinstr)
        IF_ID = myinstr
        if(myinstr.instru[0:6]=='000010'):#jump instru
            trgtLUIN = binaryToDecimal(int(myinstr.instru[6:],2),26) - 1048576 - 1
            if(trgtLUIN<len(Instru_memory)):
                LUIN = trgtLUIN
            LUIN_stack.append[LUIN+1]
            jump = True
        # if(LUIN==1):
        # if(LUIN==LUIN_stack[-1]+1):
        #     LFIN = LUIN_stack[-1]
        # if(LUIN==LUIN_stack[-1]+2 or LFIN==LUIN_stack[-1]+1):
        #     LDIN = LUIN_stack[-1]
        # if(LUIN==LUIN_stack[-1]+3 or LFIN==LUIN_stack[-1]+2 or LDIN ==LUIN_stack[-1]+1):
        #     LEIN = LUIN_stack[-1]
        # if(LUIN==LUIN_stack[-1]+4 or LFIN==LUIN_stack[-1]+3 or LDIN==LUIN_stack[-1]+2 or LEIN==LUIN_stack[-1]+1):
        #     LMIN = LUIN_stack[-1]
        # if(LUIN==LUIN_stack[-1]+5 or LFIN==LUIN_stack[-1]+4 or LDIN==LUIN_stack[-1]+3 or LEIN==LUIN_stack[-1]+2 or LMIN==LUIN_stack[-1]+1):
        #     LWIN = LUIN_stack[-1]

    if len(Running_instructions)==0:
        should_run = False
        break#The program was successfully executed
    
    # if(LUIN-1>=0 and LUIN-1 < len(Instru_memory) and len(Running_instructions)>1 and Running_instructions[-1].isFetched()):
    # for instr in Running_instructions:
    #     if(instr.isFetched()):
    #         LFIN = instr.indx
    if(LFIN >= 0 and (not end_decoding) and (not jump)):
        if LFIN == len(Instru_memory)-1:
            end_decoding=True
        command = Instru_Decode(Instru_memory[LFIN],opcode_map,Reg_memory,LFIN)
        # print(f'command : {command}')
        Running_instructions.remove(Instru_memory[LFIN])
        Instru_memory[LFIN].Decoded(command,opcode_map)
        decoded_instr = Instru_memory[LFIN]
        Running_instructions.append(decoded_instr)
        print(f'{decoded_instr} {LFIN} {clock_cycles}')
        ID_EX = decoded_instr
        
        
    # if(LUIN-2>=0 and LUIN-2 < len(Instru_memory) and len(Running_instructions)>2 and Running_instructions[-2].isDecoded()):
    if(LDIN>=0 and (not end_executing) and (not jump)):
        if LDIN == len(Instru_memory)-1:
            end_executing = True
        # print(Reg_memory)
        exec_instr = Instru_memory[LDIN]
        # Load_Hazard = False
        Hazard_result = -1
        source=0
        if(EX_MEM!=''):
            if(exec_instr.instru[16:21]==EX_MEM.instru[6:11]):#data hazard
                source=1
                Hazard_result = EX_MEM.result
            elif(exec_instr.instru[16:21]==EX_MEM.instru[11:16]):#data hazard
                source=2
                Hazard_result = EX_MEM.result
        # if(EX_MEM!='' and EX_MEM.op=='lw' and (exec_instr.instru[16:21]==MEM_WB.instru[6:11] or exec_instr.instru[16:21]==EX_MEM.instru[11:16]) and num_stalls==0):
        #     stall = True
        #     total_num_stalls+=1
        #     num_stalls = 1
        # elif(EX_MEM!='' and EX_MEM.op=='lw' and (exec_instr.instru[16:21]==MEM_WB.instru[6:11] or exec_instr.instru[16:21]==EX_MEM.instru[11:16]) and not stall):
        #     stall = False
        #     if(exec_instr.instru[16:21]==MEM_WB.instru[6:11]):#load hazard
        #         source=1
        #         Hazard_result = Data_memory[MEM_WB.result]
        #     elif(exec_instr.instru[16:21]==MEM_WB.instru[11:16]):#load hazard
        #         source=2
        #         Hazard_result = Data_memory[MEM_WB.result]
            
        if(not stall):
            result  = Execute(Instru_memory[LDIN],Reg_memory,source,Hazard_result)
            # print(f'result:{result}')
            # exec_instr = Instru_memory[LDIN]
            Running_instructions.remove(Instru_memory[LDIN])
            Instru_memory[LDIN].Executed(result)
                # Running_instructions[-2] = exec_instr
            Running_instructions.append(Instru_memory[LDIN])
                # Instru_memory[LDIN] = exec_instr
            exec_instr = Instru_memory[LDIN]
            print(f'{exec_instr} {exec_instr.op} {exec_instr.regs} {exec_instr.result} {LDIN} {clock_cycles}')
            EX_MEM = exec_instr 
            
            if((Instru_memory[LDIN].op == 'beq' and result == 1) or (Instru_memory[LDIN].op == 'bne' and result == 1)):
                Instru_memory[LDIN].to_Branch = True
                beq_instr = Instru_memory[LDIN]
                # prev_beq_instr = Instru_memory[LEIN]
                # tprev_beq_instr = Instru_memory[LMIN]
                LUIN_stack.append(LUIN+binaryToDecimal(int(Instru_memory[LDIN].imm,2),16)+1)
                flusher = []
                for instr in Running_instructions:
                    if(instr.isFetched() or instr.isDecoded()):
                        flusher.append(instr)
                print('FLUSHER{')       
                for rem_instr in flusher:   
                    print(rem_instr,rem_instr.op) 
                    Running_instructions.remove(rem_instr)
                print('}')
                print('Runninginstr{')
                for instr in Running_instructions:
                    print(instr,instr.op)
                print('}') 
                #We have to complete the execution of the instructions in the pipeline
                #1 clock cycle: previous instruction's MemAccess and 2nd last instruction's Writeback
                if(len(Running_instructions)>0):
                    if((LEIN>=0 and (not end_memaccessing))):
                        if LEIN == len(Instru_memory)-1:
                            end_memaccessing = True
                        # Data_memory = Mem_Access(Instru_memory[LEIN],Data_memory,Reg_memory)
                        memaccessesed_instr = Instru_memory[LEIN]
                        Running_instructions.remove(memaccessesed_instr)
                        # memaccessesed_instr = Running_instructions[-3]
                        # memaccessesed_instr.Mem_Accessed()
                        # Running_instructions[-3]=memaccessesed_instr
                        result = memaccessesed_instr.result
                        if(memaccessesed_instr.instrtype=='J'):
                            print(memaccessesed_instr.targetaddr)
                            print(int(myinstr.targetaddr,2))
                            memaccessesed_instr.to_set_LUIN = int(myinstr.targetaddr,2) - 1048576 - 1
                        if(memaccessesed_instr.op=='lw'):
                            # Reg_memory[int(memaccessesed_instr.instru[11:16],2)] = Data_memory[result]
                            memaccessesed_instr.loader = Data_memory[result]
                        elif(memaccessesed_instr.op=='sw'):
                            Data_memory[result] = Reg_memory[int(myinstr.instru[11:16],2)] 
                        
                        memaccessesed_instr.Mem_Accessed()
                        Running_instructions.append(memaccessesed_instr)
                        Instru_memory[LEIN] = memaccessesed_instr
                        print(f'{memaccessesed_instr} {LEIN} {clock_cycles}')
                        MEM_WB = memaccessesed_instr
                        
                    if((LMIN>=0 and (not end_writingback))):
                        if LMIN == len(Instru_memory)-1:
                            end_writingback = True
                        writtenback_instr = Instru_memory[LMIN] 
                        Running_instructions.remove(writtenback_instr)
                        result = writtenback_instr.result
                        if(writtenback_instr.instrtype=='R'):
                            Reg_memory[int(writtenback_instr.instru[16:21],2)] = result
                        elif(writtenback_instr.instrtype=='I'):
                            if(myinstr.op=='addi'):
                                Reg_memory[int(writtenback_instr.instru[11:16],2)] = result
                            if(writtenback_instr.op=='lw'):
                                Reg_memory[int(writtenback_instr.instru[11:16],2)] = Data_memory[result]
                                # memaccessesed_instr.loader = Data_memory[result]
                        # Reg_memory = Writeback(Instru_memory[LMIN],Reg_memory)
                        # Reg_memory = Writeback(Running_instructions[-4],Reg_memory)
                        # writtenback_instr = Running_instructions[-4]
                        writtenback_instr.Writtenback()
                        # Running_instructions[-4] = writtenback_instr
                        Running_instructions.append(writtenback_instr) 
                        Instru_memory[LMIN] = writtenback_instr
                        print(f'{writtenback_instr} {LMIN} {clock_cycles}')
                        # Removed_instr = writtenback_instr
                        
                    clock_cycles+=1
                    
                    if(LDIN>=0 and LDIN+1<len(Instru_memory)):
                        LDIN+=1
                    if(LEIN>=0 and LEIN+1<len(Instru_memory)):
                        LEIN+=1
                    if(LMIN>=0 and LMIN+1<len(Instru_memory)):
                        LMIN+=1
                    if(LWIN>=0 and LWIN+1<len(Instru_memory)):
                        LWIN+=1
                print('cyc2Runninginstr{')
                for instr in Running_instructions:
                    print(instr,instr.op)
                print('}')     

                if(len(Running_instructions)>0):
                    l = LUIN + binaryToDecimal(int(beq_instr.imm,2),16)+1
                    print(f'trgt LUIN{LUIN} {len(Instru_memory)} {end_fetching}')
                    if(l < len(Instru_memory)):
                        LUIN = l
                        print(f'trgt LUIN{LUIN}')
                        #fetching the instruction at target address
                        if(LUIN==len(Instru_memory)-1):
                            end_fetching=True
                        mynewinstr = Instru_Fetch(Instru_memory,LUIN) #'myinstr' is an instance of 'Instruction_Manager'
                        mynewinstr.Fetched()
                        print(f'{mynewinstr} {LUIN} {clock_cycles}')
                        Instru_memory[LUIN] = mynewinstr #the instruction's state is modified to 'FETCHED'
                        # Running_instructions.append(mynewinstr)
                        IF_ID = mynewinstr
                        # if(LUIN==1):
                        # if(LUIN==LUIN_stack[-1]+1):
                        #     LFIN = LUIN_stack[-1]
                        # if(LUIN==LUIN_stack[-1]+2):
                        #     LDIN = LUIN_stack[-1]
                        # if(LUIN==LUIN_stack[-1]+3):
                        #     LEIN = LUIN_stack[-1]
                        # if(LUIN==LUIN_stack[-1]+4):
                        #     LMIN = LUIN_stack[-1]
                        # if(LUIN==LUIN_stack[-1]+5):
                        #     LWIN = LUIN_stack[-1] 
                    if((LEIN>=0 and (not end_memaccessing))):
                        if LEIN == len(Instru_memory)-1:
                            end_memaccessing = True
                        # Data_memory = Mem_Access(Instru_memory[LEIN],Data_memory,Reg_memory)
                        memaccessesed_instr = Instru_memory[LEIN]
                        Running_instructions.remove(memaccessesed_instr)
                        # memaccessesed_instr = Running_instructions[-3]
                        # memaccessesed_instr.Mem_Accessed()
                        # Running_instructions[-3]=memaccessesed_instr
                        result = memaccessesed_instr.result
                        if(memaccessesed_instr.instrtype=='J'):
                            print(memaccessesed_instr.targetaddr)
                            print(int(memaccessesed_instr.targetaddr,2))
                            memaccessesed_instr.to_set_LUIN = int(memaccessesed_instr.targetaddr,2) - 1048576 - 1
                        if(memaccessesed_instr.op=='lw'):
                            # Reg_memory[int(memaccessesed_instr.instru[11:16],2)] = Data_memory[result]
                            memaccessesed_instr.loader = Data_memory[result]
                        elif(memaccessesed_instr.op=='sw'):
                            Data_memory[result] = Reg_memory[int(memaccessesed_instr.instru[11:16],2)] 
                        
                        memaccessesed_instr.Mem_Accessed()
                        Running_instructions.append(memaccessesed_instr)
                        Instru_memory[LEIN] = memaccessesed_instr
                        print(f'{memaccessesed_instr} {LEIN} {clock_cycles}')
                        MEM_WB = memaccessesed_instr
                    if((LMIN>=0 and (not end_writingback))):
                        if LMIN == len(Instru_memory)-1:
                            end_writingback = True
                        writtenback_instr = Instru_memory[LMIN] 
                        Running_instructions.remove(writtenback_instr)
                        result = writtenback_instr.result
                        if(writtenback_instr.instrtype=='R'):
                            Reg_memory[int(writtenback_instr.instru[16:21],2)] = result
                        elif(writtenback_instr.instrtype=='I'):
                            if(writtenback_instr.op=='addi'):
                                Reg_memory[int(writtenback_instr.instru[11:16],2)] = result
                            if(writtenback_instr.op=='lw'):
                                Reg_memory[int(writtenback_instr.instru[11:16],2)] = Data_memory[result]
                                # memaccessesed_instr.loader = Data_memory[result]
                        # Reg_memory = Writeback(Instru_memory[LMIN],Reg_memory)
                        # Reg_memory = Writeback(Running_instructions[-4],Reg_memory)
                        # writtenback_instr = Running_instructions[-4]
                        writtenback_instr.Writtenback()
                        # Running_instructions[-4] = writtenback_instr
                        Running_instructions.append(writtenback_instr) 
                        Instru_memory[LMIN] = writtenback_instr
                        print(f'{writtenback_instr} {LMIN} {clock_cycles}')
                        # Removed_instr = writtenback_instr
                        
                    clock_cycles+=1
                    # if(LUIN+1<len(Instru_memory)):
                    #     LUIN+=1
                    # if(LFIN>=0 and LFIN+1<len(Instru_memory)):
                    #     LFIN+=1
                    if(LDIN>=0 and LDIN+1<len(Instru_memory)):
                        LDIN+=1
                    if(LEIN>=0 and LEIN+1<len(Instru_memory)):
                        LEIN+=1
                    if(LMIN>=0 and LMIN+1<len(Instru_memory)):
                        LMIN+=1
                    if(LWIN>=0 and LWIN+1<len(Instru_memory)):
                        LWIN+=1 
                print('cyc3Runninginstr{')
                for instr in Running_instructions:
                    print(instr,instr.op)
                print('}')  
                if(len(Running_instructions)>0):
                    if((LMIN>=0 and (not end_writingback))):
                        #Anyway there is no 'Writeback' for beq instruction
                        Running_instructions.remove(Instru_memory[LMIN])
                        Instru_memory[LMIN].Writtenback()
                        Running_instructions.append(Instru_memory[LMIN])
                        print(f'{Instru_memory[LMIN]} {LMIN} {clock_cycles}') 
                    if(l<len(Instru_memory)):
                        LFIN = l
                        end_decoding = False
                        Running_instructions.append(Instru_memory[l])
                        print(f'LUIN{LUIN} LFIN{LFIN}')
                # Running_instructions.remove(beq_instr)
                # Remove_instrs = []
        
                # for ins in Running_instructions:
                #     if(ins.isWrittenback()):
                #         Remove_instrs.append(ins)
                # # Running_instructions.remove(ins)
        
                # for ins in Remove_instrs:
                #     Running_instructions.remove(ins)  
                LEIN=-1   
                LDIN=-1
                LMIN=-1
                LWIN=-1
                skip = True
            
            
                       
        elif((Instru_memory[LDIN].op == 'beq' and result == 0 and not stall) or (Instru_memory[LDIN].op == 'bne' and result == 0 and not stall)):
            
           Instru_memory[LDIN].to_Branch = False 
    
        else:
            if(not stall):
                Running_instructions.remove(Instru_memory[LDIN])
        
                Instru_memory[LDIN].Executed(result)
                # Running_instructions[-2] = exec_instr
                Running_instructions.append(Instru_memory[LDIN])
                # Instru_memory[LDIN] = exec_instr
                exec_instr = Instru_memory[LDIN]
        
                print(f'{exec_instr} {exec_instr.op} {exec_instr.regs} {exec_instr.result} {LDIN} {clock_cycles}')
        
                EX_MEM = exec_instr
    
    # if(LUIN-3 >= 0 and LUIN-3 < len(Instru_memory) and len(Running_instructions)>3 and Running_instructions[-3].isExecuted()):
    if((LEIN>=0 and (not end_memaccessing)) and (not skip) and (not jump) ):
        if LEIN == len(Instru_memory)-1:
                end_memaccessing = True
        # Data_memory = Mem_Access(Instru_memory[LEIN],Data_memory,Reg_memory)
        memaccessesed_instr = Instru_memory[LEIN]
        Running_instructions.remove(memaccessesed_instr)
        # memaccessesed_instr = Running_instructions[-3]
        # memaccessesed_instr.Mem_Accessed()
        # Running_instructions[-3]=memaccessesed_instr
        result = memaccessesed_instr.result
        if(memaccessesed_instr.instrtype=='J'):
            print(memaccessesed_instr.targetaddr)
            print(int(memaccessesed_instr.targetaddr,2))
            memaccessesed_instr.to_set_LUIN = int(memaccessesed_instr.targetaddr,2) - 1048576 - 1
        if(memaccessesed_instr.op=='lw'):
            # Reg_memory[int(memaccessesed_instr.instru[11:16],2)] = Data_memory[result]
            memaccessesed_instr.loader = Data_memory[result]
        elif(memaccessesed_instr.op=='sw'):
            Data_memory[result] = Reg_memory[int(memaccessesed_instr.instru[11:16],2)] 
        
        memaccessesed_instr.Mem_Accessed()
        Running_instructions.append(memaccessesed_instr)
        Instru_memory[LEIN] = memaccessesed_instr
        print(f'{memaccessesed_instr} {LEIN} {clock_cycles}')
        MEM_WB = memaccessesed_instr
    # if(LUIN-4 >= 0 and LUIN-4 < len(Instru_memory) and len(Running_instructions)>4 and Running_instructions[-4].isMem_Accessed()):
    if((LMIN>=0 and (not end_writingback)) and (not skip) and (not jump)):
        if LMIN == len(Instru_memory)-1:
            end_writingback = True
        writtenback_instr = Instru_memory[LMIN] 
        Running_instructions.remove(writtenback_instr)
        result = writtenback_instr.result
        print(f'res while writeback {result},{writtenback_instr},op{writtenback_instr.op},regs{writtenback_instr.regs}')
        if(writtenback_instr.instrtype=='R'):
            Reg_memory[int(writtenback_instr.instru[16:21],2)] = result
            Reg_memory[int(writtenback_instr.regs[2],2)] = result
            print(f'from regmem- Reg_memory[int(writtenback_instr.regs[1],2)]:{Reg_memory[int(writtenback_instr.regs[1],2)]}')
        elif(writtenback_instr.instrtype=='I'):
            if(writtenback_instr.op=='addi'):
                Reg_memory[int(writtenback_instr.instru[11:16],2)] = result
                Reg_memory[int(writtenback_instr.regs[1],2)] = result
                print(f'from regmem- Reg_memory[int(writtenback_instr.regs[1],2)]:{Reg_memory[int(writtenback_instr.regs[1],2)]}')
            if(writtenback_instr.op=='lw'):
                Reg_memory[int(writtenback_instr.instru[11:16],2)] = writtenback_instr.loader
        writtenback_instr.Writtenback()
        # Running_instructions[-4] = writtenback_instr
        Running_instructions.append(writtenback_instr) 
        Instru_memory[LMIN] = writtenback_instr
        print(f'{writtenback_instr} {LMIN} {clock_cycles}')
                    # Removed_instr = writtenback_instr
        # Removed_instr = writtenback_instr
    
    print("{")
    
    for i in Running_instructions:
        print(f'\t {i}')
    
    print("}")
    
    Remove_instrs = []
    
    for ins in Running_instructions:
        if(ins.isWrittenback()):
            Remove_instrs.append(ins)
            # Running_instructions.remove(ins)
    
    for ins in Remove_instrs:
        Running_instructions.remove(ins)
    
    if(LUIN+1<len(Instru_memory)):
        LUIN+=1
    if(LFIN>=0 and LFIN+1<len(Instru_memory) and (not skip)):
        LFIN+=1
    if(LDIN>=0 and LDIN+1<len(Instru_memory)):
        LDIN+=1
    if(LEIN>=0 and LEIN+1<len(Instru_memory)):
        LEIN+=1
    if(LMIN>=0 and LMIN+1<len(Instru_memory)):
        LMIN+=1
    if(LWIN>=0 and LWIN+1<len(Instru_memory)):
        LWIN+=1
    print(f'LUIN{LUIN} LUINstak[-1]{LUIN_stack[-1]} LFIN{LFIN} LDIN{LDIN} LEIN{LEIN} LMIN{LMIN} LWIN{LWIN}')
    if(LUIN<len(Instru_memory)):
        end_fetching=False
    if(LUIN<len(Instru_memory) and len(Running_instructions)==0):
        end_fetching=True
    # print(Removed_instr) 
    
    # if Removed_instr!='' and Removed_instr!=None:
    # if len(Running_instructions)>4:
    #     Running_instructions.remove(Running_instructions[-4])
    if(jump):
        clock_cycles+=1
        jump = False
    elif(skip):
        skip = False
    else:
        clock_cycles+=1

print(len(Running_instructions),clock_cycles)
for inst in Instru_memory:
    print(inst,inst.result)
print(Reg_memory)
print(Data_memory)
# for p in Reg_memory:
#     print(p)
    # print(f'{p[0]}:{p[1]}')   

    
    

