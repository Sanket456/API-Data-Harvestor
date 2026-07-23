import requests
import json
import time
import os

#Step 1 Data Shield (handling Unpredictable Data)

def fetch_with_breakoff(url: str, max_retries: int = 4) ->dict:
    #Think of this function as a polite but persistent waiter.

    wait_time = 1

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124"
    }

    #We will loop and try upto 4 times before giving up 
    for attempt in range(max_retries):
        print(f"Attemp {attempt+ 1} of {max_retries}: Knocking on the API's Door. ")

        try:
            # 1. SEND THE REQUEST: Go get the data! (timeout=10 means give up if it takes longer than 10s)
            response = requests.get(url, headers=header,timeout=10)
            
            # 2. CHECK THE STATUS CODE (Did they accept our order?)
            if(response.status_code==200):
                # 200 means "OK! Here is your data."
                print("Success! the API gave us Data")
                return response.json()
            elif(response.status_code==209 or response.status_code>=500):
                # 429 means "You are asking too fast". 500 means "Our Server Crashed".
                print(f"API is busy (Error {response.status_code}). Pausing for {wait_time} seconds ....")
                time.sleep(wait_time)
                wait_time = wait_time*2 # EXPONENTIAL BACKOFF: Double the wait time (1s, 2s, 4s, 8s)
            else:
                # Any other error (like a 404 Not Found), we just stop immediately.
                print(f"Fatal Error {response.status_code}. URL might be wrong.")
                return None
        except requests.exceptions.RequestException as e:
            #Wifi or Network Issue
            print(f"Network error!  Check you wifi {e}")
            time.sleep(wait_time)
            wait_time = wait_time*2
    print("We tried 4 times giving up")
    return None

def main():
    print("\n ===Starting the Pipeline ===")

    # 1. The Target: SpaceX Historical Rocket Launches
    api_url = "https://api.spacexdata.com/v4/launches"
    
    # 2. Extract: Send our 'Shield' function to get the data safely
    raw_data = fetch_with_breakoff(api_url)

    # 3. Load: Save it to the "Bronze Layer" (Your local hard drive)
    if(raw_data !=None):
        # Check if a folder named "data" exists. If it doesn't, create it!
        os.makedirs("data", exist_ok=True)

        file_path = os.path.join("data", "spacex_launches.json")

        # Added encoding='utf-8' to safely handle special characters in the text
        with open(file_path,'w', encoding='utf-8') as file:
            json.dump(raw_data,file, indent=4)
        
        print(f"Data saved successfully to: {file_path}")
        print(f"We downloaded {len(raw_data)} records.")

    print("=== Pipeline Complete ===\n")

# This tells Python: "Only run the main() function if I click 'Run' on this specific file."
if __name__ == "__main__":
    main()


