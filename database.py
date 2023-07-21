import mysql.connector


mydb = mysql.connector.connect(
host='localhost',
user='library',
password='library@123',
database = 'library',
#port = 3306 #default mysql port
)
mycursor = mydb.cursor(buffered= True)


mycursor.execute('''CREATE TABLE IF NOT EXISTS USERDATA
(USERNAME varchar(255) NOT NULL,
PASSWORD varchar(255) NOT NULL,
BOOKS varchar(255) NOT NULL)
''')
# LAST_LOGIN varchar(255) NOT NULL,
# PUBLIC_KEY_N varchar(2000) NOT NULL,
# PUBLIC_KEY_E varchar(500) NOT NULL)
# print(222)
mycursor.execute('''CREATE TABLE IF NOT EXISTS BOOKS
(ID int NOT NULL AUTO_INCREMENT,
TITLE varchar(255) NOT NULL,
AUTHOR varchar(255) NOT NULL,
PRIMARY KEY (ID));
''')

