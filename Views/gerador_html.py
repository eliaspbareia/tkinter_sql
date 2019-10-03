import webbrowser
import base64
import datetime

try:
    import jinja2
    import pdfkit
except ImportError as error:
    print("Problemas na importação de algum(ns) (dos) módulo(s)!")
    print(error.__class__.__name__ + ": " + error.message)
except Exception as exception:
    print(exception.__class__.__name__+ ": " + exception.message)


def image_file_path_to_base64_string(filepath: str) -> str:
    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read()).decode()

_WKTHMLTOPDF_ = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
report_path = r'c:\temp'
report_data = datetime.datetime.now().strftime('%Y_%m_%d')
report_file_html = report_path + '\\HTMLReport_'+report_data+'.html'
report_file_pdf = report_path+ '\\PDFReport_'+report_data+'.pdf'
options = {
    'quiet':'',
    'page-size': 'A4',
    'margin-top': '1.0cm',
    'margin-right': '1.5cm',
    'margin-bottom': '1.0cm',
    'margin-left': '1.5cm',
    'encoding': 'UTF-8',
}
config = pdfkit.configuration(wkhtmltopdf=_WKTHMLTOPDF_)
file_loader = jinja2.FileSystemLoader('Templates')
env = jinja2.Environment(loader=file_loader)
template_report = env.get_template('report.html')
content_report = 'REPORT: Elipse Plant Manager'
html_report = template_report.render(content=content_report,
                                     img_string =image_file_path_to_base64_string('imagens/maconaria.png'))

#salva o relatório em html
with open(report_file_html, 'w', encoding='utf-8') as html_file:
    html_file.write(html_report)

#transforam html em pdf
pdf_file = pdfkit.from_string(html_report, report_file_pdf, configuration=config, options=options, css='Templates/paper_pdf.css')
if (pdf_file):
    print(f'Relatório gerado com sucesso.')

