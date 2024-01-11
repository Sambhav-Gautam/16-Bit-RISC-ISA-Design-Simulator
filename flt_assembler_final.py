import sys
# Error Starting
#file1 = open("output.txt", "w")
error=0
def binary_to_decimal(bin_value):
    num=0
    for i in range(len(bin_value)):
        num+=int(bin_value[i])*(2**(len(bin_value)-i-1))
    #print(num)
    return num
def illegal_immidiate_values(j):
    k = j.split(" ")
    k1 = k[2][1:]
    if len(k1) > 127:
        return 0
    else:
        return 1


# Undefied Variables
def undefined_variables(j):
    k = j.split(" ")
    variable_name = k[2]
    if variable_name not in variables:
        return 0
    else:
        return 1


# Undefined Labels
def undefined_labels(j):
    k = j.split(" ")
    label_name = k[1]
    if label_name not in labels_adress:
        return 0
    else:
        return 1


# Error Ending
# Decimal to Binary Function
def decimal_to_binary(decimal_number, bits):
    binary_value = ""
    while True:
        x = decimal_number // 2
        y = decimal_number % 2
        binary_value += str(y)
        decimal_number = x
        if decimal_number == 0:
            break
    x = bits - len(binary_value)
    for i in range(x):
        binary_value += "0"
    binary_value = binary_value[::-1]
    return binary_value


# For rectifying error and obatining value of register
def register(value):
    d1 = {  # Dictonary with opcodes of registers
        "R0": "000",
        "R1": "001",
        "R2": "010",
        "R3": "011",
        "R4": "100",
        "R5": "101",
        "R6": "110",
        "FLAGS": "111",
    }
    if value in d1:
        return d1[value]
    else:
        return 0


# Type A : NUmber -> 1
# Checked
def addition(instruction):
    global error
    opcode = "0000000"
    list_of = instruction.split()
    if len(list_of) == 4:
        if (
            register(list_of[1]) != 0
            and register(list_of[2]) != 0
            and register(list_of[3]) != 0
        ):
            # print(adress_lines[instruction])
            # print(":")
            if(error==0):
                
                print(
                    opcode
                    + register(list_of[1])
                    + register(list_of[2])
                    + register(list_of[3])
                )
                # print("\n")
        else:
            
            error=1
            print(f"Error in line {line_no} Typos Error:Register Name Not valid")
            # print("\n")
            exit()
    else:
        
        error=1
        print(f"Error in line {line_no}  must contain 3 parameters")
        # print("\n")
        

# Type A: Number -> 2
# Checked
def subtraction(instruction):
    global error
    opcode = "0000100"
    list_of = instruction.split()
    if len(list_of) == 4:
        if (
            register(list_of[1]) != 0
            and register(list_of[2]) != 0
            and register(list_of[3]) != 0
        ):
            # print(adress_lines[instruction])
            # print(":")
            if(error==0):
                
                print(
                    opcode
                    + register(list_of[1])
                    + register(list_of[2])
                    + register(list_of[3])
                )
                # print("\n")
        else:
            
            error=1
            print(f"Error in line {line_no} Typos Error:Register Name Not valid")
            # print("\n")
            exit()
    else:
        
        error=1
        print(f"Error in line {line_no}  must contain 3 parameters")
        # print("\n")
        

# Type B:Register and Immediate type
# Number -> 3
# Checked
def move_immidiate(instruction):
    global error
    List1 = instruction.split()
    if(len(List1)!=3):
        error=1
        print(f"Error in line {line_no} instruction must contain 2 parameters")
        # print("\n")
        exit()
        
        
    if register(List1[1]) == 0:
        # 
        # 
        error=1
        print(f"Error in line {line_no} Typos Error")
        # print("\n")
        exit()
    elif(error==0):
        
        Opcode = "000100"  # Opcode with unused bit
        x = decimal_to_binary(int(List1[1][1]), 3)
        Opcode += x
        y = int(List1[2][1:])
        Opcode += decimal_to_binary(y, 7)
        # print(adress_lines[instruction])
        # print(":")
        
        print(Opcode)
        # print("\n")


# Type C: Number -> 4
# checked
def mov_register(instruction):
    global error
    opcode = "0001100000"
    List1 = instruction.split()
    if(len(List1)!=3):
        error=1
        print(f"Error in line {line_no} instruction must contain 2 parameters")
        # print("\n")
        
    if register(List1[1]) != 0 and register(List1[2]) != 0:
        # print(adress_lines[instruction])
        # print(":")
        if(error==0):
            
            print(opcode + register(List1[1]) + register(List1[2]))
            # print("\n")
    else:
        # 
        # 
        error=1
        print(f"Error in line {line_no} Typos Error:Register Name Not Valid")
        # print("\n")
        exit()


# Type D: Number -> 5
# checked
def load(instruction):
    global error
    opcode = "001000"
    lines = instruction.split()
    if(len(lines)!=3):
        error=1
        print(f"Error in line {line_no} instruction must contain 2 parameters")
        # print("\n")
        
        
    if (register(lines[1])) != 0:
        # print(adress_lines[instruction])
        # print(":")
        if(error==0):
            
            print(opcode + register(lines[1]) + variables[lines[2]])
            # print("\n")
    else:
        error=1
        # 
        # 
        print(f"Error in line {line_no} Typos Error : Register Name")
        # print("\n")
        exit()


# Type D: Number -> 6
# Checked
def store(instruction):
    global error
    opcode = "001010"
    lines = instruction.split()
    if(len(lines)!=3):
        error=1
        print(f"Error in line {line_no} instruction must contain 2 parameters")
        # print("\n")
    
    if (register(lines[1])) != 0:
        # print(adress_lines[instruction])
        # print(":")
        if(error==0):
            
            print(opcode + register(lines[1]) + variables[lines[2]])
            # print("\n")
    else:
        error=1
        # 
        # 
        print(f"Error in line {line_no} Typos Error : Register Name")
        # print("\n")
        exit()


# Type A: Number -> 7
# Checked
def mul(instruction):
    global error
    opcode = "0011000"  # opcode for multiply
    list_of = instruction.split()
    if(len(list_of)!=4):
        error=1
        print(f"Error in line {line_no} instruxtion must conatin 3 parameters ")
        # print("\n")
    if (
        register(list_of[1]) != 0
        and register(list_of[2]) != 0
        and register(list_of[3]) != 0
    ):
        # print(adress_lines[instruction])
        # print(":")
        if(error==0):
            
            print(
                opcode + register(list_of[1]) + register(list_of[2]) + register(list_of[3])
            )
            # print("\n")
    else:
        error=1
        # 
        # 
        print(f"Error in line {line_no} Typos Error:Register Name Not valid")
        # print("\n")
        exit()


# Type C: Number -> 8
# checked
def divide(instruction):
    global error
    opcode = "0011100000"
    List1 = instruction.split()
    if(len(List1)!=3):
        error=1
        print(f"Error in line {line_no} instruction must conatin 2 parameters")
        # print("\n")
    if register(List1[1]) != 0 and register(List1[2]) != 0:
        # print(adress_lines[instruction])
        # print(":")
        if(error==0):
            
            print(opcode + register(List1[1]) + register(List1[2]))
            # print("\n")
    else:
        error=1
        # 
        # 
        print(f"Error in line {line_no} Typos Error:Register Name Not Valid")
        # print("\n")
        exit()


# Type B: Number -> 9
# checked
def rightshift(instruction):
    global error
    List1 = instruction.split()
    if(len(List1)!=3):
        error=1
        print(f"Error in line {line_no} instruxtion must conatin 2 parameters")
        # print("\n")
    if register(List1[1]) == 0:
        # 
        #
        error=1
        print(f"Error in line {line_no} Typos Error: Register")
        # print("\n")
        exit()
    elif(error==0):
        
        Opcode = "010000"  # Opcode with unused bit
        x = decimal_to_binary(int(List1[1][1]), 3)
        Opcode += x
        y = int(List1[2][1:])
        Opcode += decimal_to_binary(y, 7)
        # print(adress_lines[instruction])
        # print(":")
        print(Opcode)
        # print("\n")


# Type B: Number -> 10
# checked
def left_shift(instruction):
    global error
    List1 = instruction.split()
    if(len(List1)!=3):
        error=1
        print(f"Error in line {line_no} instruction must conatin 2 parameters")
        # print("\n")
    if register(List1[1]) == 0:
        error=1
        # 
        # 
        print(f"Error in line {line_no} Typos Error:Register")
        # print("\n")
        exit()
    elif(error==0):
        
        Opcode = "010010"  # Opcode with unused bit
        x = decimal_to_binary(int(List1[1][1]), 3)
        Opcode += x
        y = int(List1[2][1:])
        Opcode += decimal_to_binary(y, 7)
        # print(adress_lines[instruction])
        # print(":")
        print(Opcode)
        # print("\n")


# Type A: Number -> 11
# checked
def XOR(instruction):
    opcode = "0101000"
    list_of = instruction.split()
    if (
        register(list_of[1]) != 0
        and register(list_of[2]) != 0
        and register(list_of[3]) != 0
    ):
        # print(adress_lines[instruction])
        # print(":")
        print(
            opcode + register(list_of[1]) + register(list_of[2]) + register(list_of[3])
        )
        # print("\n")
    else:
        # 
        # 
        print(f"Error in line {line_no} Typos Error:Register Name Not valid")
        # print("\n")
        exit()


# Type A: Number-> 12
# checked
def or_operation(instruction):
    opcode = "0101100"
    list_of = instruction.split()
    if (
        register(list_of[1]) != 0
        and register(list_of[2]) != 0
        and register(list_of[3]) != 0
    ):
        # print(adress_lines[instruction])
        # print(":")
        print(
            opcode + register(list_of[1]) + register(list_of[2]) + register(list_of[3])
        )
        # print("\n")
    else:
        # 
        # 
        print(f"Error in line {line_no} Typos Error:Register Name Not valid")
        # print("\n")
        exit()


# Type A: Number-> 13
# checked
def and_operation(instruction):
    opcode = "0110000"
    list_of = instruction.split()
    if (
        register(list_of[1]) != 0
        and register(list_of[2]) != 0
        and register(list_of[3]) != 0
    ):
        # print(adress_lines[instruction])
        # print(":")
        print(
            opcode + register(list_of[1]) + register(list_of[2]) + register(list_of[3])
        )
        # print("\n")
    else:
        # 
        # 
        print(f"Error in line {line_no} Typos Error:Register Name Not valid")
        # print("\n")
        exit()


# Type C: Number -> 14
# checked
def invert(instruction):
    opcode = "0110100000"
    List1 = instruction.split()
    if register(List1[1]) != 0 and register(List1[2]) != 0:
        # print(adress_lines[instruction])
        # print(":")
        print(opcode + register(List1[1]) + register(List1[2]))
        # print("\n")
    else:
        # 
        # 
        print(f"Error in line {line_no} Typos Error:Register Name Not Valid")
        # print("\n")
        exit()


# Type C: Number ->15
# Checked
def cmp(instruction):
    opcode = "0111000000"
    List1 = instruction.split()
    if register(List1[1]) != 0 and register(List1[2]) != 0:
        # print(adress_lines[instruction])
        # print(":")
        print(opcode + register(List1[1]) + register(List1[2]))
        # print("\n")
    else:
        # 
        # 
        print(f"Error in line {line_no} Typos Error:Register Name Not Valid")
        # print("\n")
        exit()


# Type E: Number -> 16
# Checked
def unconditional_jump(instruction):
    opcode = "011110000"
    lst1 = instruction.split(" ")
    mem_addr = lst1[1]
    if mem_addr not in variables:
        opcode += labels_adress[mem_addr]
        # print(adress_lines[instruction])
        # print(":")
        print(opcode)
        # print("\n")
    else:
        # 
        # 
        print(f"Error in line {line_no} :Use of variable instead of label")
        # print("\n")
        exit()


# Type E: Number -> 17
# Checked
def jump_if_less_than(instruction):
    lst1 = instruction.split(" ")
    opcode = "111000000"
    mem_addr = lst1[1]
    if mem_addr not in variables:
        opcode += labels_adress[mem_addr]
        # print(adress_lines[instruction])
        # print(":")
        print(opcode)
        # print("\n")
    else:
        # 
        # 
        print(f"Error in line {line_no} :Use of variable instead of label")
        # print("\n")
        exit()


# Type E: Number -> 18
# Checked
def jump_if_greater_than(instruction):
    lst1 = instruction.split(" ")
    opcode = "111010000"
    mem_addr = lst1[1]
    if mem_addr not in variables:
        opcode += labels_adress[mem_addr]
        # print(adress_lines[instruction])
        # print(":")
        print(opcode)
        # print("\n")
    else:
        # 
        # 
        print(f"Error in line {line_no} :Use of variable instead of label")
        # print("\n")
        exit()


# Type E: Number -> 19
# Checked
def jump_if_equal_than(instruction):
    lst1 = instruction.split(" ")
    opcode = "111110000"
    mem_addr = lst1[1]
    if mem_addr not in variables:
        opcode += labels_adress[mem_addr]
        # print(adress_lines[instruction])
        # print(":")
        print(opcode)
        # print("\n")
    else:
        # 
        # 
        
        print(f"Error in line {line_no} :Use of variable instead of label")
        # print("\n")
        exit()


# Type F: Number -> 20
def hault(instruction):
    # hault = instruction.split(" ")
    first_half = "11010"
    better_half = "00000000000"
    final_ans = first_half + better_half
    # x = instruction.split(":")
    # print(adress_lines[x[0]])
    # print(":")
    print(final_ans)
def floating_pt(x):
    b=x[0:3]
    a=x[3:]
    if(b!="000" and b !="111"):
        num=1
        for i in range(-1,-6,-1):
            num=num+int(a[-i-1])*(2**(i))
        num=num*(2**(binary_to_decimal(b)-3))
        return num
    elif(b=="000"):
        num=0
        for i in range(-1,-6,-1):
            num=num+int(a[-i-1])*(2**(i))
        num=num*(2**(-2))
        return num

def reverse_floating_pt(x):
    empdict={}
    for i in range(0,256):
        i1=decimal_to_binary(i,8)
        if(i1.startswith("111")):
            continue
        else:
        
            k=floating_pt(i1)
            empdict[i1]=k
    for i,j in empdict.items():
        if(j-x==float(0)):
            return i
    
    
    
    
    
# Type - A
def F_Addition(instruction):
    opcode="1000000"
    l1=["R0","R1","R2","R3","R4","R5","R6","R7"]
    l2=[0,1,2,3,4,5,6,7]
    list_of = instruction.split()
    x=l1.index(list_of[1])
    y=l1.index(list_of[2])
    z=l1.index(list_of[3])
    reg1=decimal_to_binary(l2[x],3)
    reg2=decimal_to_binary(l2[y],3)
    reg3=decimal_to_binary(l2[z],3)
    final=opcode+reg1+reg2+reg3
    print(final)

# Type - A

def F_Subtraction(instruction):
    opcode="1000100"
    l1=["R0","R1","R2","R3","R4","R5","R6","R7"]
    l2=[0,1,2,3,4,5,6,7]
    list_of = instruction.split()
    x=l1.index(list_of[1])
    y=l1.index(list_of[2])
    z=l1.index(list_of[3])
    reg1=decimal_to_binary(l2[x],3)
    reg2=decimal_to_binary(l2[y],3)
    reg3=decimal_to_binary(l2[z],3)
    final=opcode+reg1+reg2+reg3
    print(final)

# Type - B

def MoveF_Immidiate(instruction):
    opcode="10010"
    l1=["R0","R1","R2","R3","R4","R5","R6","R7"]
    l2=[0,1,2,3,4,5,6,7]
    list_of = instruction.split()
    opcode+= decimal_to_binary(l2[l1.index(list_of[1])],3)
    x=float(list_of[2][1:])
    opcode+=reverse_floating_pt(x)
    # x1=str(x)
    # y2=x1.split(".")
    # #print(y2)
    # bin_value=decimal_to_binary(int(y2[0]),4)+"."+decimal_to_bin_fractional(float("0."+y2[1]))
    # opcode+=bin_value
    print(opcode)
    
fobj1=open("sim_test.txt","r")
# Main Function
content_of_file = [i.strip() for i in fobj1.readlines()]
# lists for their purpose
count = 0
labels = []  # To store labels line
labels_adress = {}  # Labels Names with adress
instructions = []  # Lines that contain instructions
variables = {}  # Lines that contains variable declaration
empty_lines = []  # Lines that are empty
adress_lines = {}  # Adress of every level

for line in content_of_file:
    # For empty lines
    if not line:
        empty_lines.append(line)
        continue
    # Label ends with :
    elif ":" in line:
        labels.append(line)
        adress_value = decimal_to_binary(count, 7)
        adress_lines[line.split(":")[0]] = adress_value
        labels_adress[line.split(":")[0]] = adress_value
        count += 1
    # if it is variable definition
    elif line.startswith("var"):
        list_of_variables = line.split()
        variables[list_of_variables[1]] = 1
    # instructions
    else:
        instructions.append(line)
        adress_value = decimal_to_binary(count, 7)
        adress_lines[line] = adress_value
        count += 1

for i in variables:
    variables[i] = decimal_to_binary(count, 7)
    count += 1
anyvar = content_of_file[-1]
lenght=len(content_of_file)
#if "hlt" not in content_of_file:
    #print(f"Error hlt is not present ")
    #print("\n")
if anyvar.endswith("hlt") == False:
    print(f"Error: hlt is not the ending statment")
    # print("\n")
    exit()
flag = 0
line_no = 0
for j in content_of_file:
   
    if ":" in j:
        flag = 1
        j = j.split(":")[1].strip()
    if j[0:3] == "var":
        list1 = j.split()
        line_no += 1
        if len(list1) != 2 or j == "":
            
            print(f"Error in line {line_no} Syntax Error")
            # print("\n")
            exit()
        if flag == 1:
            
            print(
                f"Error in line {line_no} Variables should be declared in the beginning"
            )
            # print("\n")
            exit()

    elif j == "":
        continue
    elif j[0:4] == "addf":
        line_no += 1
        flag = 1
        F_Addition(j)
    elif j[0:4] == "subf":
        line_no += 1
        flag = 1
        F_Subtraction(j)
    elif j[0:4] == "movf":
        line_no += 1
        flag = 1
        MoveF_Immidiate(j)    
        
    elif j[0:3] == "add" :
        line_no += 1
        flag = 1
        addition(j)
    elif j[0:3] == "sub"  :
        line_no += 1
        flag = 1
        subtraction(j)
    elif j[0:3] == "mul" :
        line_no += 1
        flag = 1
        mul(j)
    elif j[0:3] == "xor" :
        line_no += 1
        flag = 1
        XOR(j)
    elif j[0:2] == "or" :
        line_no += 1
        flag = 1
        or_operation(j)
    elif j[0:3] == "and" :
        line_no += 1
        flag = 1
        and_operation(j)
    elif j[0:3] == "mov" and "$" in j:
        line_no += 1
        flag = 1
        if illegal_immidiate_values(j) == 1 :
            move_immidiate(j)
        else:
            
            print(f"Error in line {line_no} illegal immidiate values error")
            # print("\n")
    elif j[0:2] == "rs" :
        line_no += 1
        k = j.split(" ")
        flag = 1
        if k[2][0] != "$":
            
            print(f"Error in line {line_no} typos error")
            # print("\n")
            exit()
        if illegal_immidiate_values(j) == 1 :
            rightshift(j)
        else:
            
            print(f"Error in line {line_no} illegal immidiate values error")
            # print("\n")
    elif j[0:2] == "ls":
        line_no += 1
        k = j.split(" ")
        flag = 1
        if k[2][0] != "$":
            
            print(f"Error in line {line_no} typos error")
            # print("\n")
            exit()
        if illegal_immidiate_values(j) == 1 :
            left_shift(j)
        else:
            
            print(f"Error in line {line_no} illegal immidiate values error")
            # print("\n")
    elif j[0:3] == "mov" :
        line_no += 1
        k = j.split(" ")
        flag = 1

        mov_register(j)
    elif j[0:3] == "div" :
        line_no += 1
        flag = 1
        divide(j)
    elif j[0:3] == "not" :
        line_no += 1
        flag = 1
        invert(j)
    elif j[0:3] == "cmp" :
        line_no += 1
        flag = 1
        cmp(j)
    elif j[0:2] == "ld":
        line_no += 1
        flag = 1
        if undefined_variables(j) == 1 :
            load(j)
        else:
            
            print(f"Error in line {line_no} undefined variable error")
            # print("\n")
            # break
    elif j[0:2] == "st":
        line_no += 1
        flag = 1
        if undefined_variables(j) == 1 :
            store(j)
        else:
            
            print(f"Error in line {line_no} undefined variable error")
            # print("\n")
            # break
    elif j[0:3] == "jmp":
        line_no += 1
        flag = 1
        if undefined_labels(j) == 1 :
            unconditional_jump(j)
        else:
            
            print(f"Error in line {line_no} undefined label error")
            # print("\n")
            # break
    elif j[0:3] == "jlt":
        line_no += 1
        flag = 1
        if undefined_labels(j) == 1 :
            jump_if_less_than(j)
        else:
            
            print(f"Error in line {line_no} undefined label error")
            # print("\n")
            # break
    elif j[0:3] == "jgt":
        line_no += 1
        flag = 1
        if undefined_labels(j) == 1 :
            jump_if_greater_than(j)
        else:
            
            print(f"Error in line {line_no} undefined label error")
            # print("\n")
            # break
    elif j[0:2] == "je":
        line_no += 1
        flag = 1
        if undefined_labels(j) == 1 :
            jump_if_equal_than(j)
        else:
            
            print(f"Error in line {line_no} undefined label error")
            # print("\n")
            # break
    elif j[0:3] == "hlt":
        line_no += 1
        flag = 1
        hault(j)
        exit()

    else:
        
        line_no += 1
        print(f"Error in line {line_no} General Syntax Error")
        # print("\n")

