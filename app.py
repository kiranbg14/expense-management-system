import requests
import streamlit as st
import pandas as pd

API_URL = 'http://127.0.0.1:8000'   #running API from Gitbash because in pycharm running streamlit
#API_URL = 'http://localhost:8000'    #both are same

st.title('Expense Tracking System')

tab1, tab2 ,tab3 = st.tabs(['Add/Update','Analytics By Category','Analytics By Months'])

with tab1:
    date_format = st.date_input('Enter the Date:',label_visibility='collapsed')
    response = requests.get(f'{API_URL}/expenses/{date_format}') #get request
    if response.status_code == 200:
        existing_expense = response.json()
        #st.write(existing_expense)#st.table(existing_expense)
    else:
        st.error('failed to retrieve data')

    Categories=['Entertainment','Rent','Food','Shopping','Other','trekking','entertainment']
    
    with st.form(key='expense_form'): #form will have table and submit button and key used to uniquely identify the form
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text('Amount')
        with col2:
            st.text('Category')
        with col3:
            st.text('Notes')

        expenses = []
        for i in range(5): #to display only 5 rows in the frontend
            if i < len(existing_expense):
                amount = existing_expense[i]['amount']
                category = existing_expense[i]['category']
                notes = existing_expense[i]['notes']
            else:       #default values
                amount=0.0
                category='Shopping'
                notes=''

            col1,col2,col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(label='Amount', min_value=0.0, step=1.0, value=amount, key=f'amount_{date_format}_{i}',label_visibility='collapsed')
            with col2:
                category_input = st.selectbox(label='Category',options = Categories,index=Categories.index(category),key=f'category_{date_format}_{i}',label_visibility='collapsed')
            with col3:
                notes_input = st.text_input(label='Notes',value=str(notes),key=f'notes_{date_format}_{i}',label_visibility='collapsed')

            expenses.append({'amount': amount_input,'category': category_input,'notes': notes_input})

        submit_button = st.form_submit_button()
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount']>0]
            #st.write(filtered_expenses)
            response = requests.post(f'{API_URL}/expenses/{date_format}',json=filtered_expenses)
            if response.status_code == 200:
                st.success('Expenses updated successfully')
            else:
                st.error('failed to update data')

with tab2:
    col1,col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date')
    with col2:
        end_date = st.date_input('End Date')

    if st.button('Get Analytics'):
        payload = {
            'start_date' : start_date.strftime('%Y-%m-%d'),
            'end_date' : end_date.strftime('%Y-%m-%d')
        }
        response = requests.post(f'{API_URL}/analytics',json=payload)
        if response.status_code == 200:
            response = response.json()
        else:
            st.error('Failed to retrieve data')

        data = { 'Category' : list(response.keys()),
                 'Total' : [response[category]['total'] for category in response],
                 'Percentage' : [response[category]['percentage'] for category in response]
                 }
        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by='Percentage',ascending=False)

        st.bar_chart(data = df_sorted.set_index('Category')['Percentage'],width=0,use_container_width=True)

        df_sorted['Total'] = df_sorted['Total'].map('{:.2f}'.format)
        df_sorted['Percentage'] = df_sorted['Percentage'].map('{:.2f}'.format)

        st.table(df_sorted)

with tab3:
    st. title('Expense Breakdown by Months')

    year = int(st.number_input('Select Year',step=1))

    if st.button('Get Analytics by months'):
        payload = { 'year' : year}
        response = requests.post(f'{API_URL}/analytics_by_months',json = payload)

        if response.status_code == 200:
            response = response.json()
            months = response['months']
            total = response['totals']

            df = pd.DataFrame({'Months': months, 'Total': total})

            month_order = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]
            df['Months'] = pd.Categorical(df['Months'],categories=month_order, ordered=True)
            #'Categorical' is a special data type used to represent finite sets of values

            st.bar_chart(data = df.set_index('Months'),use_container_width=True)
            
            df['Total'] = df['Total'].map('{:.2f}'.format)
            st.table(df)
        else:
            st.error('Failed to retrieve data')








            

        
