import requests
import pandas as pd 
from string import printable
import time

def translate(text_):
    url = "https://text-translator2.p.rapidapi.com/translate"

    payload = {
        "source_language": "zh",
        "target_language": "en",
        "text": f"{text_}"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "0f52a3b3b3msh3fb61976f66b189p126bc4jsnb46f826b622a",
        "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
    }


    response = requests.post(url, data=payload, headers=headers)

    return response.json()


def get_required_values(df):
    output_dataframe_list = []
    columns = []
    count = 0
    print("Translation Started")
    for col_name in df.columns:
        if set(str(col_name)).difference(printable):
            columns.append(translate(col_name)['data']['translatedText'])
        else:
            columns.append(col_name)
    for row in range(len(df)):
        each_row = []
        for text in df.iloc[row]:
            if set(str(text)).difference(printable):
                each_row.append(translate(text)['data']['translatedText'])
            else:
                each_row.append(text)
        output_dataframe_list.append(each_row)
    return output_dataframe_list,columns


df = pd.read_excel('Order Export.xls')

start_time = time.time()
output_rows,columns = get_required_values(df)
output = pd.DataFrame(output_rows,columns = columns)

output.to_excel('Output.xlx')

print("Time Taken by the program - %s " % (time.time() - start_time))   