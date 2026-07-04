import asyncio
from concurrent.futures import ProcessPoolExecutor
import time
async def fetch(param) : 
  print("do something with ",param)
  await asyncio.sleep(param)
  return f"done with {param}"

async def main() : 
  coroutine1 = fetch(1)
  coroutine2 = fetch(2)
  results = await asyncio.gather(coroutine1 , coroutine2)
  print(results)

  async with asyncio.TaskGroup() as tg :
    task  = [tg.create_task(fetch(i))  for  i in range(1,3)] 
  result = [t for t in task]
  return result

if __name__=="__main__" : 
  t1 = time.perf_counter()
  result =asyncio.run(main())
  print(result)
  t2 = time.perf_counter()
  print(t2-t1)