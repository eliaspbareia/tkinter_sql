from tkinter import Tk, Menu, Toplevel
from tkinter import ttk

from Views.Members import Members as formMember
from Views.Frequencia import Frequencia as formFrequencia
from Views.printfrequencia import Print as printFrequencia
from Models.MemberModel import MemberModel as mmember
from Models.FrequenciaModel import FrequenciaModel as ffrequencia


class Sistema():
    def __init__(self):
        self.root = Tk()
        self.root.configure(background='white')
        self.frame = ttk.Frame(self.root)
        self.frame.pack()
        """Cria o menu"""
        self.menu = Menu(self.root)
        self.menuArquivo = Menu(self.menu, tearoff=0)
        #self.menuArquivo.add_command(label="Membro")
        self.menuArquivo.add_command(label="Membro", command=self.showMembros)
        self.menuArquivo.add_command(label="Frequências", command=self.showFrequencias)
        self.menuArquivo.add_command(label="Imprimir Frequências", command=self.printFrequencias)
        #self.menuArquivo.add_command(label="Frequência")
        self.menuArquivo.add_command(label="Sobre")
        self.menuArquivo.add_separator()
        self.menuArquivo.add_command(label="Sair", command=self.root.quit)
        self.menu.add_cascade(label="Sistema", menu=self.menuArquivo)
        self.root.config(menu=self.menu)

    def showMembros(self):
        self.viewmembros = Toplevel(self.root)
        self.viewmembros.geometry("630x550")
        self.center(self.viewmembros)
        self.viewmembros.transient(self.root)
        self.viewmembros.resizable(False, False)
        self.viewmembros.focus_force()
        self.viewmembros.grab_set()
        formMember(self.viewmembros, mmember)

    def showFrequencias(self):
        self.viewfreq = Toplevel(self.root)
        self.viewfreq.geometry("760x355") #largura e altura (widthxhight)
        self.center(self.viewfreq)
        self.viewfreq.transient(self.root)
        self.viewfreq.resizable(False, False)
        self.viewfreq.focus_force()
        self.viewfreq.grab_set()
        formFrequencia(self.viewfreq, ffrequencia)

    def printFrequencias(self):
        self.printfreq = Toplevel(self.root)
        self.printfreq.geometry("760x355") #largura e altura (widthxhight)
        self.center(self.printfreq)
        self.printfreq.transient(self.root)
        self.printfreq.resizable(False, False)
        self.printfreq.focus_force()
        self.printfreq.grab_set()
        printFrequencia(self.printfreq,mmember, ffrequencia)

    def center(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() -  win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height //2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    def start(self):
        self.root.title("Membros")
        self.root.geometry("600x240")
        self.root.deiconify()
        self.root.attributes('-alpha',0.0)
        self.center(self.root)
        self.root.attributes('-alpha',1.0)
        self.root.mainloop()
