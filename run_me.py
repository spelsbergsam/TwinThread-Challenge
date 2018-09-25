# Samuel Spelsberg
# September 24th, 2018
# TwinThread Challenge

#------------- Read in the JSON file---------------------#
import pandas as pd
from pandas.io.json import json_normalize
import json
from urllib.request import urlopen
import df_work

# turn the .txt file into a python dictionary object --> .txt is in json format
txt_data = urlopen("https://www.twinthread.com/code-challenge/assets.txt")
data = json.load(txt_data)

# get status number from key for critical conditio and make global var for it
statuses = data['asset_status']
CRITICAL_STATUS = statuses['Critical']

# turn assets into df
df_data = pd.DataFrame.from_dict(json_normalize(data['assets']), orient='columns')

new_dict = {}
id = 0
for asset in data['assets']: #put the embedded dicts into columns
    asset_id = asset['assetId']
    classList = asset['classList']
    ids = []
    drills = []
    names = []
    for i in classList:
        ids.append(i['id'])
        drills.append(i['drill'])
        names.append(i['name'])
    new_dict[id] = [asset_id, ids, names, drills]
    id+=1

new_df = pd.DataFrame.from_dict(new_dict, orient='index', columns=['assetId', 'classList.id', 'classList.name', 'classList.drill'])
df_data = df_data.drop('classList', 1) # normalize the data frame by dropping classList
clean_df = df_data.merge(new_df, left_on = 'assetId', right_on='assetId', how='inner')

def defaultScreen():
    print("""These are the following supported commands:
  1 - Search by top level field
  2 - Display list of assets with critical status
  3 - Provide count of unique class names, and list assets in each unique class
  4 - Display visual heirarchy of given asset ID

  Type the number corresponding to the action you want.""")


# ------------------ Simple console user interface -----------------------#
print('Welcome to TwinThread Asset Information Portal.')

while(True):
    defaultScreen()

    #validate input -----------
    inp = input()
    inp = inp.strip()
    while( inp not in ['1', '2', '3', '4'] ):
        print("Invalid input, try again. (1-4)")
        inp = input()

    if inp == '1':
        df_work.searchTopLevel(clean_df)
    elif inp == '2':
        df_work.listCriticalAssets(clean_df, CRITICAL_STATUS)
    elif inp == '3':
        df_work.uniqueClass(clean_df)
    elif inp == '4':
        print('Ran out of time!')
    else:
        print("Invalid input. Please relaunch program.") # <-- shouldn't happen
        exit()

    print("\n\nThank you, you may select another action\n")









#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#    print(df_data)
