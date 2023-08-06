from taodata.util import client
from taodata.util import auth
import pandas as pd
if __name__ == '__main__':
    token = auth.get_token()
    api = client.DataApi(token=token)
    topics = api.get_topics()
    print(topics)

    ret = api.get_task_data(token='971969723014864896', task_id='185')
    df = pd.DataFrame(columns=ret['fields'],data=ret['records'])
    print(df)



