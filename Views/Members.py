from tkinter import *
from tkinter import ttk, messagebox
import os


class Members(object):

    imgdir = os.path.join(os.path.dirname(__file__),'imagens')

    def __init__(self, root, model):
        """Estilos"""
        style = ttk.Style()
        style.configure("BW.TLabel", padding=6, foreground="white" , background="brown", font=('helvetica', 9, 'bold'))
        style.configure("BW.TEntry", padding=6, background="#ccc", relief="flat")
        style.configure("BW.TButton", padding=6, relief="flat", background="#ccc")
        style.configure('BW.Treeview', highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("BW.Treeview.Heading", background="blue", foreground="brown", relief="flat" )

        """Imagens para os botões"""
        self.btnNewImage = PhotoImage(file=self.imgdir+'\\new.png').subsample(3, 3)
        self.btnDelImage = PhotoImage(file=self.imgdir+'\\del.png').subsample(3,3)
        self.btnSaveImage = PhotoImage(file=self.imgdir+'\\disk_save.png').subsample(3,3)
        self.btnCancelImage = PhotoImage(file=self.imgdir+'\\cancel.png').subsample(3, 3)
        self.btnLoopImage = PhotoImage(file=self.imgdir+'\\iconfinder_refresh_326679.png').subsample(3, 3)
        self.btnCloseImage = PhotoImage(file=self.imgdir+'\\iconfinder_icons_exit2_1564506.png').subsample(3,3)

        self.toplevel = root
        self.model = model()

        self.operacao = "BROWSER"  #BROWSER EDIT INSERT

        self.searchFrame = ttk.Frame(self.toplevel)
        self.searchFrame.grid(column=0, row=0, padx=10, pady=10)
        self.tableFrame = ttk.Frame(self.toplevel)
        self.tableFrame.grid(column=0, row=1, padx=10, pady=10)
        self.formFrame = ttk.Frame(self.toplevel)
        self.formFrame.grid(column=0, row=2, padx=10, pady=10)
        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(1, weight=1)

        self.CreateSearch()
        self.CreateTable()
        self.CreateForm()
        self.LoadITable(tipoLeitura = 'all') #all byname
        self.initButton()


    def CreateSearch(self):
        self.label = ttk.Label(self.searchFrame, text='Pesquisa por nome: ', style='BW.TLabel', compound=LEFT)
        self.label.grid(column=0, row=0)
        self.txtSearch  = ttk.Entry(self.searchFrame, style="BW.TEntry")
        self.txtSearch.grid(row=0, column=2, columnspan=4, sticky=W, ipadx=100, padx=(10,5))
        self.btnSearch = ttk.Button(self.searchFrame, style="BW.TButton", compound=LEFT)
        self.btnSearch['text'] = 'Localizar'
        self.btnSearch['width'] = 12
        self.btnSearch['command'] = self.localizarMember
        self.btnSearch.grid(row=0, column=6, padx=(10,5))

    def CreateTable(self):
        self.tree = ttk.Treeview(self.tableFrame, column=(1,2,3), show="headings", selectmode='browse')
        self.tree['style'] = "BW.Treeview"
        self.tree.grid(row=0, column=0, columnspan=8, sticky='nsew')
        self.tree.heading(1, text='Cadastro')
        self.tree.heading(2, text='Nome')
        self.tree.heading(3, text='Telefone')
        self.tree.column(1, width=100, anchor='center')
        self.tree.column(2, width=300, anchor='w')
        self.tree.column(3, width=150, anchor='center')
        self.tree.bind('<Double-Button-1>', self.EditMember) #clique duplo
        self.tree.bind('<Button-1>', self.navega)
        self.scroll = ttk.Scrollbar(self.tableFrame, orient=VERTICAL)
        self.scroll.grid(row=0, column=9, sticky='ns')
        self.tree.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.tree.yview)


    def CreateForm(self):
        self.container1 = ttk.Frame(self.formFrame)
        self.container1.grid(row=1, column=0, pady=10)
        self.cadastro = ttk.Label(self.container1, text='Cadastro: ', style='BW.TLabel', compound=LEFT)
        self.cadastro['width'] = 10
        self.cadastro.pack(side=LEFT)
        self.txtCadastro = ttk.Entry(self.container1, style="BW.TEntry")
        self.txtCadastro.focus_set()
        self.txtCadastro['width'] = 70
        self.txtCadastro.pack(side=LEFT, padx=(10,5))

        self.container2 = ttk.Frame(self.formFrame)
        self.container2.grid(row=2, column=0, pady=15)
        self.nome = ttk.Label(self.container2, text='Nome: ', style='BW.TLabel', compound=LEFT)
        self.nome['width'] = 10
        self.nome.pack(side=LEFT)
        self.txtNome = ttk.Entry(self.container2, style="BW.TEntry")
        self.txtNome['width'] = 70
        self.txtNome.pack(side=LEFT, padx=(10,5))

        self.container3 = ttk.Frame(self.formFrame)
        self.container3.grid(row=3, column=0, pady=10)
        self.telefone = ttk.Label(self.container3, text='Telefone: ', style='BW.TLabel', compound=LEFT)
        self.telefone['width'] = 10
        self.telefone.pack(side=LEFT)
        self.txtTelefone = ttk.Entry(self.container3, style="BW.TEntry")
        self.txtTelefone['width'] = 70
        self.txtTelefone.pack(side=LEFT, padx=(10,5))
        #self.txtTelefone.bind("<FocusOut>", self.format_fone_entry_widget)

        """ Cria os botões de ações """
        self.container4 = ttk.Frame(self.formFrame)
        self.container4.grid(row=4, column=0, pady=10)
        self.btnNew = ttk.Button(self.container4, style="BW.TButton", compound=LEFT)
        self.btnNew['text']='Novo'
        self.btnNew['width'] = 10
        self.btnNew['command'] = self.newMember
        self.btnNew['image'] = self.btnNewImage
        self.btnNew.pack(side=LEFT, padx=10, pady=10)

        self.btnSave = ttk.Button(self.container4, style="BW.TButton", compound=LEFT)
        self.btnSave['text']='Salva'
        self.btnSave['width'] = 10
        self.btnSave['command'] = self.saveMember
        self.btnSave['image'] = self.btnSaveImage
        self.btnSave.pack(side=LEFT, padx=10, pady=10)

        self.btnCancel = ttk.Button(self.container4, style="BW.TButton", compound=LEFT)
        self.btnCancel['text']='Cancela'
        self.btnCancel['width'] = 10
        self.btnCancel['command'] = self.cancelMember
        self.btnCancel['image'] = self.btnCancelImage
        self.btnCancel.pack(side=LEFT, padx=10, pady=10)

        self.btnDelete = ttk.Button(self.container4, style="BW.TButton", compound=LEFT)
        self.btnDelete['text']='Deleta'
        self.btnDelete['width'] = 10
        self.btnDelete['command'] = self.deleteMember
        self.btnDelete['image'] = self.btnDelImage
        self.btnDelete.pack(side=LEFT, padx=10, pady=10)

        self.btnClose = ttk.Button(self.container4, style="BW.TButton", compound=LEFT)
        self.btnClose['text']='Sair'
        self.btnClose['width'] = 10
        self.btnClose['command'] = self.exitForm
        self.btnClose['image'] = self.btnCloseImage
        self.btnClose.pack(side=LEFT, padx=10, pady=10)

    """Funções"""
    """Funções INSERT/DELETE/SAVE/EDIT """
    def newMember(self):
        self.operacao = 'INSERT'
        self.initButton()
        self.limpaCampos()

    def saveMember(self):
        if self.operacao == 'INSERT':
            md = self.model
            cadastro = self.txtCadastro.get()
            nome = self.txtNome.get()
            telefone = self.txtTelefone.get()
            cad, nom, phone = True, True, True
            valida = [
                      cad == self.validate_number(cadastro),
                      nom == self.validate_text(nome),
                      phone == self.validate_number(telefone)
            ]

            if all(valida) and self.validada_Telefone(telefone):
                md.memberid = self.txtCadastro.get()
                md.membername = self.txtNome.get()
                md.memberphone = self.txtTelefone.get()
                self.mensagem('Insert', md.insert())
                #self.mensagem('Aviso','O cadastro número {} foi adicionado com sucesso!'.format(self.txtCadastro.get()))
                self.CreateTable()
                self.LoadITable(tipoLeitura='all')
                self.operacao = 'BROWSER'
                self.limpaCampos()
                self.initButton()
            else:
                self.error('Aviso', 'Todos os campos devem ser preenchidos corretamente.\n * Cadastro deve conter apenas números\n * Telefone deve conter 11 números')
        elif self.operacao == 'EDIT':
            md = self.model
            cadastro = self.txtCadastro.get()
            nome = self.txtNome.get()
            telefone = self.txtTelefone.get()
            cad, nom, phone = True, True, True
            valida = [
                      cad == self.validate_number(cadastro),
                      nom == self.validate_text(nome),
                      phone == self.validate_number(telefone)
            ]
            if all(valida) and self.validada_Telefone(telefone):
                md.memberid = self.txtCadastro.get()
                md.membername = self.txtNome.get()
                md.memberphone = self.txtTelefone.get()
                self.mensagem('Edit', md.save())
                # self.mensagem('Aviso','O cadastro número {} foi adicionado com sucesso!'.format(self.txtCadastro.get()))
                self.CreateTable()
                self.LoadITable(tipoLeitura='all')
                self.operacao = 'BROWSER'
                self.limpaCampos()
                self.initButton()
            else:
                self.error('Aviso', 'Todos os campos devem ser preenchidos corretamente.\n * Cadastro deve conter apenas números\n * Telefone deve conter 11 números')


    def cancelMember(self):
        self.operacao = 'BROWSER'
        self.initButton()
        self.limpaCampos()

    def deleteMember(self):
        selection = self.tree.selection()
        for selection in self.tree.selection():
            currentItem = self.tree.set(selection,"#1")
            if currentItem:
                lista = self.model.delete(currentItem)
                self.mensagem('Delete', lista)
                self.CreateTable()
                self.LoadITable(tipoLeitura='all')
                self.operacao = 'BROWSER'
                self.limpaCampos()
                self.initButton()
                break #http://book.pythontips.com/en/latest/for_-_else.html
        else:
            self.error('Aviso', 'Você deve selecionar um item primeiro.')

    """Função SEARCH """
    def localizarMember(self):
        self.LoadITable(tipoLeitura='byname')
        self.txtSearch.delete(0, END)


    def EditMember(self, event):
        self.operacao = 'EDIT'
        self.initButton()
        selection = self.tree.selection()
        for selection in self.tree.selection():
            currentItem = self.tree.set(selection,"#1")
            if currentItem:
                # query = 'SELECT memberid, membername, memberphone FROM member WHERE memberid='+currentItem+' ORDER BY membername'
                # lista = self.model.execute_db_query(query)
                lista = self.model.getById(currentItem)
                for row in lista:
                    self.txtCadastro.delete(0, END)
                    self.txtCadastro.insert(0, row[0])
                    self.txtNome.delete(0, END)
                    self.txtNome.insert(0, row[1])
                    self.txtTelefone.delete(0, END)
                    self.txtTelefone.insert(0, row[2])
        return

    """Funções relacionadas a tabela """
    def navega(self, event):
        self.operacao = 'DELETE'
        self.initButton()


    def LoadITable(self, tipoLeitura):
        if tipoLeitura == 'all':
            lista = self.model.getAll()
        elif tipoLeitura == 'byname':
            lista = self.model.getByName(self.txtSearch.get().upper())
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        for row in lista:
            self.tree.insert('','end', values=(row[0], row[1], row[2]))

    """Outras funções"""
    def exitForm(self):
        self.toplevel.destroy()

    def initButton(self):
        if self.operacao == 'BROWSER':
            self.btnNew['state'] = NORMAL
            self.btnSave['state'] = DISABLED
            self.btnCancel['state'] = DISABLED
            self.btnDelete['state'] = NORMAL
            self.txtCadastro['state'] = DISABLED
            self.txtNome['state'] = DISABLED
            self.txtTelefone['state'] = DISABLED
        elif self.operacao == 'EDIT':
            self.btnNew['state'] = DISABLED
            self.btnSave['state'] = NORMAL
            self.btnCancel['state'] = NORMAL
            self.btnDelete['state'] = DISABLED
            self.txtCadastro['state'] = NORMAL
            self.txtNome['state'] = NORMAL
            self.txtTelefone['state'] = NORMAL
        elif self.operacao == 'INSERT':
            self.btnNew['state'] = DISABLED
            self.btnSave['state'] = NORMAL
            self.btnCancel['state'] = NORMAL
            self.btnDelete['state'] = DISABLED
            self.txtCadastro['state'] = NORMAL
            self.txtNome['state'] = NORMAL
            self.txtTelefone['state'] = NORMAL
        elif self.operacao == 'DELETE':
            self.btnNew['state'] = DISABLED
            self.btnSave['state'] = DISABLED
            self.btnCancel['state'] = NORMAL
            self.btnDelete['state'] = NORMAL
            self.txtCadastro['state'] = DISABLED
            self.txtNome['state'] = DISABLED
            self.txtTelefone['state'] = DISABLED

    def limpaCampos(self):
        self.txtCadastro.delete(0, END)
        self.txtNome.delete(0, END)
        self.txtTelefone.delete(0, END)

    """Validação dos campos"""
    def validate_text(self, texto):
        if len(texto) == 0:
            return False
        else:
            return True

    def validate_number(self, numero):
        try:
            n = int(numero.replace("(","").replace(")","").replace("-",""))
            return True
        except:
            return False

    def validada_Telefone(self, telefone):
        telefone = telefone.replace("(","").replace(")","").replace("-","")
        if len(telefone) == 10 or len(telefone) == 11:
            self.format_fone_entry_widget(telefone)
            return True
        else:
            self.txtTelefone.focus_set()
            return False

    def format_fone_entry_widget(self, event):
        #(63)99935-5687
        telefone = self.txtTelefone.get().replace("(","").replace(")","").replace("-","")
        if len(telefone) == 10:
            self.txtTelefone.delete(0, END)
            self.txtTelefone.insert(INSERT, '({0}{1}){2}{3}{4}{5}-{6}{7}{8}{9}'.format(*telefone))
        elif len(telefone) == 11:
            self.txtTelefone.delete(0, END)
            self.txtTelefone.insert(INSERT, '({0}{1}){2}{3}{4}{5}{6}-{7}{8}{9}{10}'.format(*telefone))
        else:
            self.error('Aviso','Telefone inválido')
            self.txtTelefone.focus_set()




    def error(self,tipo, msg):
        messagebox.showwarning(tipo,msg)

    def mensagem(self, tipo, msg):
        messagebox.showinfo(tipo, msg)
