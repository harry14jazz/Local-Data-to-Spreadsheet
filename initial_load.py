from source import *
from decouple import config
import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = config('ssheet_id')
SAMPLE_RANGE_NAME = 'my-expenses!A1:F1'

if __name__ == "__main__":
    connecting = connect_to_mysql()
    curr = get_db_cursor(connecting)
    query = """
        SELECT id, name, price, id_category, id_sub_category, DATE_FORMAT(date_time, '%Y-%M-%e %H:%i:%s') as date_time 
        FROM my_expenses.expenses
        ORDER BY id ASC
    """
    data = []
    

    try:

        rows = curr.execute(query)
        row = curr.fetchall()
        for val in row:
            val = list(val)
            data.append(val)
        print('Data is ready')

        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()

        inserted = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values":data}).execute()

        print('Initial Load is Done')
    
    except ValueError:
        print('Error')