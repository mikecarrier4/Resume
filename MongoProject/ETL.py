"""ETL import sqlite to MongoDB"""
import sqlite3
import ssl
import pymongo
import SQL
#TODO move Password and DBNAME
PASSWORD = "jy5HOmo6e5ya4ENn"
DBNAME = "test"

def pymongo_conn(Password, Dbname):
    client = pymongo.MongoClient("mongodb+srv://new_user_1:{}@cluster0.ybyix.mongodb.net/{}?retryWrites=true&w=majority".format(Password, Dbname),ssl=True, ssl_cert_reqs=ssl.CERT_NONE )
    return client


def sqlite_conn(extraction_db = 'rpg_db.sqlite3'):
    sl_conn = sqlite3.connect(extraction_db)
    return sl_conn


def execute_query(curs, query):
    return curs.execute(query).fetchall()

"""Template for flat file"""
def character_doc_create(mongo_db, character_table):
    """character = {id, name, level, exp, hp, strength, intelligence, dexterity, wisdom}"""
    for character in character_table:
        character_doc = {
            "name": character[1],
            "level": character[2],
            "exp": character[3],
            "hp": character[4],
            'strength': character[5],
            "intelligence": character[6],
            "dexterity": character[7],
            "wisdom" : character[8],

        }
        mongo_db.rpg.insert_one(character_doc)


if __name__ == "__main__":
    sl_conn = sqlite_conn()
    sl_curs = sl_conn.cursor()
    client = pymongo_conn(PASSWORD, DBNAME)
    db = client.rpg
    characters = execute_query(sl_curs, SQL.GET_CHARACTERS)
    character_doc_create(db, characters)
    print(list(db.rpg.find()))
    

