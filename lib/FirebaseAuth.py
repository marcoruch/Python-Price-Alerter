import pprint

# FB User Result
class FBAuthorizationResult:
    """A simple Authorization class"""
    def __init__(self, user_token, user_id, authorized):
        self.user_tokenr = user_token
        self.user_id = user_id
        self.authorized = authorized
        
# Standard check
# HEADER: User-Token ===  FirebaseAuthorization Token  (ID Token) 
# HEADER: User-Id === 28 Digits Long UserHandle | User-Id  (User-Identifier on Database)
def authorizeUser(request,session):
    user_token = request.headers['User-Token']
    user_id = request.headers['User-Id']
    try:
        # must be the same
        if session['user_token'] != user_token:
            pprint.pprint("User could not be authorized.... " + user_id)
            return FBAuthorizationResult(user_token, user_id, False)
        else:
            pprint.pprint("User was authorized.... " + user_id)
            return FBAuthorizationResult(user_token, user_id, True)
    except:
        pprint.pprint("User could not be authorized.... " + user_id)
        return FBAuthorizationResult(user_token, user_id, False)