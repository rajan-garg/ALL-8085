from gi.repository import Gtk


class Loader:
    def __init__(self, shell_ui):
        self.shell_ui = shell_ui

    def loader(self, filenames):
        offset = 0
        filename = filenames[0].split('.')[0]
        inputfile = open(filename + '.ls', 'r')
        code = inputfile.read()
        lines = code.split('\n')
        outfile = open(filename + '.8085', 'w+')
        linkcode = []
        for line in lines:
            if '#' in line:
                tag = line.split(' ')[1]
                newtag = str((int(tag.split('#')[1]) + offset))
                linkcode.append(line.replace(tag, newtag))
            else:
                linkcode.append(line)
        linkcode.append('HLT')
        outfile.write('\n'.join(linkcode))
        old_box = self.shell_ui.get_object("loader_old_result_box")
        tv = Gtk.TextView()
        tb = tv.get_buffer()
        tb.set_text('\n'.join(linkcode))
        old_box.add(tv)
        old_box.show_all()

        outfile.close()

    def loader2(self, filenames):
        offset = 0
        if self.shell_ui.get_object("loader_offset_entry").get_text() is not "":
            offset = self.shell_ui.get_object("loader_offset_entry").get_text()
        filename = filenames[0].split('.')[0]
        inputfile = open(filename + '.ls', 'r')
        code = inputfile.read()
        lines = code.split('\n')
        outfile = open(filename + '.8085_O', 'w+')
        linkcode = []
        for line in lines:
            if '#' in line:
                tag = line.split(' ')[1]
                newtag = str((int(tag.split('#')[1]) + int(offset)))
                linkcode.append(line.replace(tag, newtag))
            else:
                linkcode.append(line)
        linkcode.append('HLT')
        outfile.write('\n'.join(linkcode))
        new_box = self.shell_ui.get_object("loader_new_result_box")
        tv = Gtk.TextView()
        tb = tv.get_buffer()
        tb.set_text('\n'.join(linkcode))
        new_box.add(tv)
        new_box.show_all()
        outfile.close()
