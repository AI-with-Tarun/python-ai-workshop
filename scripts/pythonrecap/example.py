import threading
import requests
import time

def download_image(url):
    print(f"Starting download from {url}")
    img = requests.get(url).content
    print(f"Finished downloading {len(img)} bytes")

urls = ["https://static0.gamerantimages.com/wordpress/wp-content/uploads/2024/12/all-of-the-one-piece-movies-specials-ranked.jpg", 
        "https://akm-img-a-in.tosshub.com/indiatoday/images/story/202410/one-piece-will-return-in-april-2025-with-a-new-arc-153338935-16x9_0.jpg"]

start_time = time.time()
threads = []
for url in urls:
    t = threading.Thread(target=download_image, args=(url,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

end_time = time.time()
print(f"\nThreaded execution took: {end_time - start_time:.2f} seconds")


import multiprocessing

def count_evens(numbers):
    count = sum(1 for n in numbers if n % 2 == 0)
    print(f"Found {count} even numbers")
    return count

data = [range(0, 100000), range(100000, 200000), range(200000, 300000)]

if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        results = pool.map(count_evens, data)
    
    print(f"Total even numbers: {sum(results)}")