import pandas as _pd

def get_luckysheet(df: _pd.DataFrame, name="Sheet1"):

    index_size = len(df.columns.levels) if isinstance(df.columns, _pd.MultiIndex) else 1
    column_list = [list(e) for e in df.columns] if isinstance(df.columns, _pd.MultiIndex) else [[e] for e in df.columns]

    output = {
        "name": name,
        "color": "",
        "status": 1,
        "order": 0,
        "config": {
            "rowlen": {},
            "customHeight": {},
            "merge": {},
            "borderInfo": [
                {
                    "rangeType": "range",
                    "borderType": "border-all",
                    "color": "#000",
                    "style": "1",
                    "range": [
                        {
                            "row": [
                                0,
                                len(df)+index_size-1,
                            ],
                            "column": [
                                0,
                                len(df.columns)-1
                            ],
                        }
                    ]
                },
                {
                    "rangeType": "range",
                    "borderType": "border-all",
                    "color": "#000",
                    "style": "8",
                    "range": [
                        {
                            "row": [
                                0,
                                index_size-1
                            ],
                            "column": [
                                0,
                                len(df.columns)-1
                            ],

                        }
                    ]
                }]

        },
        "filter_select": {
            "row": [
                index_size - 1 ,
                len(df)+1,
            ],
            "column": [
                0,
                len(df.columns)-1
            ]},
        "data": [ *[[{
            "m": el[col_row_idx],
            "ct": {
                "fa": "General",
                "t": "g"
            },
            "v": el[col_row_idx],
            "bl": 1,
            "fs": "11"
        } for el in column_list ] for col_row_idx in range(index_size) ], *df.values.tolist()],
        "row": len(df)+1,
        "column": len(df.columns),
        "scrollLeft": 0,
        "scrollTop": 0,
        "frozen": {
            "type": "rangeRow",
            "range": {
                "row_focus": index_size-1,
                "column_focus": 0
            }
        },

    }

    # add merged header cols

    # loop the colums to define their color
    for idr in range(index_size):

        color_a = True
        lastvalue_4_color = None
        lastvalue = output["data"][idr][0]["v"]
        last_group_idx = 0

        for idc, col in enumerate(column_list):

            # change the color if the colum has changed
            if lastvalue_4_color and output["data"][idr][idc]["v"] != lastvalue_4_color:
                color_a = not color_a

            # first set the color of the header
            output["data"][idr][idc].update({"bg": "#BBBBBB" if color_a else "#EEEEEE"})    

            # if the title will change or it is the last cell
            if lastvalue and (idc+1 == len(df.columns) or output["data"][idr][idc+1]["v"] != lastvalue):

                if idc - last_group_idx  > 0:
                    output["config"]["merge"][f"{idr}_{last_group_idx}"] = {
                        "r": idr,
                        "c": last_group_idx,
                        "rs": 1,
                        "cs": idc-last_group_idx+1
                    }

                last_group_idx = idc+1
                if idc+1 < len(df.columns):
                    lastvalue = output["data"][idr][idc+1]["v"]

            lastvalue_4_color = output["data"][idr][idc]["v"]

    return output
