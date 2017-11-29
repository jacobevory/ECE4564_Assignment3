import zeroconf
import socket
 
server = zeroconf.Zeroconf()
 
# Get local IP address
local_ip = socket.gethostbyname(socket.gethostname())
local_ip = socket.inet_aton(local_ip)

svc1 = zeroconf.ServiceInfo('_team18._tcp.local.',
                              'colors._team18._tcp.local.',
                              address = local_ip,
                              port = 2972,
                              weight = 0, priority=0,
                              properties = {'colors':
                                            'red blue green cyan'}
                             )
server.register_service(svc1)