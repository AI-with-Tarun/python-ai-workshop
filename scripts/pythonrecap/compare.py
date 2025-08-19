# without threading
import threading
import requests
import time

def download_image(url):
    print(f"Starting download from {url}")
    img = requests.get(url).content
    print(f"Finished downloading {len(img)} bytes from {url}")

urls = ["https://static0.gamerantimages.com/wordpress/wp-content/uploads/2024/12/all-of-the-one-piece-movies-specials-ranked.jpg", 
        "https://akm-img-a-in.tosshub.com/indiatoday/images/story/202410/one-piece-will-return-in-april-2025-with-a-new-arc-153338935-16x9_0.jpg"]

start_time = time.time()

for url in urls:
    download_image(url)

end_time = time.time()
print(f"\nSequential execution took: {end_time - start_time:.2f} seconds")