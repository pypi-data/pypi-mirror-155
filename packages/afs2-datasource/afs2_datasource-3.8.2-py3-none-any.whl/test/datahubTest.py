import os
from afs2datasource import DBManager, constant

# --------- config --------- #
db_type = constant.DB_TYPE['DATAHUB']
username = 'krq1998@126.com'
password = 'Kongruoqi123!'
datahub_url = 'http://portal-datahub-sdgs-ews.yy.sdgs.com.cn'

datahub_config = [{
    "name": "string", # dataset name
    "project_id": "project_id",
    "node_id": "node_id",
    "device_id": "device_id",
    "tags": [
      "tag_name"
    ]
}]
uri = 'influxdb://d44b1476-f532-4ce2-8244-fec7bffd858e:0ERVNiAbxCBWJZldFT6JMHdr4@172.17.21.111:8086/1f65d529-898c-46d8-8d71-30671a3f820b'
folder_name = 'ttt'
# -------------------------- #

manager = DBManager(db_type=constant.DB_TYPE['DATAHUB'],
  username=username,  # sso username
  password=password,  # sso password
  datahub_url=datahub_url,
  datahub_config=datahub_config,
  uri=uri,
  # timeRange or timeLast
  timeLast={'lastDays': 0, 'lastHours': 0, 'lastMins': 1}
)

try:
  # connect to azure blob
  is_success = manager.connect()
  print('Connection: {}'.format(is_success))
  response = manager.execute_query()
  print('Execute query successfully: {}'.format(response))

except Exception as e:
  print(e)
