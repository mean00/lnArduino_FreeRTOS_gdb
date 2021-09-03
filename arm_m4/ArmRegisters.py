#
# R0..R3
# R4..R11,LR
# S16..S31 if R14 & 0x10
#
import gdb
import pprint
from Types import StdTypes 
from List import ListInspector 


def printAdr(title,adr):
    print("%s : adr=0x%x" %(title,adr))
#
# Helper class to deal with registers
#    
class aRegisters:
  def  __init__(self):
    self.reg= [0] * 32
    self.fpu= [0] * 32
    self.psr = 0 
    #print("**Create **")
  def read32bits(self,adr):
    #print("**Read32 ** :%x" % adr)
    uint_pointer_type = gdb.lookup_type('uint32_t').pointer()
    gaddress = gdb.Value(adr)
    paddress = gaddress.cast(uint_pointer_type)
    try:
        c=int(paddress.dereference())
    #    print("=> %x" % c)
    except:
        print("** Error ** adr 0x%x" % (adr))
        c=0
    return c 
#
#
  def write32bits(self,adr,value):
    adr=int(adr)
    value=int(value)
    #print(adr)
    #print(value)
    st="set {int}"+hex(adr)+" = " +hex(value)
    #print(st)
    gdb.execute(st) 


  #
  # Dump registers to given address
  # You have to move the stack yourself !
  #
  def saveRegisterToMemory(self,adr):
    for i in range(0,8): # R4..R11 => 8 registers
        self.write32bits(adr+i*4,self.reg[(i+4)])
    # next are r0 .. r3
    adr+=8*4
    for i in range(0,4): # R4..R11 => 8 registers
        self.write32bits(adr+i*4,self.reg[i])
    adr+=4*4
    # Then r12, lr pc psr
    self.write32bits(adr,self.reg[12])
    self.write32bits(adr+1*4,self.reg[14])
    self.write32bits(adr+2*4,self.reg[15])
    self.write32bits(adr+3*4,self.psr)

  # load all the registers from the psp TCB pointer 
  def loadRegistersFromMemory(self,adr):
    printAdr("Initial Stack",adr)
    # First is the manually saved registers R4..R11 + LR
    for i in range(0,8):
       r=self.read32bits(adr+i)
       self.reg[4+i]=r
    self.reg[14]=self.read32bits(adr+8)
    adr+=9
    # Then *** OPTIONNALY** we have fpu 16...31
    fpu=False
    printAdr("R14 ",self.reg[14])
    if(not (self.reg[14] & 0x10)): # Read FP regs too
        print("** FPU **")
        fpu=True
        for i in range(0,16):
           r=self.read32bits(adr+i)
           self.fpu[16+i]=r
        adr+=16
    # Then base frame R0, R1, R2, R3,R12, LC , PC , 
    self.reg[0]=self.read32bits(adr+0)
    self.reg[1]=self.read32bits(adr+1)
    self.reg[2]=self.read32bits(adr+2)
    self.reg[3]=self.read32bits(adr+3)
    self.reg[12]=self.read32bits(adr+4)
    self.reg[14]=self.read32bits(adr+5)
    self.reg[15]=self.read32bits(adr+6)
    self.psr=self.read32bits(adr+7) # PSR
    adr+=8
    if(fpu is True): # low fpureg
        adr+=18  # 16 fp + fpspr + reserved
    print("15")
    self.reg[13]=int(adr)
    printAdr("final stack ",adr)
    printAdr("PC ",self.reg[15])
    printAdr("LR ",self.reg[14])
    #for i in range(0,16):
    #    print("%d : 0x%x" % (i,self.reg[i]))
  #
  def setRegister(self,reg, value):
    #print(reg)
    #print(value)
    st="set $"+str(reg)+"="+hex(value)
    #print(st)
    gdb.execute(st) 

  # set the CPU register with the value stored in the object
  def setCPURegisters(self):
    print("SET CPU")
    printAdr("PC ",self.reg[15])
    printAdr("LR ",self.reg[14])
    for i in range(0,16): 
      r="r"+str(i)
      self.setRegister(r,self.reg[i])
  # read the CPU register and update our internal copy with them
  def getCPURegisters(self):
    for i in range(0,16):
      r="r"+str(i)
      self.reg[i]=int(gdb.selected_frame().read_register(r) )
      self.reg[i]=self.reg[i] & 0xffffffff # unsigned hack
    self.psr=int(gdb.selected_frame().read_register("xpsr"))
    #print("Read registers")
    #for i in range(0,16):
        #print("%d: 0x%x" % (i,self.reg[i]))

