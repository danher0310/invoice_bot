from DatabaseManagerClass import DatabaseManager
from datetime import datetime

class Payment:
  def __init__(self, provider_id, reference, invoice_id, amount, date):
    self.invoice_id = provider_id
    self.reference = reference
    self.invoices_id = invoice_id
    self.amount = amount
    self.date = date
    

  def register_payment(self):
    # register payment in database
    mydb =DatabaseManager()
    mydb.connect()
    register = mydb.execute_query("insert into payments (reference_number, payment_date, amount) values (%s, %s, %s)", (self.reference, self.date, self.amount))
    print(register)
    
    
now = datetime.now().strftime("%Y-%m-%d")
test = Payment(5, 'Test_register#1', [2,3,4], 1800, now )
test.register_payment()

    
    

    
  
    
    
  
  
    
    
    
    
    
    
    