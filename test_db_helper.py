from backend import db_helper

def test_get_expense_date_valid():
    expenses=db_helper.get_expense_date('2026-02-15')
    #print(expenses)     #{'id': 77, 'expense_date': datetime.date(2026, 2, 15), 'amount': 400.0, 'category': 'Entertainment', 'notes': 'Fueling'}
    assert expenses[0]['amount'] == 400
    assert len(expenses)  == 1
    assert expenses[0]['category']   == 'Entertainment'

def test_get_expense_date_invalid():
    expenses=db_helper.get_expense_date('2999-02-15')
    assert len(expenses)  == 0

def test_fetch_expense_summary_invalid_range():
    summary=db_helper.insert_record('2099-08-01','2099-08-05')
    assert len(summary) == 0


