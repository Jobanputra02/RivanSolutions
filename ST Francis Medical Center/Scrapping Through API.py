import requests
import pandas as pd

headers = {
    'authority': 'intake.steerhealth.io',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://intake.steerhealth.io',
    'referer': 'https://intake.steerhealth.io/new-doctor-search/aa1f8845b2eb62a957004eb491bb8ba70a',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
                  'Safari/537.36',
}
json_data = {
    'name': '',
    'specialty': '',
    'distance': '',
    'location': '',
    'errors': {},
    'organizationId': 'aa1f8845b2eb62a957004eb491bb8ba70a',
    'size': 484,
    'page': 0,
}

response = requests.post('https://intake.steerhealth.io/api/doctor-search', headers=headers, json=json_data)
response.raise_for_status()
master_data = response.json()["items"]

df = pd.DataFrame(
    columns=["Full Name", "Specialty", "Add Specialty", "Gender", "Full Address", "Practice", "Address", "City",
             "State", "ZIP", "Phone", "Fax"])
dict_to_add = {}

for i in range(0, json_data['size']):

    # Full Name
    first_name = master_data[i]["firstName"]
    last_name = master_data[i]["lastName"]
    full_name = f"{first_name} {last_name}"

    # Speciality
    if master_data[i]["specialty"]:
        speciality = master_data[i]["specialty"][0]
    else:
        speciality = ""

    # Additional Speciality
    if master_data[i]["specialty"]:
        if len(master_data[i]["specialty"][1:]) == 0:
            additional_speciality = ""
        else:
            additional_speciality = ", ".join(master_data[i]["specialty"][1:])
            # additional_speciality = master_data[i]["specialty"][1:]
    else:
        additional_speciality = ""

    # Gender
    if master_data[i]["gender"]:
        gender = master_data[i]["gender"]
    else:
        gender = ""

    if master_data[i]["addresses"]:
        # Practice
        if master_data[i]["addresses"][0]["name"]:
            practice = master_data[i]["addresses"][0]["name"]
        else:
            practice = ""

        # Address
        if master_data[i]["addresses"][0]["address"]:
            address = master_data[i]["addresses"][0]["address"]
        else:
            address = ""

        if master_data[i]["addresses"][0]["address2"]:
            address2 = master_data[i]["addresses"][0]["address2"]
        else:
            address2 = ""

        # City
        if master_data[i]["addresses"][0]["city"]:
            city = master_data[i]["addresses"][0]["city"]
        else:
            city = ""

        # State
        if master_data[i]["addresses"][0]["state"]:
            state = master_data[i]["addresses"][0]["state"]
        else:
            state = ""

        # ZIP
        if master_data[i]["addresses"][0]["zip"]:
            zipcode = master_data[i]["addresses"][0]["zip"]
        else:
            zipcode = ""

        address = f"{address} {address2} {city} {state} {zipcode}"

        # Full Address
        full_address = f"{practice} {address}"

        # Phone
        if master_data[i]["addresses"][0]["phoneNumber"]:
            phone = master_data[i]["addresses"][0]["phoneNumber"]
        else:
            phone = ""

        # Fax
        if master_data[i]["addresses"][0]["fax"]:
            fax = master_data[i]["addresses"][0]["fax"]
        else:
            fax = ""

    else:
        practice = ""
        address = ""
        city = ""
        state = ""
        zipcode = ""
        full_address = ""
        phone = ""
        fax = ""

    dict_to_add["Full Name"] = [full_name]
    dict_to_add["Specialty"] = [speciality]
    dict_to_add["Add Specialty"] = [additional_speciality]
    dict_to_add["Gender"] = [gender]
    dict_to_add["Practice"] = [practice]
    dict_to_add["Address"] = [address]
    dict_to_add["City"] = [city]
    dict_to_add["State"] = [state]
    dict_to_add["ZIP"] = [zipcode]
    dict_to_add["Full Address"] = [full_address]
    dict_to_add["Phone"] = [phone]
    dict_to_add["Fax"] = [fax]
    df_to_add = pd.DataFrame(dict_to_add)
    df = pd.concat([df, df_to_add])

# df.to_csv("doctor-search.csv")
