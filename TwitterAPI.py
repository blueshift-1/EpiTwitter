
import config
import twitter
import time

def api_connection():
    api = twitter.Api(consumer_key=config.get_consumer_token(),
                          consumer_secret=config.get_consumer_secret(),
                          access_token_key=config.get_access_token(),
                          access_token_secret=config.get_access_secret())
    print(api.VerifyCredentials())
    #print(api.GetFriends("45040932"))
    #print (api._GetFriendsFollowersPaged(user_id = 1, count = '200', cursor=str(-1)))
    #print(api.CheckRateLimit())
    followers = api.GetFollowerIDs("45040932")
    followers_info = api.GetUser(user_id = followers)
    print(followers_info)
    return(api)

def post_status(api, msg):

    status = api.PostUpdate(msg)


def get_friends(api, id):

    # Holds all responses
    responses = []
    # Keeps track of the cursor (Page bookmark within results
    c = -1

    while c != 0:

        if c!=-1:
            time.sleep(60)
        print (api._GetFriendsFollowersPaged(user_id = id, count = '200', cursor=str(c)))
        #c = response ['next_cursor']
        print("NEXT CURSOR: " + str(c))
        #print(response)

        c = 0
    return(responses)
