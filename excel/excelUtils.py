import numpy as np
import pandas as pd


EXCEL_PATH = "C://Users//yijin//Desktop//447051294509056. 河南省2024年度统一考试录用公务员拟录用职位表.xls"

def load_excel():
    df=pd.DataFrame(pd.read_excel(EXCEL_PATH, header=2))
    return df
if __name__ == "__main__":
    df = load_excel()
    line_size, col_len = df.shape
    print("line_size : ", line_size)
    print("col_len : ", col_len)
    print(df.columns)
    for i in range(0, line_size):
        if("济源" in df["招录单位"][i] and "35" in df['年龄要求'][i] and "软件工程" in df['专业（学科）类别'][i]):
            for lable in df.columns:
                print(df[lable][i], end=" ")
            print("")                
    
    # print(df.columns)
    # print(columns)