import pandas as pd

def format_chart_trace(x,y, type):
    if(type == "pie"):        
        return {
            "values": y,
            "labels": x,
            "type": 'pie'
        }
        
    return {
            "type": type,
            "x": x,
            "y": y
        }
    
    
    
def process_simple_chart(df,chart_meta, csv_sheet_name, filter):
    chart_type = chart_meta["chart_type"]

    first_column = df.columns[0]
    filter_cols = df.columns[1:]

    df[filter_cols] = df[filter_cols].apply(pd.to_numeric, errors='coerce')

    available_filters = filter_cols.tolist()
    selected_filter = filter if filter in available_filters else available_filters[0]

    first_column_values = df[first_column].fillna("").tolist()
    values = df[selected_filter].fillna(0).tolist()


    trace = format_chart_trace(first_column_values,values, chart_type)

    return {
    'chart_config':{
        "traces":[trace],
        "layout":{}
    },
    'title': csv_sheet_name,
    "options": available_filters,
    'selected_option': selected_filter
    }


def process_double_chart(df, chart_meta,csv_sheet_name, filter):
    column_filter_name = chart_meta["column_name"]
    chart_type = chart_meta["chart_type"]

                
    available_column_filters = df[column_filter_name].unique()
    selected_column_filter = filter if filter in available_column_filters else available_column_filters[0]

    # Filtrar as linhas onde a coluna 'Company' == 'SWITCH'
    filtered_df = df[df[column_filter_name] == selected_column_filter]

    # Remover a coluna 'Company'
    filtered_df = filtered_df.drop(columns=[column_filter_name])

    traces = []
    x = filtered_df.columns[1:].to_list()
    for _, row in filtered_df.iterrows():
        trace = {
            "x": x,
            "y": [row[col] for col in x],
            "name": row[0],
            "type": "bar"
        }
        traces.append(trace)

    return  {
        'title': csv_sheet_name,
        'type': chart_type,
        'chart_config':{
            "traces":traces,
            "layout":{
                "barmode": "stack",
                "showlegend":True,
                "legend": {
                    "title": { "text": '' },     
                    "traceorder": 'normal'
                }
            }
        },
        "options": available_column_filters,
        'selected_option': selected_column_filter,
        'columns_filter':{
            'available': available_column_filters,
            'selected': selected_column_filter
        }
    }