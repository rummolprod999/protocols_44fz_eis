import pymysql

if __name__ == "__main__":
    print('Привет, этот файл только для импортирования!')


def connect_bd_localhost(baza):
    con = pymysql.connect(host="localhost", user="test", passwd="*********", db=baza, charset='utf8',
                          init_command='SET NAMES UTF8', cursorclass=pymysql.cursors.DictCursor, autocommit=True)
    return con


def connect_bd(baza):
    con = pymysql.connect(host="localhost", port=3306, user="parser", passwd="Dft56Point", db=baza, charset='utf8',
                          init_command='SET NAMES UTF8', cursorclass=pymysql.cursors.DictCursor, autocommit=True)
    return con
