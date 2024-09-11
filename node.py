import requests
import json

# Define your API URL and Access Token
api_url = "https://go.getblock.io/6b1596a2490241c88276f45cc11d4999"
access_token = "YOUR_ACCESS_TOKEN"

# Set the headers for authorization and content-type
headers = {
    'x-api-key': access_token,
    'Content-Type': 'application/json'
}

# Create the JSON-RPC request with 'rules' parameter
payload = json.dumps({
    "jsonrpc": "2.0",
    "id": "btc-6b159",
    "method": "getblocktemplate",
    "params": [{
        "rules": ["segwit"]
    }]
})

# Send the request to GetBlock's Bitcoin API
response = requests.post(api_url, headers=headers, data=payload)

# Parse the response
block_template = response.json()

# Print the block template to see what was returned
print(json.dumps(block_template, indent=4))
