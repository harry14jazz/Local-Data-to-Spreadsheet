from source import *
from decouple import config

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

def connect_to_sheet(creds):
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        return sheet

    except HttpError as err:
        print(err)


def get_last_id_sheet(sheet, ssheet_id, range_cell):
    
    try:
        ## From this code below, this used for read the data in spreadsheet
        result = sheet.values().get(spreadsheetId=ssheet_id, range=range_cell).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        return values[-1][0]
    except HttpError as err:
        print(err)

def get_data(last_id):
    query = f"""
        SELECT id, name, price, id_category, id_sub_category, DATE_FORMAT(date_time, '%Y-%M-%e %H:%i:%s') as date_time
        FROM my_expenses.expenses
        WHERE id > {last_id}
    """
    connecting = connect_to_mysql()
    curr = get_db_cursor(connecting)

    data = []

    try:
        rows = curr.execute(query)
        row = curr.fetchall()
        for val in row:
            val = list(val)
            data.append(val)
        
        return data
    except ValueError:
        print('Error get data')

def append_to_sheet(sheet, ssheet_id, col_range, data):
    try:
        sheet.values().append(spreadsheetId=ssheet_id, range=col_range, valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values":data}).execute()
    except HttpError as err:
        print(err)

    return 'Daily load has done'




if __name__ == "__main__":
    # Define spreasheets, authentication, and sheet name with range
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    service_account_file = 'keys.json'

    credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes= scope)

    spreadsheet_id = config('ssheet_id')
    last_id_col = 'my-expenses!A:A'
    append_col = 'my-expenses!A1:F1'

    # Connect to sheet
    sheet = connect_to_sheet(credentials)

    # Get last Id from the expenses sheet
    last_id = get_last_id_sheet(sheet, spreadsheet_id, last_id_col)

    # Get data from local expenses db where the id is after last id
    insert_data = get_data(last_id)
    
    # Append data to spreadsheet
    result = append_to_sheet(sheet, spreadsheet_id, append_col, insert_data)
    print(result)

