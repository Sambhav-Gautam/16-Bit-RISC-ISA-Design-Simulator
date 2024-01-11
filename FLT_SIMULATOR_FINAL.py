import sys
def increment():
    global pc
    pc= pc+1


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


def binary_to_decimal(bin_value):
    num=0
    for i in range(len(bin_value)):
        num+=int(bin_value[i])*(2**(len(bin_value)-i-1))
    #print(num)
    return num

# 1
# type a
# opcode="00000"
def Addition(instruction):
    if(((registers[binary_to_decimal(instruction[10:13])] + registers[binary_to_decimal(instruction[13:])]))<(2**16)):
        registers[binary_to_decimal(instruction[7:10])] = ( registers[binary_to_decimal(instruction[10:13])] + registers[binary_to_decimal(instruction[13:])] )
        registers[7]=0
    else:
        registers[binary_to_decimal(instruction[7:10])] =(registers[binary_to_decimal(instruction[10:13])] + registers[binary_to_decimal(instruction[13:])])%(2**16)
        registers[7] =8
    increment()

# 2
# type a
# opcode="00001"
    
def Subtraction(instruction):
    if(((registers[binary_to_decimal(instruction[10:13])] - registers[binary_to_decimal(instruction[13:])]))>=0):
        
        registers[binary_to_decimal(instruction[7:10])] =((registers[binary_to_decimal(instruction[10:13])] - registers[binary_to_decimal(instruction[13:])]))
        registers[7]=0
    else:
        registers[binary_to_decimal(instruction[7:10])] =0
        registers[7]=8
    increment()
    

# 3
# type b
# opcode="00010"
def move_immediate(instruction):
    # #change
    #registers[7]=0
    registers[binary_to_decimal(instruction[6:9])] = binary_to_decimal(instruction[9:])
    increment()
    #change
    registers[7]=0
# 4
# type c
# opcode="00011"
def move_register(instruction):
    # #change
    # registers[7]=0
    registers[binary_to_decimal(instruction[10:13])]=registers[binary_to_decimal(instruction[13:])]
    increment()
    #change
    registers[7]=0

# 5
# type d
# opcode="00100"



def load(instruction):
    # #change
    # registers[7]=0
    registers[binary_to_decimal(instruction[6:9])]=binary_to_decimal(mem[binary_to_decimal(instruction[9:])])
    increment()
    
# 6
# type d
# opcode="00101"

def store(instruction):
    # #change
    # registers[7]=0
    mem[binary_to_decimal(instruction[9:])]=decimal_to_binary(registers[binary_to_decimal(instruction[6:9])],16)
    increment()

# 7
# type a
# opcode="00110"

def multiply(instruction):
    if(((registers[binary_to_decimal(instruction[10:13])] * registers[binary_to_decimal(instruction[13:])]))<(2**16)):
        registers[binary_to_decimal(instruction[7:10])] = ( registers[binary_to_decimal(instruction[10:13])] * registers[binary_to_decimal(instruction[13:])] )
        registers[7]=0
    else:
        registers[binary_to_decimal(instruction[7:10])] =(registers[binary_to_decimal(instruction[10:13])] * registers[binary_to_decimal(instruction[13:])])%(2**16)
        registers[7] =8
    increment()

# 8
# type c
# opcode="00111"

def division(instruction):
    if(registers[binary_to_decimal(instruction[13:])]==0):
        registers[0]=0
        registers[1]=0
        registers[7]=8
    else:
        registers[0]=registers[(binary_to_decimal(instruction[10:13]))]//registers[(binary_to_decimal(instruction[13:]))]
        registers[1]=registers[(binary_to_decimal(instruction[10:13]))]%registers[(binary_to_decimal(instruction[13:]))]
        registers[7]=0
    increment()

# 9
# type d
# opcode="01000"
def right_shift(instruction):
    # #change
    # registers[7]=0
    ans1=binary_to_decimal(instruction[9:])
    ans2=binary_to_decimal(instruction[6:9])
    registers[ans2]=(registers[ans2]) >> (ans1)
    
    increment()

# 10
# type d
# opcode="01001"
def left_shift(instruction):
    # #change
    # registers[7]=0
    ans1=binary_to_decimal(instruction[9:])
    ans2=binary_to_decimal(instruction[6:9])
    registers[ans2]=(registers[ans2]) << (ans1)

    increment()
    
# 11
# type a
# opcode="01010"
def xor(instruction):
    # #change
    # registers[7]=0
    registers[binary_to_decimal(instruction[7:10])] =(registers[binary_to_decimal(instruction[10:13])] ^ registers[binary_to_decimal(instruction[13:])])
    
    increment()

# 12
# type a
# opcode="01011"
def Or(instruction):
    # #change
    # registers[7]=0
    registers[binary_to_decimal(instruction[7:10])] =(registers[binary_to_decimal(instruction[10:13])] | registers[binary_to_decimal(instruction[13:])])
    
    increment()


# 13
# type a
# opcode="01100"
def And(instruction):
    # #change
    # registers[7]=0
    registers[binary_to_decimal(instruction[7:10])] =((registers[binary_to_decimal(instruction[10:13])]&registers[binary_to_decimal(instruction[13:])]))
    increment()


# 14
# type c
# opcode="01101"    
def Invert(instruction):
    # #change
    # registers[7]=0
    registers[binary_to_decimal(instruction[10:13])]= 65535-registers[binary_to_decimal(instruction[13:])]
    increment()

# 15
# type c
# opcode="01110" 
def compare(instruction):
    if registers[binary_to_decimal(instruction[10:13])]==registers[binary_to_decimal(instruction[13:])]:
        registers[7]=1
    elif  registers[binary_to_decimal(instruction[10:13])]<registers[binary_to_decimal(instruction[13:])]:
        registers[7] =4
    elif  registers[binary_to_decimal(instruction[10:13])]>registers[binary_to_decimal(instruction[13:])]:
        registers[7] =2
        
    increment()
    
    
# 16
# type e
# opcode="01111" 
def uncoditional_jump(instruction):
    # #change
    # registers[7]=0
    global pc
    pc= binary_to_decimal(instruction[9:])

# 17
# type e
# opcode="10000"     
def jump_if_lt(instruction):
    global pc
    if(registers[7]==4):
        pc= binary_to_decimal(instruction[9:])
    else:
        increment()
    registers[7]=0
# 18
# type e
# opcode="10001" 
def jump_if_gt(instruction):
    global pc
    if(registers[7]==2):
        pc= binary_to_decimal(instruction[9:])
    else:
        increment()
    registers[7]=0
        

# 19
# type e
# opcode="10010"         
def jump_if_eq(instruction):
    global pc
    if(registers[7]==1):
        pc= binary_to_decimal(instruction[9:])
    else:
        increment()
    registers[7]=0

# 20
# type e
# opcode="10011" 
def Halt(instruction):
    global ishalted
    ishalted =True
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
    
    
def F_Addition(instruction):
    x=floating_pt(decimal_to_binary(registers[binary_to_decimal(instruction[10:13])],8))
    y=floating_pt(decimal_to_binary(registers[binary_to_decimal(instruction[13:])],8))
    z=x+y
    if(z<15.75):
        registers[binary_to_decimal(instruction[7:10])]=z
    else:
        registers[7]=8
        registers[binary_to_decimal(instruction[7:10])]=0
    
    increment()

def F_Subtraction(instruction):
    x=floating_pt(decimal_to_binary(registers[binary_to_decimal(instruction[10:13])],8))
    y=floating_pt(decimal_to_binary(registers[binary_to_decimal(instruction[13:])],8))
    z=x-y
    if(z>0):
        registers[binary_to_decimal(instruction[7:10])]=z
    else:
        registers[7]=8
        registers[binary_to_decimal(instruction[7:10])]=0
    increment()
def movf_IMM(instruction):
    x=floating_pt(instruction[8:])
    registers[binary_to_decimal(instruction[5:8])]=x
    increment()
    
fobj=open("sim_test.txt","r")
pc=0
ishalted=False
content_of_file = [i.strip() for i in fobj.readlines()]
mem=["0000000000000000"]*128
registers=[0,0,0,0,0,0,0,0]
j =0
for i in content_of_file:
    mem[j] =i
    j+=1
print(registers)
#print(mem[14])
dict_instruction={"00000":Addition,"00001":Subtraction,
                "00010":move_immediate,"00011":move_register,
                "00100":load,"00101":store,"00110":multiply,
                "00111":division,"01000":right_shift,"01001":left_shift,
                "01010":xor,"01011":Or,"01100":And,"01101":Invert,
                "01110":compare,"01111":uncoditional_jump,
                "11100":jump_if_lt,"11101":jump_if_gt,"11111":jump_if_eq,
                "11010":Halt,"10000":F_Addition,"10010":movf_IMM}
fobj2=open("output file.txt","w")

while(ishalted==False):
    xstr=""
    now = mem[pc]
    #print(pc,end="\n")
    print(decimal_to_binary(pc,7),end="        ")
    xstr+=decimal_to_binary(pc,7)
    xstr+="        "
    dict_instruction[now[0:5]](now) #Execution
    
    for i in registers:
        k="00000000"
        print(k+reverse_floating_pt(i),end=" ")
        xstr+=(k+reverse_floating_pt(i))
        xstr+=" "

    fobj2.write(xstr)
    fobj2.write("\n")
    


for i in range(len(mem)-1):
    print(mem[i],end="\n")
    fobj2.write(str(mem[i]))
    fobj2.write("\n")
print(mem[i],end="")
fobj2.write(mem[i])    
  
    
    
    
    



    
    
    
    
