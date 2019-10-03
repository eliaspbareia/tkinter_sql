import sqlite3

class MemberModel():
    db_filename = 'c:\programas\macom\database\macom.db'

    def __init__(self, memberid=0, membername=None, memberphone=None):
        self.memberid = memberid
        self.membername = membername
        self.memberphone = memberphone

        self.con = sqlite3.connect(self.db_filename)
        self.cur = self.con.cursor()


    def getAll(self):
        return self.cur.execute('SELECT * FROM member').fetchall()

    def getNames(self):
        return self.cur.execute('SELECT memberid, membername FROM member').fetchall()

    def getById(self, id):
        return self.cur.execute("SELECT * FROM member WHERE memberid = {}".format(id))

    def countRecord(self):
        return self.cur.execute("SELECT COUNT(*) FROM member WHERE memberid={}".format(self.memberid)).fetchone()[0]

    def getByName(self, name):
        return self.cur.execute("SELECT * FROM member WHERE membername LIKE '{}%'".format(name))

    def getByNameID(self, name):
        return self.cur.execute("SELECT memberid FROM member WHERE membername LIKE '{}%'".format(name))
    #https://gist.github.com/natorsc/81a15c001b7abd722dbb4da47bc89c93
    def save(self):
        try:
            query = "UPDATE member SET membername='{}', memberphone='{}' WHERE memberid= '{}'".format(self.membername, self.memberphone, self.memberid)
            self.cur.execute(query)
        except sqlite3.Error as e:
            return "Error: {}".format(e)
        else:
            self.con.commit()
            return 'Registro atualizado com sucesso.'


    def insert(self):
        try:
            if self.countRecord() == 1:
                return 'O número de cadastro já existe no banco de dados!'
            else:
                query = "INSERT INTO member(memberid, membername, memberphone) VALUES( {},'{}','{}')".format(self.memberid, self.membername, self.memberphone)
                self.cur.execute(query)
        except sqlite3.Error as e:
            return "Error: {}".format(e)
        else:
            self.con.commit()
            return 'Registro inserido com sucesso.'

    def delete(self, id):
        try:
            query = "DELETE FROM member WHERE memberid= {}".format(id)
            self.cur.execute(query)
        except sqlite3.Error as e:
            return "Error: {}".format(e)
        else:
            self.con.commit()
            return 'Registro excluído com sucesso.'
