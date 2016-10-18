import os
import sys

from gi.repository import Gtk

from linker import Linker
from loader import Loader
from assembler import Assembler
from preprocessor import preprocess
from simulator import Simulator


class AllApp(Gtk.Application):
    # constructor of the Gtk Application

    def __init__(self):
        Gtk.Application.__init__(self)
        self.shell_ui = Gtk.Builder()
        self.shell_ui.add_from_file("shell.glade")
        self.handler_dict = {
            "on_start_file_chooser_button_clicked": self.on_start_file_chooser_button_clicked,
            "on_start_button_clicked": self.on_start_button_clicked,
            "on_simulator_open_file_button_clicked": self.on_simulator_open_file_button_clicked,
            "on_simulate_pass_button_clicked": self.on_simulate_pass_button_clicked,
            "on_run_button_clicked": self.on_run_button_clicked,
            "on_quit_image_menu_item_activate": self.on_quit_activate,
            "on_offset_button_clicked": self.on_offset_button_clicked
        }
        self.shell_ui.connect_signals(self.handler_dict)
        self.x = []
        self.z = []
        self.assembler_instance = None
        self.loader_instance = None
        self.linker_instance = None
        self.simulator_instance = None
        # self.simulator=Simulator()

    def on_offset_button_clicked(self, widget):
        self.loader_instance.loader2(self.x)

    def do_activate(self):
        window = self.shell_ui.get_object("all_window")
        self.add_window(window)
        window.show_all()

    def on_start_file_chooser_button_clicked(self, widget):
        window = self.shell_ui.get_object("all_window")
        dialog = Gtk.FileChooserDialog(title="Please choose a file", parent=window, action=Gtk.FileChooserAction.OPEN,
                                       buttons=(
                                           Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN,
                                           Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selected_file_path = dialog.get_filename()
            relative_path = os.path.basename(selected_file_path)
            inputfile = open(relative_path, "r")
            code = inputfile.read()
            lines = code.split('\n')
            finalfile = lines[0].split('.')[0] + '.8085'
            print(lines[0].split('.')[0])
            print(finalfile)

            entries_box = self.shell_ui.get_object("start_entries_box")
            wids = entries_box.get_children()
            for widget in wids:
                widget.destroy()
            i = 0
            print (lines)
            for line in lines:
                if line != '':
                    self.z.append(line)
                    label = Gtk.Label("Code" + str(i))
                    tv = Gtk.TextView()
                    tb = tv.get_buffer()
                    entries_box.add(label)
                    entries_box.add(tv)
                    i += 1
                    with open(line, "r") as file:
                        s = file.read()
                        tb.set_text(s)
                        print(s)
            self.shell_ui.get_object("start_entry_number_entry").set_text(str(i))
            entries_box.show_all()
            self.x = preprocess(self.z)
            processed_box = self.shell_ui.get_object("processed_box")
            i = 0
            for file_name in self.x:
                if file_name != '':
                    label = Gtk.Label("Code" + str(i))
                    tv = Gtk.TextView()
                    tb = tv.get_buffer()
                    processed_box.add(label)
                    processed_box.add(tv)
                    i += 1
                    with open(file_name, "r") as file:
                        s = file.read()
                        tb.set_text(s)
                        print(s)
            processed_box.show_all()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        dialog.destroy()

    def on_start_button_clicked(self, widget):
        finalfile = self.x[0].split('.')[0] + '.8085'
        info = self.shell_ui.get_object("start_info_label")
        # str1 = ''
        # str1 += 'Interpreting...........\nRunning Assembler \n'
        # info.set_text(str1)
        self.assembler_instance = Assembler(self.shell_ui)
        self.assembler_instance.test(self.x)
        # str1 = str1 + 'Assembler Completed \n' + 'Running Linker \n'
        # info.set_text(str1)
        self.linker_instance = Linker(self.shell_ui, self.assembler_instance.symTable,
                                      self.assembler_instance.globTable,
                                      self.assembler_instance.filelen)
        self.linker_instance.linker(self.x)
        # str1 = str1 + 'Linker Completed \n' + 'Set offset and run loader\n'
        # info.set_text(str1)
        self.loader_instance = Loader(self.shell_ui)
        self.loader_instance.loader(self.x)
        # str1 = str1 + 'Loading Complete \n' + '\t\tFile ready to simulate.\n' + '\t\tFile name is : ' + finalfile + '\n'
        # info.set_text(str1)

    def on_simulator_open_file_button_clicked(self, widget):
        pass

    def on_simulate_pass_button_clicked(self, widget):
        finalfile = self.x[0].split('.')[0] + '.8085'
        self.simulator_instance = Simulator(self.shell_ui, self.shell_ui.get_object("all_window"))
        self.simulator_instance.load(finalfile)

    def on_run_button_clicked(self, widget):
        self.simulator_instance.callbackf()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def on_quit_activate(self, menu_item):
        sys.exit()


app = AllApp()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
