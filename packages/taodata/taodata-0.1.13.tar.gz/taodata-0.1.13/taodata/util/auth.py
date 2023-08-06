# -*- coding:utf-8 -*- 

import pandas as pd
import os
from taodata.util import cons


def set_token(token):
    df = pd.DataFrame([token], columns=['token'])
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, cons.TOKEN_F_P)
    df.to_csv(fp, index=False)
    
    
def get_token():
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, cons.TOKEN_F_P)
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        return str(df.loc[0]['token'])
    else:
        print(cons.TOKEN_ERR_MSG)
        return None


