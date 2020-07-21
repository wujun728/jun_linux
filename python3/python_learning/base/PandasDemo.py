import pandas as pd

series = pd.Series(range(10), index=reversed(range(10)));
print(series[9]);