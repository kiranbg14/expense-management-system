from fastapi import FastAPI ,HTTPException
from datetime import date
from typing import List
import db_helper
from pydantic import BaseModel

app=FastAPI()

class Expense_Group(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date : date
    end_date : date

class Year(BaseModel):
    year : int


#get request
@app.get('/expenses/{expense_date}',response_model=List[Expense_Group]) #to validate the response of list of category,amount,notes. we got list of expenses as ouptut
def get_expenses(expense_date: date): #date is type hint
    expenses = db_helper.get_expense_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail='Failed to retrieve expenses from database')
    return expenses

#post request
@app.post('/expenses/{expense_date}') #using post because we are inserting data from json format
def add_or_update_expense(expense_date: date,expenses:List[Expense_Group] ):#along with expense_date, passing list of expenses. we got list of expenses as input
    db_helper.delete_record(expense_date)   #before adding/updating delete the records for that expense_Date
    for expense in expenses:
        expenses = db_helper.insert_record(expense_date, expense.amount, expense.category, expense.notes)
    return {'message' : 'expenses updated successfully'}

#post request
@app.post('/analytics')
def get_analytics(data_range : DateRange):
    data = db_helper.fetch_expense_summary(data_range.start_date,data_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail='Failed to retrieve expense data from database')

    total = sum([row['total']for row in data])

    if total != 0:
        percentage = [(row['total']/total)*100 for row in data]
    else:
        percentage = [0 for _ in data]

    breakdown={}
    for i,row in enumerate(data):
        breakdown[row['category']] = {'total' : row['total'], 'percentage' : percentage[i]}

    return breakdown

#post request
@app.post('/analytics_by_months')
def get_expenses_by_month(year : Year):
    data = db_helper.fetch_summary_by_months(year.year)
    if data is None:
        raise HTTPException(status_code=500, detail='Failed to retrieve expense data from database')

    total = [row['amount'] for row in data]

    month = [row['month'] for row in data]

    return {"months": month, "totals": total}




