import gspread as GS
gc = GS.service_account(filename='creds.json') 

previousWeekData = open("data/Building 1/test2.csv", 'r').read()
currentWeekData = open("data/Building 1/test1.csv", 'r').read()

gc.import_csv('1TI1BKUzVo8runnVTvOg_ttk1WLl_PZElSQWET47ZNt8', previousWeekData)
gc.import_csv('1REqhOuo6PhOqWs4qzfPx-gxJxJ0Fo6pL-rTVRFJT2-g', currentWeekData)