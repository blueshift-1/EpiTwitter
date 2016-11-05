# Basic Utility Functions

import csv

def user_headers():
    return (['profile_background_tile', 'following', 'notifications', 'screen_name', 'utc_offset', 'profile_use_background_image', 'followers_count', 'profile_background_color', 'protected', 'default_profile', 'description', 'status', 'profile_text_color', 'time_zone', 'profile_link_color', 'contributors_enabled', 'has_extended_profile', 'entities', 'friends_count', 'statuses_count', 'geo_enabled', 'created_at', 'favourites_count', 'is_translator', 'id_str', 'location', 'translator_type', 'name', 'default_profile_image', 'lang', 'profile_image_url_https', 'profile_sidebar_fill_color', 'profile_banner_url', 'profile_background_image_url', 'url', 'is_translation_enabled', 'profile_image_url', 'profile_background_image_url_https', 'id', 'follow_request_sent', 'verified', 'listed_count', 'profile_sidebar_border_color'])

def print_csv(data, headers, file):
    with open(file, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, headers)
        dict_writer.writeheader()
        dict_writer.writerows(data)