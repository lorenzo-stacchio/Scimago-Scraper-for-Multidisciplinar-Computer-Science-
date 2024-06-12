import requests

# Define the URL and headers
url = 'https://api.hikerapi.com/v2/hashtag/medias/recent?name=5xmille'

headers = {
    'accept': 'application/json',
    'x-access-key': 'XFlaTHVioAgiwWIndiJ9ZrBMXSraZftn'
}


# Make the GET request
response = requests.get(url, headers=headers)


# Check if the request was successful
if response.status_code == 200:
    # Save the response content to a file
    with open('INSTAGRAM/5mille_v2_test.json', 'w', encoding="utf-8") as file:
        file.write(response.text)
    print("Response saved successfully.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
