import asyncio
import json
import os
from twikit import Client

def clean_cookie_file():
    """Convert cookie format"""
    try:
        with open("cookies.json", "r") as f: 
            data = json.load(f) # loads your cookies.json file

        # if it's already a dict, it's probably fine
        if isinstance(data, dict):
            return

        # if it's a list, convert it
        if isinstance(data, list):
            print("[!] Cleaning format...")
            cookies_dict = {cookie["name"]: cookie["value"] for cookie in data}

            with open("clean_cookies.json", "w") as f:
                json.dump(cookies_dict, f, indent=2)
            print("[+] Cookies cleaned and saved.")
    except Exception as e:
        print(f"[!] Failed to read or clean cookies: {e}")

def login():
    clean_cookie_file()
    client = Client()
    client.load_cookies("clean_cookies.json") # Authentication
    return client

async def auto_follow_back(client, username):
    user = await client.get_user_by_screen_name(screen_name=username)
    user_id = user.id

    while True:
        print("[*] Checking for new followers...")

        followers = await client.get_followers_ids(user_id=user_id)
        following = await client.get_friends_ids(user_id=user_id)

        follower_ids = set(followers)
        following_ids = set(following)

        to_follow_back = follower_ids - following_ids

        if to_follow_back:
            print(f"[+] Found {len(to_follow_back)} new followers to follow back.")
            for uid in to_follow_back:
                try:
                    await client.follow_user(user_id=uid)
                    print(f"[+] Followed back {uid}")
                    await asyncio.sleep(60)
                except Exception as e:
                    print(f"[!] Error following {uid}: {e}")
        else:
            print("[=] No new users to follow back.")

        print("[⏳] Sleeping for 5 minutes before next check...\n")
        await asyncio.sleep(300)

async def main():
    client = login()
    await auto_follow_back(client, "fruitlover83") # replace "fruitlover83" with your username.

if __name__ == "__main__":
    asyncio.run(main())
