import mysql.connector
from contextlib import contextmanager
from logging_set_up import setup_loggers

loger = setup_loggers('db_helper','my_connect.log')

@contextmanager
def get_db_cursor(commit = False):
    connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'expense_manager'
    )

    if connection.is_connected():
        print('connection is successful')
    else:
        print('connection failed')

    cursor=connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_all_records():  #Retrieve
    with get_db_cursor() as cursor:
        cursor.execute('select * from expense_manager.expenses')
        expenses=cursor.fetchall()
        for expense in expenses:
            print(expense)

def get_expense_date(expense_date):  #Retrieve
    loger.info(f'This function fetch expenses for the date : {expense_date}')     #logging
    with get_db_cursor() as cursor:
        cursor.execute('select * from expense_manager.expenses where expense_date = %s',(expense_date,))
        expenses=cursor.fetchall()
        return expenses
        for expense in expenses:
            print(expense)

def insert_record(expense_date, amount, category, notes):  #Insert
    loger.info(f'This function inserts data to expenses table for the date : {expense_date}')  # logging
    with get_db_cursor(commit = True) as cursor:
        cursor.execute('insert into expense_manager.expenses (expense_date, amount, category, notes) values (%s,%s,%s,%s)',(expense_date, amount, category, notes))

def delete_record(expense_date):  #Delete
    loger.info(f'This function deletes data from expenses table for the date : {expense_date}')  # logging
    with get_db_cursor(commit = True) as cursor:
        cursor.execute('delete from expense_manager.expenses where expense_date = %s',(expense_date,))

def fetch_expense_summary(start_date,end_date):
    loger.info(f'This function fetches data from expenses table for the date  between: {start_date} and {end_date}')  # logging
    with get_db_cursor() as cursor:
        cursor.execute('select category, sum(amount) total from expense_manager.expenses where expense_date '
                       'between %s and %s group by category',(start_date,end_date) )
        summary=cursor.fetchall()
        return summary
        for record in summary:
            print(record)

def fetch_summary_by_months(year):
    loger.info(f'This function fetches data from expense table by the year - month wise breakdown')
    with get_db_cursor() as cursor:
        cursor.execute("SELECT sum(amount) amount,date_format(expense_date,'%M') month FROM expense_manager.expenses where year(expense_date) = %s group by date_format(expense_date,'%M')",(year,))
        summary=cursor.fetchall()
        print(summary)
        return summary



if __name__=='__main__':
    #fetch_all_records()
    #get_expense_date('2024-08-02')
    #insert_record('2026-02-15',400,'Entertainment','Fueling')
    #delete_record('2026-02-15')
    #fetch_expense_summary('2024-08-01','2024-08-05')
    fetch_summary_by_months(2024)



