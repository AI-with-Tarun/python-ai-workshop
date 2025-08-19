import asyncio

async def scrape_page(url):
    print(f"Fetching {url}...")
    await asyncio.sleep(1) 
    data = f"Content from {url}"
    print(f"Got: {data}")
    return data

async def scrape_multiple():
    result1 = await scrape_page("https://tarunjain.netlify.app")
    result2 = await scrape_page("https://github.com/lucifertrj") 
    
    print(f"All results: {[result1, result2]}")

asyncio.run(scrape_multiple())  