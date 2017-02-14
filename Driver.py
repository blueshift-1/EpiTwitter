import TwitterAPI
import Utilities

test_id = "107336879"

con = TwitterAPI.api_connection()
followers = TwitterAPI.get_friends(con,test_id)


follower_information = TwitterAPI.get_user_information(con, followers)
