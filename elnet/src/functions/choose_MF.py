import pandas as pd
from pathlib import Path


base_path = Path(__file__).resolve().parent
transponder_file_path = base_path / ".." / ".." / "data" / "params" / "transponders.csv"
df=pd.read_csv(transponder_file_path)
print(df)

def choose_MF(G,path,traffic_G,df):
    return

