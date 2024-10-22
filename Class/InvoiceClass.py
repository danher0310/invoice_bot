import jinja2
import pdfkit
from datetime import datetime
import os
from DatabaseManagerClass import DatabaseManager
# C:\Program Files\wkhtmltox\bin


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
    self.path = None    
    
           
    
    
    
  
  def print_invoice(self):
    now = datetime.now()
    if (self.language == 'english'):
      date_format = now.strftime("%m/%d/%Y")  
    else:
      date_format = now.strftime("%d/%m/%Y") 
       
    invoice_data = { 
      'dates' : date_format,
      'name' : self.provider_name,
      'invoiceN' : self.check_invoice_number(),
      'address' : self.provider_address,
      'phone' : self.provider_phone,
      'account' : self.account,
      'description' :self.description, 
      'price' : self.amount,
      'balance': self.balance
      
      
      
    }
    
    template_loader = jinja2.FileSystemLoader(r'D:\projects\all-python\bots\actual reports\Invoice_bot\template')
    template_env = jinja2.Environment(loader=template_loader)
    
    path_saving = (f'D:\\projects\\all-python\\bots\\actual reports\\Invoice_bot\\invoices\\test_invoice_{self.provider_name}.pdf')
    if not os.path.exists(path_saving):
    
      template = template_env.get_template("eng_invoices.html")
      output_text = template.render(invoice_data)
      config = pdfkit.configuration(wkhtmltopdf=r"D:\projects\all-python\bots\actual reports\Invoice_bot\tools\wkhtmltox\bin\wkhtmltopdf.exe")    
               
    if pdfkit.from_string(output_text, path_saving, configuration=config, css=r'D:\projects\all-python\bots\actual reports\Invoice_bot\template\assets\css\index.css', options={"enable-local-file-access": ""}):
      print(path_saving)
      return path_saving
    
    
  def check_invoice_number(self):
    mydb = DatabaseManager()
    mydb.connect()
    check_invoice = mydb.execute_query("SELECT invoice_number from  invoices  where provider_id =%s order by invoice_number DESC", (self.provider_id,))
    
    if len(check_invoice)>0:
      return int(check_invoice[0][0])+1
    else:
      return self.invoice_default
    
    
    
    
    
# test = CreateInvoice([2, "Cathy's Cleanning Services", 'collage park', '+18281782', '10', 300, '-182881818'])
# print(test.check_invoice_number())


    
   