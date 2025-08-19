import asyncio
import requests

async def check_status(url):
    r = requests.get(url)
    print(f"{url} is {r.status_code}")

urls = ["https://google.com", "https://github.com"]

async def main():
    await asyncio.gather(*(check_status(u) for u in urls))

asyncio.run(main())


async def download(filename):
    print(f"Starting {filename}")
    await asyncio.sleep(0.05) 
    print(f"Downloaded {filename}")

async def main():
    await asyncio.gather(
        download("photo.jpg"),
        download("video.mp4"),
        download("music.mp3")
    )

asyncio.run(main())  