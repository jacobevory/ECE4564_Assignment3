import requests

access_token = '4511~qCyMvD0YiKX4IrjRoxuhJ7iytKJkKCXIYGM4nQdqFPgjimz8a0gdZtljZWuoq533'
filename = 'uploadtest.txt'

api_url='https://canvas.vt.edu/api/v1/groups/46402/files'
session = requests.Session()
session.headers = {'Authorization': 'Bearer %s' % access_token}
payload = {}
payload['name'] = filename
payload['parent_folder_path'] = '/'
r = session.post(api_url, data=payload)
r.raise_for_status()
r = r.json()
payload = list(r['upload_params'].items())
with open(filename, 'rb') as f:
     file_content=f.read()
payload.append((u'file', file_content))
r = requests.post(r['upload_url'], files=payload)
r.raise_for_status()
r = r.json()



