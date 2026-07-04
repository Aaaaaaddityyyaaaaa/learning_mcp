import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

def fetch(param) : 
  print(f"do something with {param}")
  time.sleep(param)
  return f"done with {param}"

async def main() :
  task1 = asyncio.create_task(asyncio.to_thread(fetch , 1))
  task2 = asyncio.create_task(asyncio.to_thread(fetch,2))
  response1 = await task1
  print(response1)
  response2 = await task2
  print(response2)

  loop = asyncio.get_event_loop()
  with ProcessPoolExecutor(max_workers=4) as executor  :
    result1 = loop.run_in_executor(executor , fetch ,1 )
    result2 = loop.run_in_executor(executor ,fetch ,2 )
    print( await result1 )
    print( await result2 )
    


if __name__ == "__main__" : 
  t1 = time.perf_counter()
  asyncio.run(main())
  t2 = time.perf_counter()
  print("time taken : ",t2-t1)