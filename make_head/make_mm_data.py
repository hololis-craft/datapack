from google.oauth2.service_account import Credentials
import gspread

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/10czE4OoQ-3k_SK0TGciAh9-b14DudNp1JeHLyQRd80g/edit#gid=0"


scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credentials = Credentials.from_service_account_file(
    "google-credentials.json", scopes=scopes
)

gc = gspread.authorize(credentials)


spreadsheet = gc.open_by_url(SPREADSHEET_URL)
print(spreadsheet.get_worksheet(0).get_all_records())
