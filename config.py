import os

database_user = os.environ.get('database_user')
database_password = os.environ.get('database_password')
database_host = os.environ.get('database_host')
database_name = 'beauty_salon'
beauty_salon_token = os.environ.get('beauty_salon_token')
channel_cid = os.environ.get('channel_cid')

db_config = {'user':database_user , 'password':database_password , 'host':database_host , 'database':database_name}
db_config1 = {'API_TOKEN': beauty_salon_token}
db_config2 = {'channel_cid' : channel_cid}

