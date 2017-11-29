import requests

url ='https://vt.instructure.com/files/5541430/download?download_frd=1&verifier=6wvPx91ZgGvBNwdrAZur7R3MlkWziVRe0Yhj5rvH'
r = requests.get(url, allow_redirects=True)
open('file', 'wb').write(r.content)

