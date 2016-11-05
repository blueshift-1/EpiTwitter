
import config
import twitter
import time
import sys
import warnings

####  Modified Python-Twitter API Function to return JSON output ####

def UsersLookup_modified(self,
                    user_id=None,
                    screen_name=None,
                    users=None,
                    include_entities=True,
                    return_JSON = False):
    """Fetch extended information for the specified users.

    Users may be specified either as lists of either user_ids,
    screen_names, or twitter.User objects. The list of users that
    are queried is the union of all specified parameters.

    Args:
      user_id:
        A list of user_ids to retrieve extended information. [Optional]
      screen_name:
        A list of screen_names to retrieve extended information. [Optional]
      users:
        A list of twitter.User objects to retrieve extended information.
        [Optional]
      include_entities:
        The entities node that may appear within embedded statuses will be
        disincluded when set to False. [Optional]

    Returns:
      A list of twitter.User objects for the requested users
    """
    if not user_id and not screen_name and not users:
        raise twitter.TwitterError({'message': "Specify at least one of user_id, screen_name, or users."})

    url = '%s/users/lookup.json' % self.base_url
    parameters = {}
    uids = list()
    if user_id:
        uids.extend(user_id)
    if users:
        uids.extend([u.id for u in users])
    if len(uids):
        parameters['user_id'] = ','.join(["%s" % u for u in uids])
    if screen_name:
        parameters['screen_name'] = ','.join(screen_name)
    if not include_entities:
        parameters['include_entities'] = 'false'

    resp = self._RequestUrl(url, 'GET', data=parameters)
    try:
        data = self._ParseAndCheckTwitter(resp.content.decode('utf-8'))
    except twitter.TwitterError as e:
        _, e, _ = sys.exc_info()
        t = e.args[0]
        if len(t) == 1 and ('code' in t[0]) and (t[0]['code'] == 34):
            data = []
        else:
            raise

    if return_JSON:
        return data
    return [twitter.User.NewFromJsonDict(u) for u in data]


def _GetFriendsFollowers_TimeControlled (self,
                             url=None,
                             user_id=None,
                             screen_name=None,
                             cursor=None,
                             count=None,
                             total_count=None,
                             skip_status=False,
                             include_user_entities=True,
                             sleep_control=0):

    """ Fetch the sequence of twitter.User instances, one for each friend
    or follower.

    Args:
      url:
        URL to get. Either base_url + ('/followers/list.json' or
        '/friends/list.json').
      user_id:
        The twitter id of the user whose friends you are fetching.
        If not specified, defaults to the authenticated user. [Optional]
      screen_name:
        The twitter name of the user whose friends you are fetching.
        If not specified, defaults to the authenticated user. [Optional]
      cursor:
        Should be set to -1 for the initial call and then is used to
        control what result page Twitter returns.
      count:
        The number of users to return per page, up to a maximum of 200.
        Defaults to 200. [Optional]
      total_count:
        The upper bound of number of users to return, defaults to None.
      skip_status:
        If True the statuses will not be returned in the user items.
        [Optional]
      include_user_entities:
        When True, the user entities will be included. [Optional]

    Returns:
      A sequence of twitter.User instances, one for each friend or follower
    """

    if cursor is not None or count is not None:
        warnings.warn(
            "Use of 'cursor' and 'count' parameters are deprecated as of "
            "python-twitter 3.0. Please use GetFriendsPaged instead.",
            DeprecationWarning, stacklevel=2)

    count = 200
    cursor = -1
    result = []

    if total_count:
        try:
            total_count = int(total_count)
        except ValueError:
            raise twitter.TwitterError({'message': "total_count must be an integer"})

        if total_count <= 200:
            count = total_count

    while True:
        if total_count is not None and len(result) + count > total_count:
            break

        next_cursor, previous_cursor, data = self._GetFriendsFollowersPaged(
            url,
            user_id,
            screen_name,
            cursor,
            count,
            skip_status,
            include_user_entities)

        if next_cursor:
            cursor = next_cursor
            time.sleep(sleep_control)

        result.extend(data)

        if next_cursor == 0 or next_cursor == previous_cursor:
            break

    return result

def GetFollowers_TimeControlled(self,
                 user_id=None,
                 screen_name=None,
                 cursor=None,
                 count=None,
                 total_count=None,
                 skip_status=False,
                 include_user_entities=True,
                 sleep_control=0):
    """Fetch the sequence of twitter.User instances, one for each follower.

    If both user_id and screen_name are specified, this call will return
    the followers of the user specified by screen_name, however this
    behavior is undocumented by Twitter and may change without warning.

    Args:
      user_id:
        The twitter id of the user whose followers you are fetching.
        If not specified, defaults to the authenticated user. [Optional]
      screen_name:
        The twitter name of the user whose followers you are fetching.
        If not specified, defaults to the authenticated user. [Optional]
      cursor:
        Should be set to -1 for the initial call and then is used to
        control what result page Twitter returns.
      count:
        The number of users to return per page, up to a maximum of 200.
        Defaults to 200. [Optional]
      total_count:
        The upper bound of number of users to return, defaults to None.
      skip_status:
        If True the statuses will not be returned in the user items. [Optional]
      include_user_entities:
        When True, the user entities will be included. [Optional]

    Returns:
      A sequence of twitter.User instances, one for each follower
    """
    url = '%s/followers/list.json' % self.base_url
    return self._GetFriendsFollowers_TimeControlled(url,
                                     user_id,
                                     screen_name,
                                     cursor,
                                     count,
                                     total_count,
                                     skip_status,
                                     include_user_entities,
                                     sleep_control)
#### End Function ####


#### API Wrappers ####

def api_connection():
    api = twitter.Api(consumer_key=config.get_consumer_token(),
                          consumer_secret=config.get_consumer_secret(),
                          access_token_key=config.get_access_token(),
                          access_token_secret=config.get_access_secret())

    print(api.VerifyCredentials())
    return(api)

def post_status(api, msg):

    status = api.PostUpdate(msg)


def get_friends(api, id):

    return api.GetFollowers(id, sleep_control=60)
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


def get_user_information(api, ids):
    return( api.UsersLookup(users= ids, return_JSON=True))

#### End API Wrappers ####