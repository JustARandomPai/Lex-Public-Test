import aiohttp
import asyncio
import random
import string
import logging

from .utilities import debug_print

async def fetch_username(session, user, config):
    retries = config['defaultRetries']
    for attempt in range(retries):
        try:
            async with session.get(
                f'https://auth.roblox.com/v1/usernames/validate?request.username={user}&request.birthday=1337-04-20',
                ssl=None,
                timeout=5
            ) as response:
                if response.status != 200:
                    debug_print(f"HTTP Error {response.status} for user {user}. Retrying...")
                    await asyncio.sleep(2 ** attempt)
                    continue
                data = await response.json()
                return data, user
        except (aiohttp.ClientConnectionError, aiohttp.ClientPayloadError, asyncio.TimeoutError) as e:
            debug_print(f"Error for user {user}: {str(e)}. Retrying...")
            await asyncio.sleep(2 ** attempt)
    return None, user

async def find_usernames(config):
    valid_usernames = []
    config = config["settings"]
    Found = 0

    async with aiohttp.ClientSession() as session:
        while Found < config['targetValidNames']:
            tasks = []
            batch_size = min(config['defaultBatchSize'], config['targetValidNames'] - Found)
            for _ in range(batch_size):
                user = randomword(config['length'], config['includeNumbers'])
                if is_valid_username(user):
                    task = asyncio.create_task(fetch_username(session, user, config))
                    tasks.append(task)

            responses = await asyncio.gather(*tasks)

            for data, user in responses:
                if data and 'code' in data and int(data['code']) == 0:
                    Found += 1
                    valid_usernames.append(user)
                    try:
                        with open('valid.txt', 'a') as f:
                            f.write(f"{user}\n")
                    except IOError as e:
                        debug_print(f"Error writing username {user} to file: {str(e)}")

    return valid_usernames

def display_summary(valid_usernames, config):
    print(f"Found {len(valid_usernames)} valid usernames.")
    if valid_usernames:
        for index, username in enumerate(valid_usernames, start=1):
            print(f"{index:02d} - {username}")

def reset_counters():
    pass

def randomword(length, include_numbers):
    letters = string.ascii_lowercase + (string.digits if include_numbers else '')
    return ''.join(random.choice(letters) for _ in range(length))

def is_valid_username(username):
    valid = len(username) >= 3 and len(username) <= 20 and username.isalnum()
    if not valid:
        logging.warning(f"Invalid username generated: {username}. Must be 3-20 characters and alphanumeric.")
    return valid
