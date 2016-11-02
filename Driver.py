import TwitterAPI

import json


test_id = "45040932"

con = TwitterAPI.api_connection()
#followers = TwitterAPI.get_friends(con,test_id)
#with open(test_id + '.txt', 'w') as outfile:
#    json.dump(followers, outfile)