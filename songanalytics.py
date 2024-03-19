from os import system as sy
from spotifydata import song_data_
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

p = print

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Analytics(BaseModel):
    album_link: str

p = print
sy('cls')

@app.post("/Album/")
async def analytics(request_data: Analytics):
    try:
        streams = song_data_(request_data.album_link,"BQALDD10IUXWDXD0VBMtzVWq5pNA-9n7cBMgu7oEePQllQMXJBrTdImAFCZJHjWUi_waij7qVIcBvlxwzaJQT_MmZrXmuZW3NxR9NpVmRWQd7ftQeJtIUIDb4OyXh604jsA2loeyMb6W89qjUDi1c5HtiioIe5FqOBm_5XqKakMUQdNXtLdSUub9CAugPt0L1po93P28V5fC9_WU5W2RhREqfWB9nGs2vNPR7SJ6KbZYEw2KO5SabOuf30jYsirheqyKaAMk0BCheiQwLxSUvfqtWXzTpxSxsUwZFJxM0YQZnLqfPX9GJguyRmUicjxfyVWzgmv3GqcvYdtjb6cVkWVbb-Q7IHYQ")

        return streams
    except KeyboardInterrupt:
        quit()
    except Exception as e:
        p(e)
        raise HTTPException(status_code=404, detail='Not Found')

if __name__ == "__main__":
    uvicorn.run("songanalytics:app", host="127.0.0.1", port=8000, reload=True)
