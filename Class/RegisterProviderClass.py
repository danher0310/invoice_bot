
from DatabaseManagerClass import DatabaseManager
from dotenv import load_dotenv


class ProviderRegister:
  
  def __init__(self,  name, address, phone, account, invoice_default, chat_id, frequency, days):
    self.name = name
    self. address = address
    self.phone = phone
    self.account = account
    self.invoice_default = invoice_default
    self.chat_id = chat_id
    self.frequency = frequency
    self.days = days
    self.initials = self.build_initials()
    
    
  def build_initials(self):
    split_name = self.name.split()
    initials = ''.join([initial[0].upper() for initial in split_name])
    return initials
  
  def register_provider(self):    
    
    myDB = DatabaseManager()
    myDB.connect()
    check_providers =  myDB.execute_query("select name from providers where name = %s", (self.name, ) )
    if (len(check_providers) == 0): 
      register = myDB.execute_query("insert into providers (name, address, phone, account, invoice_default, initials, chat_id, frequency, days) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.name, self.address, self.phone, self.account,  self.invoice_default, self.initials, self.chat_id, self.frequency, self.days))    
      if(register):
        print(register)
        myDB.close()
        return "Provider was register successfully"
      else:
        myDB.close()
        return "We have a error please check the information"
    else: 
      return "This provider exists"
      
    
  # def create_provider_sql_structure(self):
  #   sqlStructrure = DatabaseManager(self.initials)
  #   sqlStructrure.connect()
  #   sqlStructrure.close()    
    


    
    
    
    
    
    
    
    
    
    
  


test = ProviderRegister("Katie Santos", 'collage park', '+18281782', 10, 4050, '-182881818', 'Monthly', ("8"))
test.register_provider()
#test.create_provider_sql_structure()

# db_test = DatabaseManager( '', 'invoices' )

# db_test.connect()
# check = db_test.exceute_query("update invoices set invoice_number = %s, amount = %s, description = %s where id = %s ", ('INV-021', 5700.00, 'Software development services monthly', 21))
# print(check)
# #print(len(check))
# db_test.close()



    