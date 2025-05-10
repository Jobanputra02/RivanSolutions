import requests

offset = 0
cursor = None
total_images_list = []
total_i = 0

while True:
    headers = {
        'Host': 'prod.meeshoapi.com',
        'authorization': '32c4d8137cn9eb493a1921f203173080',
        'app-version': '14.5',
        'app-version-code': '453',
        'instance-id': 'b60e8898495544a9a44914b14b58209c',
        'country-iso': 'in',
        'application-id': 'com.meesho.supply',
        'app-session-id': '23a41222-080d-4b45-8306-c3817491e62a',
        'app-sdk-version': '26',
        'app-client-id': 'android',
        'xo': 'eyJ0eXBlIjoiY29tcG9zaXRlIn0=.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTJOemd4TnpZMU1EWXNJbVY0Y0NJNk1UZ3pOVGcxTmpVd05pd2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaVlqWXdaVGc0T1RnME9UVTFORFJoT1dFME5Ea3hOR0l4TkdJMU9ESXdPV01pTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSTRabUk0TW1GbVpDMDNZems0TFRReU16Z3RZV05tTUMxaE56WXhaRGxtTkRZeVpXSWlmUS4xV2pjY2RtRnpmWjA0OTVyanhDOTJxelNwd3d3d3lvMTZhMU4zdjQ1YUR3IiwieG8iOm51bGx9',
        'app-iso-language-code': 'en',
        'content-type': 'application/json; charset=UTF-8',
        'user-agent': 'okhttp/4.9.0',
    }
    json_data = {
        'filter': {
            'type': 'meri_shop',
            'sort_option': None,
            'selected_filters': [],
            'session_state': None,
            'selectedFilterIds': [],
            'isClearFilterClicked': False,
            'supplier_id': 108483,
            'featured_collection_type': None,
        },
        'search_session_id': None,
        'cursor': cursor,
        'offset': offset,
        'limit': 20,
        'supplier_id': 108483,
        'featured_collection_type': None,
        'meta': None,
        'retry_count': None,
        'product_listing_page_id': None,
        'product_id_clicked_item': None,
    }

    response = requests.post('https://prod.meeshoapi.com/api/1.0/anonymous/meri-shop/feed', headers=headers,
                             json=json_data)
    response_json = response.json()
    # breaking the while loop
    if len(response_json['catalogs']) == 0:
        break

    total_i += sum([i['num_designs'] for i in response_json['catalogs']])

    # shifting to next page
    offset += 20
    cursor = response_json['cursor']

print(total_i)
