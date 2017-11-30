canvasAccessToken = "4511~4EMizjmsMkdhFJ8db8W3NHvmHYmX5GkpT7Dl70Zk8vyAsv5TrstxRBooRA1On43s"

#Token:			
#4511~4EMizjmsMkdhFJ8db8W3NHvmHYmX5GkpT7Dl70Zk8vyAsv5TrstxRBooRA1On43s		
#Copy this token down now. Once you leave this page you won't be able to retrieve the full token #anymore, you'll have to regenerate it to get a new value.		
#App:	User-Generated		
#Purpose:	ECE4564_Assignment3		
#Created:	Nov 15 at 6:38pm		
#Last Used:	--		
#Expires:	Dec 31 at 12am		
#Regenerate Tokenimport requests

'''
url ='https://vt.instructure.com/files/5541430/download?download_frd=1&verifier=6wvPx91ZgGvBNwdrAZur7R3MlkWziVRe0Yhj5rvH'
r = requests.get(url, allow_redirects=True)
open('file', 'wb').write(r.content)
'''