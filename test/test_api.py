import requests
from core.utils import log_exception

if __name__ == "__main__":
    """
    Note: Make sure the API is running before testing the API calls 
    """
    try:
        print("------------- Testing API -------------")
        URL = "http://0.0.0.0:8091/blockchain_data"
        UserID = "blockcypher"
        Password = "netcent@1"
        lim = 10
        payload = {"num_of_records": lim}
        resp = requests.post(URL, json=payload, auth=(UserID, Password))
        if resp.status_code == 200:
            print(f"Successfully Authenticated: {resp.status_code } ")
        json_len = len(resp.json())
        if json_len <= lim:
            print(f"Successfully retrieved the records: {json_len}")
        print("------- API Tested Successfully -------")
    except Exception as e:
        log_exception(e, "Error while testing API Endpoint")
        print("--------- API Test Unsuccessful ---------")
