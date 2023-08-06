def blocks(type):
    if type.lower() == 'all':
        print('Network Blocks (amount per block):\nFast: 10\nMedium: 5\nSlow: 3\nUltra-Slow: 1')
    elif type.lower() == 'fast':
        print('Fast Network Block: 10')
    elif type.lower() == 'medium':
        print('Medium Network Block: 10')
    elif type.lower() == 'slow':
        print('Slow Network Block: 10')
    elif type.lower() == 'ultra-slow':
        print('Ultra-slow Network Block: 10')
    else:
        print('Invalid network type. Please use fast, medium, slow, ultra-slow, or all')

def block(type):
    print('Please use blocks instead of block')

def server():
    import urllib.request
    url = urllib.request.urlopen('https://www.fliicoin.com/api/server')
    if(url.getcode()==200):
       data = url.read()
       return data
    else:
       return ("Error receiving data: ", url.getcode())

def mine(username, input):
    import urllib.request
    url = urllib.request.urlopen('https://www.fliicoin.com/mine?username=' + username + '&guess=' + input)
    if(url.getcode()==200):
       data = url.read()
       return data
    else:
       return ("Something went wrong when attempting to mine: ", url.getcode())