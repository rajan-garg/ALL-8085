import sys
from gi.repository import Gtk


class Simulator:
    def __init__(self, shell_ui, window):
        self.shell_ui = shell_ui
        self.curr_inst_label = self.shell_ui.get_object("current_instruction")
        self.offset = 0
        if self.shell_ui.get_object("loader_offset_entry").get_text() is not "":
            self.offset = int(self.shell_ui.get_object("loader_offset_entry").get_text())
        self.memstr = self.shell_ui.get_object("memory_registers")
        self.rega = self.shell_ui.get_object("regA")
        self.regb = self.shell_ui.get_object("regB")
        self.regc = self.shell_ui.get_object("regC")
        self.regd = self.shell_ui.get_object("regD")
        self.rege = self.shell_ui.get_object("regE")
        self.regf = self.shell_ui.get_object("regF")
        self.regg = self.shell_ui.get_object("regG")
        self.regh = self.shell_ui.get_object("regH")
        self.regPC = self.shell_ui.get_object("regPC")
        self.regSP = self.shell_ui.get_object("regSP")
        self.window = window
        self.reg = dict()
        self.reg['A'] = 0
        self.reg['B'] = 0
        self.reg['C'] = 0
        self.reg['D'] = 0
        self.reg['E'] = 0
        self.reg['F'] = 0
        self.reg['G'] = 0
        self.reg['H'] = 0
        self.reg['PC'] = 0
        # Special Function
        self.memory = {}
        self.reg['SP'] = 0
        self.PC = 0
        self.stack = []
        self.oplen = {}
        self.dbloc = []
        self.getopcodelen()

    def callbackf(self):
        self.simulator(int(self.reg['PC']))

    def simulator(self, pc=0):
        inst = self.memory[pc]
        opcode = inst.split(' ')[0]
        print('Current Instruction : ' + str(self.memory[pc]))
        self.curr_inst_label.set_text(str(self.memory[pc]))
        print('Register Values')
        print('A : ' + str(self.reg['A']))
        self.rega.set_text(str(self.reg['A']))
        print('B : ' + str(self.reg['B']))
        self.regb.set_text(str(self.reg['B']))
        print('C : ' + str(self.reg['C']))
        self.regc.set_text(str(self.reg['C']))
        print('D : ' + str(self.reg['D']))
        self.regd.set_text(str(self.reg['D']))
        print('E : ' + str(self.reg['E']))
        self.rege.set_text(str(self.reg['E']))
        print('F : ' + str(self.reg['F']))
        self.regf.set_text(str(self.reg['F']))
        print('G : ' + str(self.reg['G']))
        self.regg.set_text(str(self.reg['G']))
        print('H : ' + str(self.reg['H']))
        self.regh.set_text(str(self.reg['H']))
        print('Variable Memory Locations')
        memlocs = ''
        for db in self.dbloc:
            memlocs += (str(db + self.offset) + ' : ' + str(self.memory[db]) + '\n')
        self.memstr.set_text(memlocs)
        print(memlocs)
        # raw_input("Press Enter to continue...")
        if opcode == 'HLT':
            dialog = Gtk.MessageDialog(parent=self.window, flags=0, type=Gtk.MessageType.INFO,
                                       buttons=Gtk.ButtonsType.OK, message_format="Finished Simulation")
            dialog.run()
            print("INFO dialog closed")
            dialog.destroy()
            return
        elif opcode == 'JMP':
            nextinst = int(inst.split(' ')[1])
            self.PC = nextinst
            print(nextinst)
            print(self.PC)
        elif opcode == 'MVI':
            regvar = inst.split(' ')[1].split(',')[0].lstrip().rstrip()
            self.reg[regvar] = int(inst.split(' ')[1].split(',')[1].lstrip().rstrip())
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'ADI':
            self.reg['A'] = int(self.reg['A']) + int(inst.split(' ')[1])
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'STA':
            memloc = int(inst.split(' ')[1])
            self.memory[memloc] = int(self.reg['A'])
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'LDA':
            memloc = int(inst.split(' ')[1])
            self.reg['A'] = int(self.memory[memloc])
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'MOV':
            destreg = inst.split(' ')[1].split(',')[0].lstrip().rstrip()
            srcreg = inst.split(' ')[1].split(',')[1].lstrip().rstrip()
            self.reg[destreg] = self.reg[srcreg]
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'ADD':
            srcreg = inst.split(' ')[1]
            self.reg['A'] = int(self.reg['A']) + int(self.reg[srcreg])
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'SUI':
            self.reg['A'] = int(self.reg['A']) - int(inst.split(' ')[1])
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'SUB':
            srcreg = inst.split(' ')[1]
            self.reg['A'] = int(self.reg['A']) - int(self.reg[srcreg])
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'ANI':
            self.reg['A'] = int(self.reg['A']) & int(inst.split(' ')[1])
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'ANA':
            srcreg = inst.split(' ')[1]
            self.reg['A'] = int(self.reg['A']) & int(self.reg[srcreg])
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'ORI':
            self.reg['A'] = int(self.reg['A']) | int(inst.split(' ')[1])
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'ORA':
            srcreg = inst.split(' ')[1]
            self.reg['A'] = int(self.reg['A']) | int(self.reg[srcreg])
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'PUSH':
            srcreg = inst.split(' ')[1]
            self.stack.append(int(self.reg[srcreg]))
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'POP':
            srcreg = inst.split(' ')[1]
            self.reg[srcreg] = self.stack.pop()
            self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'JNZ':
            nextinst = int(inst.split(' ')[1])
            if int(self.reg['A']) != 0:
                self.PC = nextinst
            else:
                self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'JZ':
            nextinst = int(inst.split(' ')[1])
            if int(self.reg['A']) == 0:
                self.PC = nextinst
            else:
                self.PC = pc + int(self.oplen[opcode])
        elif opcode == 'JP':
            nextinst = int(inst.split(' ')[1])
            if int(self.reg['A']) > 0:
                self.PC = nextinst
            else:
                self.PC = pc + int(self.oplen[opcode])
        self.reg['PC'] = self.PC

    def getopcodelen(self):
        inputfile = open('lenopcodes.cf', "r")
        code = inputfile.read()
        lines = code.split('\n')
        for line in lines:
            line = line.lstrip().rstrip()
            if line != '':
                self.oplen[line.split(' ')[0]] = int(line.split(' ')[1])

    def load(self, filename):
        inputfile = open(filename, "r")
        code = inputfile.read()
        lines = code.split('\n')
        mem = 0
        for line in lines:
            op = line.split(' ')[0].lstrip().rstrip()
            if op != 'DB':
                self.memory[mem] = line
                mem += self.oplen[op]
            else:
                self.memory[mem] = int(line.split(' ')[1].lstrip().rstrip())
                self.dbloc.append(mem)
                mem += 1
