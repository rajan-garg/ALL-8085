from gi.repository import Gtk


class Linker:
    def __init__(self, shell_ui, symtable, globtable, filelen):
        self.shell_ui = shell_ui
        self.symTable = symtable
        self.globTable = globtable
        self.filelen = filelen

    def get_loc(self, exter, filenames):
        for filename in filenames:
            filename = filename.split('.')[0]
            for vari in self.globTable[filename]:
                # print(vari)
                if vari == exter:
                    val = self.symTable[filename][vari]
                    val = val.split('#')[1]
                    return filename, val

    def linker(self, filenames):
        startcount = {}
        lastcount = 0
        for filename in filenames:
            print(filenames)
            startcount[filename.split('.')[0]] = lastcount
            print(self.filelen)
            lastcount += self.filelen[filename.split('.')[0]]
        for filename in filenames:
            filename = filename.split('.')[0]
            inputfile = open(filename + '.li', 'r')
            code = inputfile.read()
            lines = code.split('\n')
            outfile = open(filename + '.loaded', 'w')
            newcode = []
            for line in lines:
                line = line.lstrip().rstrip()
                if '$' in line:
                    exter = line.split(' ')[1].split('$')[1]
                    x, y = self.get_loc(exter, filenames)
                    newline = line.replace('$' + exter, '@' + str(int(startcount[x] + int(y))))
                    newcode.append(newline)
                else:
                    newcode.append(line)

            outfile.write('\n'.join(newcode))
            outfile.close()

        outfile = open(filenames[0].split('.')[0] + '.ls', 'w')
        linkcode = []
        for filename in filenames:
            filename = filename.split('.')[0]
            inputfile = open(filename + '.loaded', 'r')
            code = inputfile.read()
            lines = code.split('\n')
            for line in lines:
                line = line.lstrip().rstrip()
                if '#' in line:
                    tag = line.split(' ')[1]
                    newtag = '#' + str((int(tag.split('#')[1]) + startcount[filename]))
                    linkcode.append(line.replace(tag, newtag))
                elif '@' in line:
                    newtag = line.replace('@', '#')
                    linkcode.append(newtag)
                else:
                    linkcode.append(line)
        print("Output of linker : ")
        print(linkcode)
        outfile.write('\n'.join(linkcode))
        results_box = self.shell_ui.get_object("linker_results_box")
        tv = Gtk.TextView()
        tb = tv.get_buffer()
        tb.set_text('\n'.join(linkcode))
        results_box.add(tv)
        results_box.show_all()
        outfile.close()
