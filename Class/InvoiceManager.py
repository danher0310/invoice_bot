
from datetime import datetime
from DatabaseManagerClass import DatabaseManager
from InvoiceClass import CreateInvoice
from datetime import datetime
from dateutil.relativedelta import relativedelta
import babel.numbers

class InvoiceManager:
  
  def __init__(self):
    self.week_day = self.weekDay()
    self.date_number = 8
    
  def weekDay(self):
    day_name = datetime.now().isoweekday()
    return day_name

  def date(self):
    date_number = datetime.now().day
    return date_number  
    
  def check_weekly_invoices(self):
    myDB = DatabaseManager()
    myDB.connect()    
    sql = "SELECT id, name, address, phone, account, invoice_default, chat_id from providers where frequency = %s and days like %s"
    params = ('weekly',f'%{self.week_day}%' )
    checker  = myDB.execute_query(sql, params)
    if (len(checker) > 0):
      for data in checker:
        provider_id = data[0]
        provider_client = data[1]
        provider_address = data[2]
        provider_phone = data[3]
        account = data[4]
        invoice_default = data[5]
        chat_id = data[6]
        
        
        provider_data = (provider_id, provider_client, provider_address, provider_phone, account, invoice_default, chat_id   )
        print(provider_data)
    myDB.close()
        
  def check_fortnightly_invoices(self):
    myDB = DatabaseManager()
    myDB.connect()    
    sql = "SELECT id, name, address, phone, account, invoice_default, chat_id from providers where frequency = %s and days like %s"
    params = ('fortnightly',f'%{self.date_number}%')
    checker  = myDB.execute_query(sql, params)
    if (len(checker) > 0):
      for data in checker:
        provider_id = data[0]
        provider_name = data[1]
        provider_address = data[2]
        provider_phone = data[3]
        account = data[4]
        invoice_default = data[5]
        chat_id = data[6]        
        provider_data = (provider_id, provider_name, provider_address, provider_phone, account, invoice_default, chat_id  )
        test = CreateInvoice(list(provider_data))
        test.print_invoice()
        print(list(provider_data))
    myDB.close()
    
  def check_monthly_invoices(self):
    myDB = DatabaseManager()
    myDB.connect()    
    sql = "SELECT id, name, address, phone, account, invoice_default, format, dates_show, chat_id, description, languages, amount  from providers where frequency = %s and days like %s"
    params = ('monthly',f'%{self.date_number}%')
    checker  = myDB.execute_query(sql, params)
    if (len(checker) > 0):
      for data in checker:
        provider_id = data[0]
        provider_name = data[1]
        provider_address = data[2]
        provider_phone = data[3]
        account = data[4]
        invoice_default = data[5]
        form = data[6]        
        day_show = (data[7])
        chat_id = data[8]
        description = data[9]
        language = data[10]
        amount = babel.numbers.format_currency(data[11] , "USD")
        
        if (form == 'days'):
          day_show = list(day_show.replace(",", ""))
          description += self.build_days_desctiption(day_show, language)
        elif (form == 'actual'):
          description +=self.build_month_description(language)          

        balance = self.build_balance( provider_id, provider_name, 30)
        
        if balance != None:
          balance = balance
        else:
          balance = []
        
        
        test_data = (provider_id, provider_name, provider_address, provider_phone, account, invoice_default, form, day_show, description, language, chat_id, amount  )
        provider_data = (provider_id, provider_name, provider_address, provider_phone, account, invoice_default, description, language, chat_id, amount, balance  )   
        #print(test_data)      
        test = CreateInvoice(list(provider_data))
        test.print_invoice()
        
    myDB.close()
    
  def build_days_desctiption (self, days, language):
    now = datetime.now()
    month = now.month
    year = now.year    
    day_start = days[0]
    day_end  = days[1]    
    if language == 'english':      
      date_start = datetime.strptime(f'{month-1}/{day_start}/{year}', '%m/%d/%Y').strftime("%m/%d/%Y")
      date_end = datetime.strptime(f'{month}/{day_end}/{year}', '%m/%d/%Y').strftime("%m/%d/%Y")
    else:
      date_start = datetime.strptime(f'{day_start}/{month -1}/{year}', '%d/%m/%Y').strftime("%d/%m/%Y")
      date_end = datetime.strptime(f'{day_end}/{month}/{year}', '%d/%m/%Y').strftime("%d/%m/%Y")
    
    return f" {date_start} - {date_end}"  
    
  def build_month_description(self, language):
    now = datetime.now()
    year = now.year   
    if language == 'english': 
      month = now.strftime("%B") 
      return f" {month} {year}"
    else:
      month = now.month
      
      spanish_dict = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Deciembre"
      }
      return f" {spanish_dict[month]} {year}"
      
      
  def check_balance(self, id):
    myDB = DatabaseManager()
    myDB.connect()    
    sql = "SELECT creation_date, description, SUM(amount) OVER(ORDER BY id asc ) AS cumulative_sum, amount  FROM invoices WHERE provider_id = %s and status is NULL or status != 'paid' ORDER BY id desc limit 3"
    params = (id,)
    checker_balance  = myDB.execute_query(sql, params)
    myDB.close()
    return checker_balance
   
    
  def check_payments(self, day, provider_name, difference):
    date1 = day.strftime("%Y-%m-%d")
    date2 = (day - relativedelta(days=difference)).strftime("%Y-%m-%d")
    myDB = DatabaseManager()
    myDB.connect()
    sql = 'SELECT SUM(pay.amount) OVER (PARTITION BY p.id) AS total_payments FROM  providers p JOIN invoices i ON p.id = i.provider_id JOIN invoice_payments ip ON i.id = ip.invoice_id JOIN payments pay ON ip.payment_id = pay.id WHERE p.name = %s and pay.payment_date between %s and %s ORDER BY pay.payment_date DESC LIMIT 1;'
    params = (provider_name, f"{date2} 00:00:00", f"{date1} 23:59:59")
    checker_payment  = myDB.execute_query(sql, params)
    myDB.close()
    if len(checker_payment) > 0:      
      return checker_payment[0][0]
    else: 
      return 0
    
    
    
  def build_balance(self, provider_id, provider_name, difference):
    balances =  self.check_balance(provider_id)
    table =  []
    if len(balances) > 0:
      row =  []
      old_payment = 0
      for balance in balances:            
        payment = self.check_payments(balance[0], provider_name, 30)           
        date_invoice = balance[0].strftime("%m/%d/%Y")             
        description = balance[1]
        charge = balance[3]
        
        if len(table) == 0:
          previous = balance[2] - balance[3] + payment
          total_debt = balance[2]
        else: 
          previous = (previous - balance[3]) + (payment)
          total_debt = balance[2] + old_payment
          
        row = date_invoice, description, babel.numbers.format_currency(previous, "USD"), babel.numbers.format_currency(charge, "USD"), babel.numbers.format_currency(payment, "USD"), babel.numbers.format_currency(total_debt, "USD")
        previous = previous
        old_payment += payment                      
        table.append(list(row))  
      print(list(reversed(table)))  
        
       
      return list(reversed(table))

    else:
      return None
    
    
    
 
    
  
  
        
        
       
    
    
    
    
    
  
  # def test(self):
  #   print(self.week_day, self.date_number)
  
test = InvoiceManager()
test.check_monthly_invoices()



