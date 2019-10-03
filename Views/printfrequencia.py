import webbrowser
import base64
import datetime
import os
from tkinter import *
from tkinter import ttk
try:
    import jinja2
    import pdfkit
    from tkcalendar import DateEntry
except ImportError as error:
    print("Problemas na importação de algum(ns) (dos) módulo(s)!")
    print(error.__class__.__name__ + ": " + error.message)
except Exception as exception:
    print(exception.__class__.__name__+ ": " + exception.message)


class Print(object):
    TEMPLATES = os.path.join(os.path.dirname(__file__), 'Templates')
    
    IMAGENS = os.path.join(os.path.dirname(__file__), 'Imagens')
    if not os.path.exists(IMAGENS):
        os.makedirs(IMAGENS)

    _WKTHMLTOPDF_ = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    report_path = r'c:\temp'
    report_data = datetime.datetime.now().strftime('%Y_%m_%d')
    report_file_html = report_path + '\\HTMLReport_' + report_data + '.html'
    report_file_pdf = report_path + '\\PDFReport_' + report_data + '.pdf'
    options = {
        'quiet': '',
        'page-size': 'A4',
        'margin-top': '1.0cm',
        'margin-right': '1.5cm',
        'margin-bottom': '1.0cm',
        'margin-left': '1.5cm',
        'encoding': 'UTF-8',
    }

    def __init__(self, root, mmember, mfrequencia):
        self.toplevel = root
        self.toplevel.title('Impressão de Frequência(s)')
        self.modelmember = mmember()
        self.modelfrequencia = mfrequencia()

        self.TIPOPESQUISA = [
            ("Individual", "I"),
            ("Todos", "T")
        ]
        self.vPesquisa = StringVar()
        self.vPesquisa.set('T')
        self.mensagem = StringVar()

        self.comboCache = list()

        """Estilos"""
        style = ttk.Style()

        style.configure("PR.TLabel", padding=6, foreground="black", font=('helvetica', 9, 'bold'))
        style.configure("PR.TEntry", padding=6, background="#ccc", relief="flat")
        style.configure("PR.TButton", padding=6, relief="flat", background="#ccc")

        self.btnCancelImage = PhotoImage(file=self.IMAGENS + '\\cancel.png').subsample(3, 3)
        self.btnPrintImage = PhotoImage(file=self.IMAGENS + '\\iconfinder_document_print_118913.png').subsample(3, 3)

        self.formFrame = ttk.Frame(self.toplevel)
        self.formFrame.grid(column=0, row=0, padx=10, pady=10)

        self.formBotao = ttk.Frame(self.toplevel)
        self.formBotao.grid(column=0, row=2, padx=10, pady=10)

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.CreateGui()

    def image_file_path_to_base64_string(self, filepath: str) -> str:
        with open(filepath, 'rb') as f:
            return base64.b64encode(f.read()).decode()

    def CreateGui(self):
        self.createForm()
        self.createBotoes()


    def createForm(self):
        self.container1 = Frame(self.formFrame)
        self.container1['pady'] = 10
        self.container1.grid(row=0, column=0)
        self.lblInicial = ttk.Label(self.container1, style="PR.TLabel", text="Data Inicial:", width=12)
        self.lblInicial.pack(side=LEFT)
        self.dtaInicial = DateEntry(self.container1, width=11, background='darkblue', foreground='white', borderwidth=2,
                                    year=2019, locale='pt_BR', date_pattern='dd-MM-yyyy',state='readonly')
        self.dtaInicial.pack(side=LEFT, ipadx=25, padx=(10, 5))
        self.lblFinal = ttk.Label(self.container1, style="PR.TLabel", text="Data Final:", width=12)
        self.lblFinal.pack(side=LEFT)
        self.dtaFinal = DateEntry(self.container1, width=11, background='darkblue', foreground='white', borderwidth=2,
                                  year=2019, locale='pt_BR', date_pattern='dd-MM-yyyy',state='readonly')
        self.dtaFinal.pack(side=LEFT, ipadx=25, padx=(10, 5))

        """
         O combobox fica invisível caso o radiobutton 'todos' esteja ativado
         caso contrário mostra o combobox
        """
        self.container2_1 = Frame(self.formFrame)
        self.container2_1['pady'] = 10
        self.container2_1.grid(row=2, column=0)
        self.lbl = ttk.Label(self.container2_1, style="PR.TLabel", text="Membro:", width=12)
        self.lbl.pack(side=LEFT)
        self.cbxCombo = ttk.Combobox(self.container2_1, state='readonly', width=53)
        self.cbxCombo.pack(side=LEFT, ipadx=25, padx=(10, 5))
        self.preencherCombo()

    def createBotoes(self):
        self.container3 = Frame(self.formBotao)
        self.container3['pady'] = 10
        self.container3.grid(row=0, column=0)
        self.btnPrint = ttk.Button(self.container3, style="PR.TButton", compound=LEFT)
        self.btnPrint['text'] = 'Imprimir'
        self.btnPrint['width'] = 12
        self.btnPrint['command'] = self.print_relatorio
        self.btnPrint['image'] = self.btnPrintImage
        self.btnPrint.pack(side=LEFT, padx=10, pady=10)

        self.btnCancel = ttk.Button(self.container3, style="PR.TButton", compound=LEFT)
        self.btnCancel['text'] = 'Fechar'
        self.btnCancel['width'] = 12
        self.btnCancel['command'] = self.exitForm
        self.btnCancel['image'] = self.btnCancelImage
        self.btnCancel.pack(side=LEFT, padx=10, pady=10)

    def createMessage(self):
        self.container4 = Frame(self.frameMensagem)
        self.container4['pady'] = 10
        self.container4.grid(row=0, column=0)
        self.lblTipoPesq = ttk.Label(self.container4, style="PR.TLabel", textvariable=self.mensagem, width=100)
        self.lblTipoPesq.pack(side=LEFT)

    """Outras funções"""
    def exitForm(self):
        self.toplevel.destroy()

    # def verificaTipoImpressao(self):
    #     # tipoPesquisa = self.vPesquisa.get()
    #     # if tipoPesquisa == 'I':
    #         self.mensagem.set('')
    #         #Exibe o combobox
    #         self.cbxCombo.pack(side=LEFT)
    #         self.preencherCombo()
    #     # elif tipoPesquisa == 'T':
    #     #     self.mensagem.set('Será impressa a frequência de todos no período acima')
    #     #     self.cbxCombo.pack_forget()

    def preencherCombo(self):
        self.comboCache.clear() #limpa a lista
        for row in self.modelmember.getNames():
            self.comboCache.append(row[1])            #preenche a lista
            self.cbxCombo['values'] = self.comboCache #insere o retorno do bd no combo
            self.cbxCombo.current(0)

    def print_relatorio(self):
        """
            get() pega o que estiver no combo,
            já o select_get() pega o que for sendo selecionado
        """
        lista = list()
        selecao = self.cbxCombo.get()
        numcad = self.modelmember.getByNameID(selecao)
        for row in numcad:
            numcad = row[0]
        inicio = self.formataData(self.dtaInicial.get())
        fim = self.formataData(self.dtaFinal.get())
        frequenciaTotal = self.modelfrequencia.getTotalPresenca(numcad, inicio, fim)
        for row in frequenciaTotal:
            frequenciaTotal = row[0]
        totalFaltas = self.modelfrequencia.getTotalPresencaByTipo(numcad, inicio, fim, 'F')
        for row in totalFaltas:
            totalFaltas = row[0]
        totalPresenca = self.modelfrequencia.getTotalPresencaByTipo(numcad, inicio, fim, 'P')
        for row in totalPresenca:
            totalPresenca = row[0]
        totalJustificativa = self.modelfrequencia.getTotalPresencaByTipo(numcad, inicio, fim, 'J')
        for row in totalJustificativa:
            totalJustificativa = row[0]

        persons = [
            {'nome': selecao,
             'cadastro':numcad,
             'dtaInicial':inicio,
             'dtaFinal':fim,
             'total': frequenciaTotal,
             'falta': totalFaltas,
             'presenca':totalPresenca,
             'justificativa':totalJustificativa
             }]

        config = pdfkit.configuration(wkhtmltopdf=self._WKTHMLTOPDF_)
        file_loader = jinja2.FileSystemLoader(self.TEMPLATES)
        env = jinja2.Environment(loader=file_loader)
        template_report = env.get_template('report.html')
        content_report = 'REPORT: Elipse Plant Manager'
        html_report = template_report.render(content=content_report,
                                             img_string=self.image_file_path_to_base64_string(self.IMAGENS+'/simbolos-da-maconaria-6_xl.png'), persons=persons)

        # salva o relatório em html
        with open(self.report_file_html, 'w', encoding='utf-8') as html_file:
            html_file.write(html_report)

        # transforam html em pdf
        pdf_file = pdfkit.from_string(html_report, self.report_file_pdf, configuration=config, options=self.options,
                                      css=self.TEMPLATES+'/paper_pdf.css')
        if (pdf_file):
            webbrowser.open_new(self.report_file_pdf)
            


    def formataData(self, valor):
        """
        :param valor: passa o valor da data a ser formatada
        :return: data formatada
        """
        valoratual = valor.replace("-","")
        valoratual = '{4}{5}{6}{7}-{2}{3}-{0}{1}'.format(*valoratual)
        return valoratual
