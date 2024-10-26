import os
from pyrogram import Client
from asyncio import sleep
from random import choices
from string import ascii_letters
from tqdm.asyncio import tqdm
from colorama import Fore
from stdiomask import getpass


class TelegramMessageFilter:
    def __init__(self):
        self.client = None
        self.authenticate()

    def authenticate(self):
        session_file = next((f.split('.')[0] for f in os.listdir() if f.endswith('.session')), None)
        if session_file:
            self.client = Client(session_file)
        else:
            print(f'{Fore.GREEN}Required information here: https://my.telegram.org/apps\n')
            self.client = Client(
                name="".join(choices(ascii_letters, k=15)),
                api_id=int(input('Enter your API ID: ')),
                api_hash=input('Enter your API Hash: '),
                phone_number=getpass('Enter your phone number: ', '*'),
                password=getpass('Enter your password (if applicable): ', '*')
            )
            os.system('cls' if os.name == 'nt' else 'clear')

        with self.client:
            self.client.loop.run_until_complete(self._run_search())

    async def _run_search(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.GREEN}Authorization successful!")
        chat_id = input("Enter chat ID: ")
        search_queries = {query.strip().lower() for query in
                          input("Enter search queries (comma separated): ").split(",")}
        forward_limit = int(input("Enter the number of messages to be forwarded: "))

        with tqdm(total=forward_limit, desc="Forwarding Messages") as pbar:
            async for message in self.client.get_chat_history(chat_id):
                if message.text and any(query in message.text.lower() for query in search_queries):
                    await self.client.forward_messages("me", chat_id, message.id)
                    pbar.update(1)
                    if pbar.n >= forward_limit:
                        break
                await sleep(0.01)


if __name__ == '__main__':
    try:
        TelegramMessageFilter()
    except Exception as e:
        print(f"An error occurred: {e}")
    input("Press Enter to exit...")
