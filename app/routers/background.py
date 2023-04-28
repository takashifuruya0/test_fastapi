import time
from fastapi import routing, BackgroundTasks


router = routing.APIRouter(tags=["task"])


def write_log(message: str):
    time.sleep(5)
    with open("app/log.txt", mode="a") as log:
        log.write(message)


@router.get("/log/{message}/")
async def add_log(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, message)
    return {"message": message}