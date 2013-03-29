import OpenTokSDK



def get_session():
    api_key = '24175212' # Replace with your OpenTok API key.
    api_secret = '40f335ab2eb8bcd4c5f6c4c7cfa70638c1aff011'  # Replace with your OpenTok API secret.
    session_address = '192.168.1.12' # Replace with the representative URL of your session.
    
    opentok_sdk = OpenTokSDK.OpenTokSDK(api_key, api_secret)
    session = opentok_sdk.create_session(session_address)
    
    print session.session_id
    
    connectionMetadata = 'username=Bob, userLevel=4'
    token = opentok_sdk.generate_token(session.session_id, OpenTokSDK.RoleConstants.PUBLISHER, None, connectionMetadata)
    
    print token
