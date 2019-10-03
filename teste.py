# from Models.MemberModel import MemberModel as mmember
# members = mmember()
# # lista = members.getAll()
# #
# # print(lista)
# members.memberid = 2095
# row = members.countRecord()
#
# for r in row:
#
#     if len(r) > 0:
#         print('Membro já cadastrado')
#     else:
#         print('Membro não cadastrado')
#
# from Models.FrequenciaModel import FrequenciaModel as modelo
#
# modelo = modelo()
# modelo.num_cadastro = 2095
# lista = modelo.getmember()
# print(lista)

# import sqlite3
# import os.path
# connection = sqlite3.connect('config.db')
# c = connection.cursor()
#
# def create_table():
#     c.execute('CREATE TABLE IF NOT EXISTS VideoCapture (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, value text)')
#     sql = 'SELECT * FROM VideoCapture WHERE name = ?'
#     search = 'NumCam'
#     status = 0
#     for row in c.execute(sql, (search,)):
#         status = 1
#     else:
#         if status == 1:
#         print('Ja cadstrado')
#     else:
#         c.execute("INSERT INTO VideoCapture(name, value) VALUES('NumCam', 4)")

# from reportlab.pdfgen import canvas
# #http://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/
# def GeneratePDF(lista):
#     try:
#         nome_pdf = input('Informe o nome do PDF')
#         pdf = canvas.Canvas('{}'.format(nome_pdf))
#         x = 720
#         for nome, idade in lista.items():
#             x -= 20
#             pdf.drawString(247, x, '{} : {}'.format(nome, idade))
#             pdf.setTitle(nome_pdf)
#             pdf.setFont("Helvetica-Oblique", 14)
#             pdf.drawString(245, 750, 'Lista de Convidados')
#             pdf.setFont("Helvetica-Bold", 12)
#             pdf.drawString(245, 724, 'Nome e Idade')
#             pdf.save()
#             print('{}.pdf criado com sucesso'.format(nome_pdf))
#     except :
#         print('Erro ao gerar {}.pdf'.format(nome_pdf))
#
#
#
# lista = {'Rafaela': '19', 'Jose': '15', 'Maria': '22','Eduardo':'24'}
# GeneratePDF(lista)

import sqlite3
import os

db_filename = 'c:\programas\macom\database\macom.db'
connection = sqlite3.connect(db_filename)
cursor = connection.cursor()
rows = cursor.execute("SELECT * FROM frequencia WHERE reuniao BETWEEN '2019-09-01' AND '2019-09-30'").fetchall()
for row in rows:
    print(row[0], row[1], row[2], row[3], row[4])
    # dia, mes, ano = row[2].split('/')
    # if mes == '09':
    #     print(mes)




