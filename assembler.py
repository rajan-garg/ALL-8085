import re
from gi.repository import Gtk


class Assembler:
    def __init__(self, shell_ui):
        self.shell_ui = shell_ui
        self.oplen = {}
        self.symTable = {}
        self.globTable = {}
        self.filelen = {}

    def calculate_len(self):
        inputfile = open('lenopcodes.cf', "r")
        code = inputfile.read()
        lines = code.split('\n')
        for line in lines:
            line = line.lstrip().rstrip()
            if line != '':
                self.oplen[line.split(' ')[0]] = int(line.split(' ')[1])

    def try_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def test(self, filenames):
        self.calculate_len()
        glo = re.compile(r'glob var (.*)=(.*)')
        ext = re.compile(r'extern(.*)')
        var = re.compile(r'var (.*)=(.*)')
        add = re.compile(r'(.+)=(.+)\+(.+)')
        sub = re.compile(r'(.+)=(.+)\-(.+)')
        ana = re.compile(r'(.+)=(.+)&(.+)')
        ora = re.compile(r'(.+)=(.+)\|(.+)')
        slop = re.compile(r'loop(.+)')
        elop = re.compile(r'endloop(.*)')
        ifgt = re.compile(r'if (.*)>(.*)')
        ifgte = re.compile(r'endif(.*)')
        ifeq = re.compile(r'if (.*)=(.*)')

        for filename in filenames:
            print("Pass1 in " + filename + " :")
            filename = filename.split('.')[0]
            inputfile = open(filename + ".x", "r")
            code = inputfile.read()
            memaddr = 0
            lines = code.split('\n')
            self.symTable[filename] = {}
            self.globTable[filename] = {}
            loopctr = 0
            ifctr = 0
            ifjmp = {}
            for line in lines:
                line = line.lstrip().rstrip()
                if var.match(line):
                    self.symTable[filename][var.match(line).group(1).lstrip().rstrip()] = '#' + str(memaddr + 3)
                    memaddr += 4
                elif glo.match(line):
                    self.symTable[filename][glo.match(line).group(1).lstrip().rstrip()] = '#' + str(memaddr + 3)
                    self.globTable[filename][glo.match(line).group(1).lstrip().rstrip()] = '#' + str(memaddr + 3)
                    memaddr += 4
                elif ext.match(line):
                    self.symTable[filename][ext.match(line).group(1).lstrip().rstrip()] = '$' + str(
                        ext.match(line).group(1).lstrip().rstrip())
                elif add.match(line):
                    x = add.match(line).group(1).lstrip().rstrip()
                    y = add.match(line).group(2).lstrip().rstrip()
                    z = add.match(line).group(3).lstrip().rstrip()
                    if self.try_int(y) and self.try_int(z):
                        memaddr += self.oplen['MVI']
                        memaddr += self.oplen['ADI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(y) and not self.try_int(z):
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ADI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(z) and not self.try_int(y):
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ADI']
                        memaddr += self.oplen['STA']
                    elif not self.try_int(y) and not self.try_int(z):
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['MOV']
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ADD']
                        memaddr += self.oplen['STA']
                elif sub.match(line):
                    if self.try_int(y) and self.try_int(z):
                        memaddr += self.oplen['MVI']
                        memaddr += self.oplen['SUI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(y) and not self.try_int(z):
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['SUI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(z) and not self.try_int(y):
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['SUI']
                        memaddr += self.oplen['STA']
                    elif not self.try_int(y) and not self.try_int(z):
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['MOV']
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['SUB']
                        memaddr += self.oplen['STA']
                elif ana.match(line):
                    x = ana.match(line).group(1).lstrip().rstrip()
                    y = ana.match(line).group(2).lstrip().rstrip()
                    z = ana.match(line).group(3).lstrip().rstrip()
                    if self.try_int(y) and self.try_int(z):
                        memaddr += self.oplen['MVI']
                        memaddr += self.oplen['ANI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(y) and not self.try_int(z):
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ANI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(z) and not self.try_int(y):
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ANI']
                        memaddr += self.oplen['STA']
                    elif not self.try_int(y) and not self.try_int(z):
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['MOV']
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ANA']
                        memaddr += self.oplen['STA']
                elif ora.match(line):
                    x = ora.match(line).group(1).lstrip().rstrip()
                    y = ora.match(line).group(2).lstrip().rstrip()
                    z = ora.match(line).group(3).lstrip().rstrip()
                    if self.try_int(y) and self.try_int(z):
                        memaddr += self.oplen['MVI']
                        memaddr += self.oplen['ORI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(y) and not self.try_int(z):
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ORI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(z) and not self.try_int(y):
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ORI']
                        memaddr += self.oplen['STA']
                    elif not self.try_int(y) and not self.try_int(z):
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['MOV']
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ORA']
                        memaddr += self.oplen['STA']
                elif slop.match(line):
                    x = slop.match(line).group(1).lstrip().rstrip()
                    if self.try_int(x):
                        memaddr += self.oplen['PUSH']
                        memaddr += self.oplen['MVI']
                        self.symTable[filename][loopctr] = '#' + str(memaddr)
                        loopctr += 1
                elif elop.match(line):
                    loopctr -= 1
                    memaddr += self.oplen['MOV']
                    memaddr += self.oplen['SUI']
                    memaddr += self.oplen['MOV']
                    memaddr += self.oplen['JNZ']
                    memaddr += self.oplen['POP']
                elif ifgt.match(line):
                    x = ifgt.match(line).group(1).lstrip().rstrip()
                    y = ifgt.match(line).group(2).lstrip().rstrip()
                    ifctr += 1
                    memaddr += self.oplen['LDA']
                    memaddr += self.oplen['MOV']
                    memaddr += self.oplen['LDA']
                    memaddr += self.oplen['SUB']
                    memaddr += self.oplen['JP']
                    memaddr += self.oplen['JZ']
                elif ifeq.match(line):
                    x = ifeq.match(line).group(1).lstrip().rstrip()
                    y = ifeq.match(line).group(2).lstrip().rstrip()
                    ifctr += 1
                    memaddr += self.oplen['LDA']
                    memaddr += self.oplen['MOV']
                    memaddr += self.oplen['LDA']
                    memaddr += self.oplen['SUB']
                    memaddr += self.oplen['JNZ']
                elif ifgte.match(line):
                    ifjmp[ifctr - 1] = memaddr

            print("SymTable in Pass1 of file " + filename + " : ")
            print(self.symTable)
        pass_one_box = self.shell_ui.get_object("pass_one_box")
        tv = Gtk.TextView()
        tb = tv.get_buffer()
        tb.set_text(str(self.symTable))
        pass_one_box.add(tv)
        pass_one_box.show_all()

        for filename in filenames:
            filename = filename.split('.')[0]
            inputfile = open(filename + ".x", "r")
            outfile = open(filename + '.l', 'w+')
            code = inputfile.read()
            lines = code.split('\n')
            loopctr = 0
            newcode = []
            memaddr = 0
            ifctr = 0
            ifjmp = {}
            for line in lines:
                line = line.lstrip().rstrip()
                if var.match(line):
                    address = self.symTable[filename][var.match(line).group(1).lstrip().rstrip()].split('#')[1]
                    newcode.append('JMP #' + str(int(address) + 1))
                    newcode.append('DB ' + var.match(line).group(2).lstrip().rstrip())
                    memaddr += 4
                elif glo.match(line):
                    address = self.symTable[filename][glo.match(line).group(1).lstrip().rstrip()].split('#')[1]
                    newcode.append('JMP #' + str(int(address) + 1))
                    newcode.append('DB ' + glo.match(line).group(2).lstrip().rstrip())
                    memaddr += 4
                elif add.match(line):
                    x = add.match(line).group(1).lstrip().rstrip()
                    y = add.match(line).group(2).lstrip().rstrip()
                    z = add.match(line).group(3).lstrip().rstrip()
                    if self.try_int(y) and self.try_int(z):
                        newcode.append('MVI A,' + y)
                        newcode.append('ADI ' + z)
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['MVI']
                        memaddr += self.oplen['ADI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(y) and not self.try_int(z):
                        newcode.append('LDA ' + str(self.symTable[filename][z]))
                        newcode.append('ADI ' + y)
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ADI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(z) and not self.try_int(y):
                        newcode.append('LDA ' + str(self.symTable[filename][y]))
                        newcode.append('ADI ' + z)
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ADI']
                        memaddr += self.oplen['STA']
                    elif not self.try_int(y) and not self.try_int(z):
                        newcode.append('LDA ' + str(self.symTable[filename][y]))
                        newcode.append('MOV B,A')
                        newcode.append('LDA ' + str(self.symTable[filename][z]))
                        newcode.append('ADD B')
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['MOV']
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ADD']
                        memaddr += self.oplen['STA']
                elif sub.match(line):
                    x = sub.match(line).group(1).lstrip().rstrip()
                    y = sub.match(line).group(2).lstrip().rstrip()
                    z = sub.match(line).group(3).lstrip().rstrip()
                    if self.try_int(y) and self.try_int(z):
                        newcode.append('MVI A,' + y)
                        newcode.append('SUI ' + z)
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['MVI']
                        memaddr += self.oplen['SUI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(y) and not self.try_int(z):
                        newcode.append('LDA ' + str(self.symTable[filename][z]))
                        newcode.append('SUI ' + y)
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['SUI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(z) and not self.try_int(y):
                        newcode.append('LDA ' + str(self.symTable[filename][y]))
                        newcode.append('SUI ' + z)
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['SUI']
                        memaddr += self.oplen['STA']
                    elif not self.try_int(y) and not self.try_int(z):
                        newcode.append('LDA ' + str(self.symTable[filename][y]))
                        newcode.append('MOV B,A')
                        newcode.append('LDA ' + str(self.symTable[filename][z]))
                        newcode.append('SUB B')
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['MOV']
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['SUB']
                        memaddr += self.oplen['STA']
                elif ana.match(line):
                    x = ana.match(line).group(1).lstrip().rstrip()
                    y = ana.match(line).group(2).lstrip().rstrip()
                    z = ana.match(line).group(3).lstrip().rstrip()
                    if self.try_int(y) and self.try_int(z):
                        newcode.append('MVI A,' + y)
                        newcode.append('ANI ' + z)
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['MVI']
                        memaddr += self.oplen['ANI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(y) and not self.try_int(z):
                        newcode.append('LDA ' + str(self.symTable[filename][z]))
                        newcode.append('ANI ' + y)
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ANI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(z) and not self.try_int(y):
                        newcode.append('LDA ' + str(self.symTable[filename][y]))
                        newcode.append('ANI ' + z)
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ANI']
                        memaddr += self.oplen['STA']
                    elif not self.try_int(y) and not self.try_int(z):
                        newcode.append('LDA ' + str(self.symTable[filename][y]))
                        newcode.append('MOV B,A')
                        newcode.append('LDA ' + str(self.symTable[filename][z]))
                        newcode.append('ANA B')
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['MOV']
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ANA']
                        memaddr += self.oplen['STA']
                elif ora.match(line):
                    x = ora.match(line).group(1).lstrip().rstrip()
                    y = ora.match(line).group(2).lstrip().rstrip()
                    z = ora.match(line).group(3).lstrip().rstrip()
                    if self.try_int(y) and self.try_int(z):
                        newcode.append('MVI A,' + y)
                        newcode.append('ORI ' + z)
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['MVI']
                        memaddr += self.oplen['ORI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(y) and not self.try_int(z):
                        newcode.append('LDA ' + str(self.symTable[filename][z]))
                        newcode.append('ORI ' + y)
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ORI']
                        memaddr += self.oplen['STA']
                    elif self.try_int(z) and not self.try_int(y):
                        newcode.append('LDA ' + str(self.symTable[filename][y]))
                        newcode.append('ORI ' + z)
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ORI']
                        memaddr += self.oplen['STA']
                    elif not self.try_int(y) and not self.try_int(z):
                        newcode.append('LDA ' + str(self.symTable[filename][y]))
                        newcode.append('MOV B,A')
                        newcode.append('LDA ' + str(self.symTable[filename][z]))
                        newcode.append('ORA B')
                        newcode.append('STA ' + str(self.symTable[filename][x]))
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['MOV']
                        memaddr += self.oplen['LDA']
                        memaddr += self.oplen['ORA']
                        memaddr += self.oplen['STA']
                elif slop.match(line):
                    x = slop.match(line).group(1).lstrip().rstrip()
                    if self.try_int(x):
                        newcode.append('PUSH D')
                        newcode.append('MVI E,' + x)
                        memaddr += self.oplen['PUSH']
                        memaddr += self.oplen['MVI']
                        loopctr += 1
                elif elop.match(line):
                    newcode.append('MOV A,E')
                    newcode.append('SUI 1')
                    newcode.append('MOV E,A')
                    newcode.append('JNZ ' + str(self.symTable[filename][loopctr - 1]))
                    newcode.append('POP D')
                    memaddr += self.oplen['MOV']
                    memaddr += self.oplen['SUI']
                    memaddr += self.oplen['MOV']
                    memaddr += self.oplen['JNZ']
                    memaddr += self.oplen['POP']
                    loopctr -= 1
                elif ifgt.match(line):
                    x = ifgt.match(line).group(1).lstrip().rstrip()
                    y = ifgt.match(line).group(2).lstrip().rstrip()
                    newcode.append('LDA ' + str(self.symTable[filename][x]))
                    newcode.append('MOV B,A')
                    newcode.append('LDA ' + str(self.symTable[filename][y]))
                    newcode.append('SUB B')
                    newcode.append('JP &&&' + str(ifctr))
                    newcode.append('JZ &&&' + str(ifctr))
                    ifctr += 1
                    memaddr += self.oplen['LDA']
                    memaddr += self.oplen['MOV']
                    memaddr += self.oplen['LDA']
                    memaddr += self.oplen['SUB']
                    memaddr += self.oplen['JP']
                    memaddr += self.oplen['JZ']
                elif ifeq.match(line):
                    x = ifeq.match(line).group(1).lstrip().rstrip()
                    y = ifeq.match(line).group(2).lstrip().rstrip()
                    newcode.append('LDA ' + str(self.symTable[filename][x]))
                    newcode.append('MOV B,A')
                    newcode.append('LDA ' + str(self.symTable[filename][y]))
                    newcode.append('SUB B')
                    newcode.append('JNZ &&&' + str(ifctr))
                    ifctr += 1
                    memaddr += self.oplen['LDA']
                    memaddr += self.oplen['MOV']
                    memaddr += self.oplen['LDA']
                    memaddr += self.oplen['SUB']
                    memaddr += self.oplen['JNZ']
                elif ifgte.match(line):
                    ifjmp[ifctr - 1] = memaddr

            outfile.write('\n'.join(newcode))
            outfile.close()
            self.filelen[filename] = memaddr
            print("self.filelen is")
            print(self.filelen)
            inputfile = open(filename + '.l', 'r')
            code = inputfile.read()
            lines = code.split('\n')
            newcode = []
            for line in lines:
                if '&&&' in line:
                    tag = line.split(' ')[1]
                    linenum = tag.split('&&&')[1].lstrip().rstrip()
                    linenum = int(linenum)
                    newtag = '#' + str(ifjmp[linenum])
                    newcode.append(line.replace(tag, newtag))
                else:
                    newcode.append(line)
            outfile = open(filename + '.li', 'w')
            print("newcode of " + filename + "in Pass2: ")
            print(newcode)

            outfile.write('\n'.join(newcode))
            pass_two_box = self.shell_ui.get_object("pass_two_box")
            tv = Gtk.TextView()
            tb = tv.get_buffer()
            tb.set_text('\n'.join(newcode))
            label = Gtk.Label("Pass 2 for " + filename + " : ")
            pass_two_box.add(label)
            pass_two_box.add(tv)
            pass_two_box.show_all()
            outfile.close()
        print("lol01")
        print(self.filelen)
