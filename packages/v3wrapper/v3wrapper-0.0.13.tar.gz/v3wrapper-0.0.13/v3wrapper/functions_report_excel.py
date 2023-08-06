import pandas as pd
def excel_and_chart(list_of_dfs,list_of_sheet_names, xlsx_file_path="output.xlsx",chart_type='column',chart_width=1200,chart_height=600):
    '''
    :param list_of_dfs: self explanatory. Each df will go into one sheet
    :param list_of_sheet_names: one per df
    :param xlsx_file_path: must end in .xlsx
    :param chart_type: "line", "column", "bar" etc.
    :param chart_width: in pyxels
    :param chart_height: in pyxels
    '''
    #write it to excel
    df_sheet = zip(list_of_dfs,list_of_sheet_names)
    with pd.ExcelWriter(xlsx_file_path,engine='xlsxwriter') as writer:
        for d, sheet in df_sheet:
            #check if datetime index and delocalize
            if isinstance(d.index, pd.DatetimeIndex):
                d.index = d.index.tz_localize(None)
            #write each sheet
            d.to_excel(writer,sheet_name = sheet)
            (max_row, max_col) = d.shape
            #add charts
            chart = writer.book.add_chart({'type': chart_type})
            for i in range(len(d.columns)):
                col = i + 1
                chart.add_series({
                    'name':       [sheet, 0, col],
                    'categories': [sheet, 1, 0,   max_row, 0],
                    'values':     [sheet, 1, col, max_row, col],
                })
            writer.sheets[sheet].insert_chart(1, col+1, chart)
            chart.set_size({'width':chart_width, 'height':chart_height})
            chart.set_title({'name': sheet,'name_font': {'name': 'Calibri','color': 'black'}})
    return