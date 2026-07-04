import asyncio 
import requests 
import os
import sys
from urllib.parse import urlparse
from concurrent.futures import ProcessPoolExecutor
from PIL import Image 

IMAGE_URLS = [
    "https://images.unsplash.com/photo-1516117172878-fd2c41f4a759?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1532009324734-20a7a5813719?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1524429656589-6633a470097c?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1530224264768-7ff8c1789d79?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1564135624576-c5c88640f235?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1541698444083-023c97d3f4b6?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1522364723953-452d3431c267?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1516972810927-80185027ca84?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1550439062-609e1531270e?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1549692520-acc6669e2f0c?w=1920&h=1080&fit=crop",
]




def download(image_url , path = "./image_dir") :
  response = requests.get(image_url)
  response.raise_for_status()
  os.makedirs(name = path , exist_ok=True )
  clean_name = os.path.basename(urlparse(image_url).path)
  filename= os.path.join(path , clean_name + ".jpg")
  with open(filename  , "wb") as f : 
    f.write(response.content)

  return f"completed download {image_url}"


def preprocess(path) :
  try : 
    img = Image.open(path)
  except Exception as e :
    raise RuntimeError("File path error")
  img = img.convert("RGB")
  img = img.resize((512,512))
  img.save(path)
  return("saved")  
  
async def preprocess_all () :
  loop = asyncio.get_running_loop()
  paths = []


  for dirs , _ , file_names in os.walk("./image_dir") :
    for file in file_names :
      paths.append(os.path.join(dirs,file))

  with ProcessPoolExecutor(max_workers=4) as executor :
    futures = [loop.run_in_executor(executor , preprocess ,path ) for path in paths]
    results = await asyncio.gather(*futures)
  
  print(results)
    
  
  
async def download_all() : 
  try:
   async with asyncio.TaskGroup() as tg :
      task = [tg.create_task(asyncio.to_thread(download , url)) for url in IMAGE_URLS ]  
  except* Exception as eg :
      for e in eg.exceptions :
        print("download_failed ",e)

 
if __name__ == "__main__" :
  asyncio.run(preprocess_all())

