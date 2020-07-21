import pandas as pd
import numpy as np
xlsx = pd.ExcelFile("../data/data.xlsx");
xlsx2 = pd.read_excel(xlsx, 'Sheet1')
print(xlsx2);


