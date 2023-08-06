from taodata.util import auth

if __name__ == '__main__':
    token = '971969723014864896'
    auth.set_token(token)
    local_token = auth.get_token()
    if token == local_token:
        print('it is passed!')
    else:
        print('it is failed!')
