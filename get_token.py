import gather_keys_oauth2 as Oauth2

CLIENT_ID = '22BCNW'
CLIENT_SECRET = 'd837c8ae2b4b0c84cd42123eee101ec8'

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()

ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

open("access_token", "w").write(ACCESS_TOKEN)
open("refresh_token", "w").write(REFRESH_TOKEN)
