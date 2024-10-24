import jinja2
import pdfkit
from datetime import datetime
import os
from DatabaseManagerClass import DatabaseManager
from os import  makedirs
from dotenv import load_dotenv
import re
# C:\Program Files\wkhtmltox\bin

load_dotenv()



class CreateInvoice:
  def __init__(self, data):
    self.provider_id = data[0]
    self.provider_name = data[1]
    self.provider_address = data[2]
    self.provider_phone = data[3]
    self.account = data[4]
    self.invoice_default = data[5]
    self.description = data[6]
    self.language = data[7]    
    self.chat_id = data[8]
    self.amount = data[9]
    self.balance = data[10]
    self.initials = data[11]
    self.path = None    
    
           
    
    
    
  
  def print_invoice(self):
    now = datetime.now()
    if (self.language == 'english'):
      date_format = now.strftime("%m/%d/%Y")  
    else:
      date_format = now.strftime("%d/%m/%Y") 
    invoice_number = self.check_invoice_number()
       
    invoice_data = { 
      'dates' : date_format,
      'name' : self.provider_name,
      'invoiceN' : invoice_number,
      'address' : self.provider_address,
      'phone' : self.provider_phone,
      'account' : self.account,
      'description' :self.description, 
      'price' : self.amount,
      'balance': self.balance,
      
      
      
      
    }
    clean_amount = float(re.sub(r'[^\d.]', '', self.amount ))
    template_loader = jinja2.FileSystemLoader(r'D:\projects\all-python\bots\actual reports\Invoice_bot\template')
    template_env = jinja2.Environment(loader=template_loader)
    folder = f"{os.getenv('path_saving')}{os.sep}{self.initials}"
    makedirs(folder, exist_ok=True)
    path_saving = (f'{folder}{os.sep}Invoice_{self.provider_name}_{now.strftime("%m-%d-%Y") }.pdf')
    if not os.path.exists(path_saving):
    
      template = template_env.get_template("eng_invoices.html")
      output_text = template.render(invoice_data)
      config = pdfkit.configuration(wkhtmltopdf=r"D:\projects\all-python\bots\actual reports\Invoice_bot\tools\wkhtmltox\bin\wkhtmltopdf.exe") 
    try:
      if pdfkit.from_string(output_text, path_saving, configuration=config, css=r'D:\projects\all-python\bots\actual reports\Invoice_bot\template\assets\css\index.css', options={"enable-local-file-access": ""}):
        if self.insert_invoice(invoice_number, clean_amount, self.description, self.provider_id):
          return path_saving
        else:
          return "Sorry, but the invoice has some error, please contact to administrator"
      else:
        return "Sorry, but this invoice was already processed today. Try again tomorrow."
    except:
      return "Sorry, but the invoice has some error, please contact to administrator"
               
    
    
    
  def check_invoice_number(self):
    mydb = DatabaseManager()
    mydb.connect()
    check_invoice = mydb.execute_query("SELECT invoice_number from  invoices  where provider_id =%s order by invoice_number DESC", (self.provider_id,))
    mydb.close()
    if len(check_invoice)>0:
      return int(check_invoice[0][0])+1
    else:
      return self.invoice_default
    
  def insert_invoice(self, invoice_number,  amount, description, provider_id ):
    mydb = DatabaseManager()
    mydb.connect()
    register_invoice = mydb.execute_query("insert into invoices (invoice_number, amount, description, provider_id) values(%s, %s, %s, %s)", ( invoice_number,  amount, description, provider_id))
    if(register_invoice):
      mydb.close()
      return "Provider was register successfully"
    else:
      mydb.close()
      return "We have a error please check the information"
    
    
    
    
    
    
# test = CreateInvoice([2, "Cathy's Cleanning Services", 'collage park', '+18281782', '10', 300, '-182881818'])
# print(test.check_invoice_number())


    
   