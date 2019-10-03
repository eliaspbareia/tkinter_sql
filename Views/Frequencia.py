from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

import os


class Frequencia(object):

    IMGDIR = os.path.join(os.path.dirname(__file__), 'imagens')

    def __init__(self, root, model):
        self.toplevel = root
        self.toplevel.title('Controle de Frequência')
        self.modelo = model()

        self.operacao = 'Browse'
        self.info_label = StringVar()
        """Configuração inicial dos radiobutton"""
        self.presenca = StringVar()
        self.PRESENCA = [
            ("Presente", "P"),
            ("Ausente", "F"),
            ("Justificada", "J")
        ]
        self.presenca.set("P")

        self.ANO = [
            2019,
            2020,
            2021,
            2022
        ]

        """Estilos"""
        style = ttk.Style()
        style.configure("BW.TLabel", padding=6, foreground="white", background="brown", font=('helvetica', 9, 'bold'))
        style.configure("BW.TEntry", padding=6, background="#ccc", relief="flat")
        #opcoes combobox -column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky
        style.configure("BW.TCombo", ipady=5, relief="flat")
        style.configure("BW.TButton", padding=6, relief="flat", background="#ccc")
        style.configure('BW.Treeview', highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("BW.Treeview.Heading", background="blue", foreground="brown", relief="flat")
        style.configure("BW.TDataentry", fieldbackground='light green', background='dark green', foreground='dark blue', arrowcolor='white')
        """Imagens para os botões"""
        self.btnNewImage = PhotoImage(file=self.IMGDIR + '\\new.png').subsample(3, 3)
        self.btnDelImage = PhotoImage(file=self.IMGDIR + '\\del.png').subsample(3, 3)
        self.btnSaveImage = PhotoImage(file=self.IMGDIR + '\\disk_save.png').subsample(3, 3)
        self.btnCancelImage = PhotoImage(file=self.IMGDIR + '\\cancel.png').subsample(3, 3)
        self.btnLoopImage = PhotoImage(file=self.IMGDIR + '\\iconfinder_refresh_326679.png').subsample(3, 3)
        self.btnCloseImage = PhotoImage(file=self.IMGDIR + '\\iconfinder_icons_exit2_1564506.png').subsample(3, 3)

        self.searchFrame = ttk.Frame(self.toplevel)
        self.searchFrame.grid(column=0, row=0, padx=10, pady=10, columnspan=2)
        self.tableFrame = ttk.Frame(self.toplevel)
        self.tableFrame.grid(column=0, row=1, padx=10, pady=10)
        self.formFrame = ttk.LabelFrame(self.toplevel, text='Informações')
        self.formFrame.grid(column=1, row=1, padx=10, pady=10)

        self.statusFrame = ttk.Frame(self.toplevel, border=1, relief=FLAT)
        self.statusFrame.grid(column=0, row=2, padx=10, pady=10, columnspan=2)

        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(1, weight=1)

        self.createtable()
        self.createsearch()
        self.createform()
        self.createBarraStatus()
        self.estadoBotoes()



    def createform(self):
        self.container1 = Frame(self.formFrame)
        self.container1['pady'] = 10
        self.container1.grid(row=1, column=0)
        self.lblCadastro = ttk.Label(self.container1, style="BW.TLabel", text="Cadastro:", width=12)
        self.lblCadastro.pack(side=LEFT)
        self.txtCadastro = ttk.Entry(self.container1, style="BW.TEntry")
        self.txtCadastro['state'] = DISABLED
        self.txtCadastro['width'] = 20
        self.txtCadastro.pack(side=LEFT, padx=(10, 5))

        self.container2 = Frame(self.formFrame)
        self.container2['pady'] = 10
        self.container2.grid(row=2, column=0)
        self.lblReuniao = ttk.Label(self.container2, style="BW.TLabel", text="Data Reunião:", width=12)
        self.lblReuniao.pack(side=LEFT)
        # self.txtReuniao = ttk.Entry(self.container2, style="BW.TEntry")
        # self.txtReuniao['width'] = 20
        # self.txtReuniao['state'] = DISABLED
        # self.txtReuniao.pack(side=LEFT, padx=(10, 5))
        # self.txtReuniao.bind("<FocusOut>", self.formatadata)
        self.txtReuniao = DateEntry(self.container2, width=11, background='darkblue', foreground='white', borderwidth=2, year=2019, locale='pt_BR', date_pattern='yyyy-MM-dd' )
        self.txtReuniao.pack(side=LEFT, ipadx=25, padx=(10,5))

        self.container3 = Frame(self.formFrame)
        self.container3['pady'] = 10
        self.container3.grid(row=3, column=0)
        for text, mode in self.PRESENCA:
            self.rdbPresenca = Radiobutton(self.container3, text=text, variable=self.presenca, value=mode)
            self.rdbPresenca.pack(anchor=W, side=LEFT, expand=1)

        """ Cria os botões de ações """
        self.container4 = ttk.Frame(self.formFrame)
        self.container4.grid(row=4, column=0, pady=10)
        self.btnNew = ttk.Button(self.container4, style="BW.TButton", compound=LEFT)
        self.btnNew['text'] = 'Nova'
        self.btnNew['width'] = 5
        self.btnNew['command'] = self.cadastraFrequencia
        self.btnNew['image'] = self.btnNewImage
        self.btnNew.pack(side=LEFT, padx=10, pady=10)

        self.btnExcluir = ttk.Button(self.container4, style="BW.TButton", compound=LEFT)
        self.btnExcluir['text'] = 'Excluir'
        self.btnExcluir['width'] = 6
        self.btnExcluir['command'] = self.excluirFrequencia
        self.btnExcluir['image'] = self.btnDelImage
        self.btnExcluir.pack(side=LEFT, padx=10, pady=10)

        self.btnSave = ttk.Button(self.container4, style="BW.TButton", compound=LEFT)
        self.btnSave['text'] = 'Salvar'
        self.btnSave['width'] = 6
        self.btnSave['command'] = self.saveFrequencia
        self.btnSave['image'] = self.btnSaveImage
        self.btnSave.pack(side=LEFT, padx=10, pady=10)

        self.btnCancel = ttk.Button(self.container4, style="BW.TButton", compound=LEFT)
        self.btnCancel['text'] = 'Cancelar'
        self.btnCancel['width'] = 8
        self.btnCancel['command'] = self.cancelaFrequencia
        self.btnCancel['image'] = self.btnCancelImage
        self.btnCancel.pack(side=LEFT, padx=10, pady=10)


    def createtable(self):
        self.tree = ttk.Treeview(self.tableFrame, column=(1, 2, 3), show="headings", selectmode='browse')
        self.tree['style'] = "BW.Treeview"
        self.tree.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.tree.heading(1, text='#')
        self.tree.heading(2, text='Data')
        self.tree.heading(3, text='Frequência')
        self.tree.column(1, width=50, anchor='center')
        self.tree.column(2, width=100, anchor='center')
        self.tree.column(3, width=150, anchor='center')
        self.tree.bind('<Double-Button-1>', self.EditMember) #clique duplo
        self.tree.bind('<Button-1>', self.navega)
        self.scroll = ttk.Scrollbar(self.tableFrame, orient=VERTICAL)
        self.scroll.grid(row=0, column=3, sticky='ns')
        self.tree.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.tree.yview)

    def createsearch(self):
        self.label = ttk.Label(self.searchFrame, text='Pesquisa: ', style='BW.TLabel', compound=LEFT)
        self.label.grid(column=0, row=0,  padx=(5, 5))
        self.cbxData = ttk.Combobox(self.searchFrame,values=self.ANO)
        self.cbxData.current(0)
        self.cbxData.grid(row=0, column=1, ipady=5)
        self.txtSearch = ttk.Entry(self.searchFrame, style="BW.TEntry")
        self.txtSearch.focus_set()
        self.txtSearch.grid(row=0, column=2, columnspan=4, sticky=W, ipadx=50, padx=(10, 5))
        #fazer o bind para a statusbar
        self.txtSearch.bind("<FocusIn>", lambda event: self.statuscommand('Entre com o número do cadastro.'))
        self.btnSearch = ttk.Button(self.searchFrame, style="BW.TButton", compound=LEFT)
        self.btnSearch['text'] = 'Localizar'
        self.btnSearch['width'] = 10
        self.btnSearch['command'] = self.localizarmember
        self.btnSearch.grid(row=0, column=6, padx=(10, 5))

    def createBarraStatus(self):
        self.lblMessage = ttk.Label(self.statusFrame, textvar=self.info_label, relief=SUNKEN)
        self.lblMessage.pack(expand=1, fill=X, pady=10, padx=5)

    def statuscommand(self,  texto):
        self.info_label.set(texto)

    def localizarmember(self):
        md = self.modelo
        valor = self.txtSearch.get()
        md.num_cadastro = valor
        md.ano = self.cbxData.get()
        lista = md.getmember()
        try:
            if len(lista) == 0:
                items = self.tree.get_children()
                self.operacao = 'Browse'
                for item in items:
                    self.tree.delete(item)
            else:
                items = self.tree.get_children()
                for item in items:
                    self.tree.delete(item)
                for row in lista:
                    self.tree.insert('','end', values=(row[0], row[1], row[2]))
                self.txtCadastro.insert(0,self.txtSearch.get())
                self.operacao = 'Insert'
                self.estadoBotoes()

        except :
            self.mensagem('Aviso', 'O registro de cadastro nº{} não foi localizado.\nOu não há registro para o ano informado.'.format(valor))

    def reloadTable(self):
        md = self.modelo
        md.num_cadastro = self.txtSearch.get()
        md.ano = self.cbxData.get()
        lista = md.getmember()
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        for row in lista:
            self.tree.insert('', 'end', values=(row[0], row[1], row[2]))

    def navega(self, event):
        self.operacao = 'Delete'
        self.estadoBotoes()

    def EditMember(self, event):
        selection = self.tree.selection()
        for selection in self.tree.selection():
            currentItem = self.tree.set(selection, "#1")
            if currentItem:
                lista = self.modelo.getById(currentItem)
                for row in lista:
                    self.id = row[0]
                    self.txtReuniao['state'] = NORMAL
                    self.txtCadastro.delete(0, END)
                    self.txtCadastro.insert(0, row[1])
                    self.txtReuniao.delete(0, END)
                    self.txtReuniao.insert(0, row[2])
                    self.presenca.set(row[3])
                    self.operacao = 'Edit'
                    self.estadoBotoes()
        return

    """Outras funções"""
    def saveFrequencia(self):
        md = self.modelo
        selection = self.tree.selection()
        for selection in self.tree.selection():
            currentItem = self.tree.set(selection, "#1")
            if currentItem:
                md.id = currentItem
        if self.txtCadastro.get() == '':
            md.num_cadastro = self.txtSearch.get()
        else:
            md.num_cadastro = self.txtCadastro.get()
        md.data_reuniao = self.txtReuniao.get()
        md.presenca = self.presenca.get()
        md.ano = self.pegaano(self.txtReuniao.get())
        self.mensagem('Incluir/Alterar', md.savefrequencia(self.operacao))
        self.txtReuniao.delete(0, END)
        self.txtReuniao['state'] = DISABLED
        self.operacao = 'Insert'
        self.estadoBotoes()
        self.reloadTable()

    def excluirFrequencia(self):
        selection = self.tree.selection()
        for selection in self.tree.selection():
            currentItem = self.tree.set(selection, "#1")
            if currentItem:
                lista = self.modelo.delete(currentItem)
                self.mensagem('Delete', lista)
                #self.createtable()
                self.reloadTable()
                self.operacao = 'Delete'
                self.estadoBotoes()
                break
        else:
            self.error('Aviso', 'Você deve selecionar um item primeiro.')

    def cancelaFrequencia(self):
        self.operacao = 'Delete'
        self.estadoBotoes()


    def cadastraFrequencia(self):
        #limpa as caixas de texto     
        self.txtReuniao.delete(0, END)
        self.txtReuniao['state'] = NORMAL
        self.operacao = 'Novo'
        self.estadoBotoes()

    def estadoBotoes(self):
        if self.operacao == 'Browse':
            self.btnNew['state'] = DISABLED
            self.btnExcluir['state'] = DISABLED
            self.btnSave['state'] = DISABLED
            self.btnCancel['state'] = DISABLED
        elif self.operacao == 'Insert':
            self.btnNew['state'] = NORMAL
            self.btnExcluir['state'] = DISABLED
            self.btnSave['state'] = DISABLED
            self.btnCancel['state'] = DISABLED
        elif self.operacao == 'Novo':
            self.btnNew['state'] = DISABLED
            self.btnExcluir['state'] = DISABLED
            self.btnSave['state'] = NORMAL
            self.btnCancel['state'] = NORMAL
        elif self.operacao == 'Delete':
            self.btnNew['state'] = NORMAL
            self.btnExcluir['state'] = NORMAL
            self.btnSave['state'] = DISABLED
            self.btnCancel['state'] = DISABLED
        elif self.operacao == 'Edit':
            self.btnNew['state'] = DISABLED
            self.btnExcluir['state'] = DISABLED
            self.btnSave['state'] = NORMAL
            self.btnCancel['state'] = NORMAL


    def exitForm(self):
        self.toplevel.destroy()

    def mensagem(self, tipo, msg):
        messagebox.showinfo(tipo, msg)

    def error(self,tipo, msg):
        messagebox.showwarning(tipo,msg)
        


    def validate_text(self, texto):
        if len(texto) == 0:
            return False
        else:
            return True

    def pegaano(self, ano):
        ano = ano.split('-')
        return ano[0]

