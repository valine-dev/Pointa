import requests

targetUri = 'http://127.0.0.1:5000'
ingameStruct = '/inGame/{0}?fts={1}&r={2}&p={3}'

# Login
req = requests.post(
                targetUri+'/outGame/'+'null',
                json={'Action': 'Ready'}
            )
req2 = requests.post(
                targetUri+'/outGame/'+'null',
                json={'Action': 'Ready'}
            )
try:
    assert req.status_code == 200
except AssertionError:
    print('Login1 Error')
p1k = req.json()['UUID']
try:
    assert req2.status_code == 200
except AssertionError:
    print('Login2 Error')
p2k = req2.json()['UUID']


req = requests.post(
    targetUri+'/outGame/'+p1k,
    json={'Action': 'Invite','Target': p2k}
    )
try:
    assert req.status_code == 200
except AssertionError:
    print('Invite Error')

url = targetUri + ingameStruct.format(
    p2k,
    '0',
    '0',
    '0'
)
req = requests.get(url)
try:
    assert req.status_code == 200
except AssertionError:
    print('Recieve Error, Url:', url)



print('Accepted. 0 BUG!')
