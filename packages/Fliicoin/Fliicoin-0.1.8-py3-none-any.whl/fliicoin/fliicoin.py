class fliicoin:
    def blocks(type):
        if type.lower() == 'all':
            return ('Network Blocks (amount per block):\nFast: 10\nMedium: 5\nSlow: 3\nUltra-Slow: 1')
        elif type.lower() == 'fast':
            return ('Fast Network Block: 10')
        elif type.lower() == 'medium':
            return ('Medium Network Block: 10')
        elif type.lower() == 'slow':
            return ('Slow Network Block: 10')
        elif type.lower() == 'ultra-slow':
            return ('Ultra-slow Network Block: 10')
        else:
            return ('Invalid network type. Please use fast, medium, slow, ultra-slow, or all')

    def block(type):
        print('Please use blocks instead of block')

    def server():
        import requests
        link = ('https://www.fliicoin.com/api/server')
        f = requests.get(link)
        return (f.text)

    def mine(username, input):
        import requests
        link = ('https://www.fliicoin.com/mine?username=' + username + '&guess=' + input)
        f = requests.get(link)
        return (f.text)