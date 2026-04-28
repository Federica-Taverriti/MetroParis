from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def hasconn(u: Fermata, v: Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c WHERE c.id_stazP = %s and c.id_stazA = %s"
        cursor.execute(query, (u.id_fermata, v.id_fermata)) #serve solo id_fermata, altrimenti si passa la dataclass

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result) > 0 #se maggiore return True, boolean

    @staticmethod
    def getvicini(u: Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c WHERE c.id_stazP = %s"
        cursor.execute(query, (u.id_fermata,)) #query da tutte connessioni (vicini) da stazione di partenza

        for row in cursor:
            result.append(Connessione(**row)) #creiamo dataclass di tipo "Connessione" nel modello, perchè ritorna informazioni delle connessioni
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c"
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

