from typing import Annotated
from fastapi import routing, File, UploadFile, status

router = routing.APIRouter(tags=["file"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_file(file: Annotated[bytes, File()]) -> dict:
    return {"file_size": len(file)}


@router.post("/upload", status_code=status.HTTP_201_CREATED, description="Upload a file")
async def create_upload_file(file: UploadFile) -> dict:
    return {"filename": file.filename, "content_type": file.content_type}