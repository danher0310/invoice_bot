import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()
#Clase tu manage all function of the databae
class DatabaseManager:
  def __init__(self):
    self.host = os.getenv('dbhost')
    self.user = os.getenv('dbuser')
    self.password = os.getenv('dbpass')   
    self.database = os.getenv('database')
    #self.initials = initials
    self.connection = None
    self.cursor = None
    
  def connect(self):
    #Conection tu database
    self.connection = mysql.connector.connect(
      host = self.host,
      user = self.user,
      password = self.password,
      database = self.database
    )
    self.cursor = self.connection.cursor()
    
  #   if self.database is None:
  #     self.create_database()
  #     self.use_database()
  #     self.create_table()
  #     self.close()
  #   else:
  #     self.use_database()
      
      
  # def create_database(self):
  #   #creation of database
  #   self.cursor.execute(f"CREATE DATABASE {self.initials}_database")
  #   print(f"Base de datos '{self.initials}_database' creada o ya existe.")
  #   self.database = f"{self.initials}_database"
  #   self.use_database
    
  # def use_database(self):
  #   self.cursor.execute(f"USE {self.database}")
    
  # def create_table(self):
  #   try:
  #     self.cursor.execute('''
  #         CREATE TABLE IF NOT EXISTS invoices (
  #           id bigint primary key unique auto_increment not null,
  #           invoice_number text not null,
  #           creation_date timestamp not null default now(),
  #           amount numeric(10, 2) not null,
  #           description text
  #         );
  #         CREATE TABLE IF NOT EXISTS payments (
  #           id bigint primary key unique auto_increment not null,
  #           reference_number text,
  #           payment_date timestamp not null default now(),
  #           amount numeric(10, 2) not null
  #         );
  #         CREATE TABLE IF NOT EXISTS invoice_payments (
  #           id bigint primary key unique auto_increment not null,
  #           invoice_id bigint not null references invoices (id),
  #           payment_id bigint not null references payments (id),
  #           amount numeric(10, 2) not null
  #         );       
          
  #         ''')
  #     print("Tabla 'usuarios' creada o ya existe.")
      
  #   except mysql.connector.Error as err:
  #     print(err)
  #     self.close()
  #     return  False
      
    
  def execute_query(self, query, params=None):
    try:
      self.cursor.execute(query, params)
      
      if query.strip().lower().startswith("select"):
        return self.cursor.fetchall()      
      else:
        self.connection.commit()
        return self.cursor.lastrowid
      
      
    except mysql.connector.Error as err:
      print(err)
      self.close()
      return  False

   
    
    
  def close(self):
    if self.cursor:
        self.cursor.close()
    if self.connection:
        self.connection.close()
    print("Conection close.")
    
  
# db_test = DatabaseManager( '', 'invoices' )




# db_test.connect()
# check = db_test.exceute_query("update invoices set invoice_number = %s, amount = %s, description = %s where id = %s ", ('INV-021', 1700.00, 'Software development services', 21))
# print(check)
# #print(len(check))
# db_test.close()

    
    
    
    
    
    
  