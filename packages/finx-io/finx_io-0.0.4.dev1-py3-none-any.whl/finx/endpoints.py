#! Python
#
# endpoint functions
#
def ws_endpoint(environment):
    if environment == 'dev':
        return 'ws://54.152.2.221:3000'
    return 'ws://ws.finx.io'
