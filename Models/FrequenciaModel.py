import sqlite3
import json

class FrequenciaModel:

    db_filename = 'c:\programas\macom\database\macom.db'

    def __init__(self, id=0, cadastro=0, reuniao=None, presenca=None, ano=0):
        self.id = id
        self.num_cadastro = cadastro
        self.data_reuniao = reuniao
        self.presenca = presenca
        self.ano = ano


        self.conn = sqlite3.connect(self.db_filename)
        self.cursor = self.conn.cursor()

    def getmember(self):
        try:
            return self.cursor.execute("select idfrequencia, reuniao, presenca from frequencia where cadastro = {} and ano = {} ORDER BY reuniao".format(*[self.num_cadastro,self.ano])).fetchall()
        except sqlite3.Error as e:
            return "Error: {}".format(e)

    def getById(self, id):
        return self.cursor.execute("SELECT * FROM frequencia WHERE idfrequencia = {} ".format(id))

    # def getByPeriodoAll(self, dtainicial, dtafinal):
    #     """
    #     :param cadnum: número do cadastro
    #     :param dtainicial:  data inicial para fins de pesquisa
    #     :param dtafinal:    data final para fins de pesquisa
    #     :return: retorna a pesquisa
    #     """
    #     #SELECT * FROM frequencia WHERE reuniao BETWEEN '2019-09-01' AND '2019-09-30'"
    #     self.cursor.execute("SELECT * FROM frequencia WHERE reuniao BETWEEN '{}' AND '{}'".format(dtainicial, dtafinal))
    #     rows_headers = [x[0] for x in self.cursor.description]
    #     rows = self.cursor.fetchall()
    #     json_list = []
    #     for row in rows:
    #         json_list.append(dict(zip(rows_headers, row)))
    #     #self.cursor.close()
    #     return json.dumps({'items':json_list}, indent=4)

    def getTotalPresencaByTipo(self,numcad, dtainicial, dtafinal, tipopresenca):
        return self.cursor.execute("SELECT COUNT(presenca) FROM frequencia WHERE cadastro = {} AND presenca = '{}' AND reuniao BETWEEN '{}' AND '{}'".format(numcad, tipopresenca, dtainicial, dtafinal))

    def getTotalPresenca(self,numcad, dtainicial, dtafinal):
        return self.cursor.execute("SELECT COUNT(presenca) FROM frequencia WHERE cadastro = {} AND reuniao BETWEEN '{}' AND '{}'".format(numcad, dtainicial, dtafinal))

    # def getByPeriodoId(self, numcad, dtainicial, dtafinal):
    #     totalfrequencia = self.cursor.execute("select count(presenca) from frequencia WHERE cadastro = {} AND reuniao BETWEEN '{}' AND '{}'".format(numcad, dtainicial, dtafinal))
    #
    #     self.cursor.execute("SELECT * FROM frequencia WHERE cadastro = {} AND reuniao BETWEEN '{}' AND '{}'".format(numcad, dtainicial, dtafinal))
    #     rows_headers = [x[0] for x in self.cursor.description]
    #     rows = self.cursor.fetchall()
    #     json_list = []
    #     for row in rows:
    #         json_list.append(dict(zip(rows_headers, row)))
    #
    #     return json.dumps({'cadastro': numcad, 'totalfrequencia': totalfrequencia, 'datainicial': dtainicial, 'datafinal': dtafinal}, indent=4)

    def delete(self, id):
        try:
            query = "DELETE FROM frequencia WHERE idfrequencia= {}".format(id)
            self.cursor.execute(query)
        except sqlite3.Error as e:
            return "Error: {}".format(e)
        else:
            self.conn.commit()
            return 'Registro excluído com sucesso.'

    def savefrequencia(self, operacao):
        if operacao == 'Novo':
            try:
                query = "INSERT INTO frequencia(cadastro, reuniao, presenca, ano) VALUES( {},date('now'),'{}',{})".format(self.num_cadastro, self.presenca, self.ano)
                self.cursor.execute(query)
            except sqlite3.Error as e:
                return "Error: {}".format(e)
            else:
                self.conn.commit()
                return 'Registro inserido com sucesso.'
        else:
            try:
                query = "UPDATE frequencia SET cadastro={}, reuniao='{}', presenca='{}', ano ={} WHERE idfrequencia= '{}'".format(self.num_cadastro, self.data_reuniao, self.presenca, self.ano, self.id)
                self.cursor.execute(query)
            except sqlite3.Error as e:
                return "Error: {}".format(e)
            else:
                self.conn.commit()
                return 'Registro atualizado com sucesso.'

