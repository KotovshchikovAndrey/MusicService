from fastapi import APIRouter, Request, status
from fastapi.responses import StreamingResponse

from config.dependencies import ListenTrackDependency
from domain.dtos.inputs import ListenTrackDto

router = APIRouter(prefix="/tracks")


@router.get("/{track_oid:str}/listen")
async def listen_track(
    track_oid: str,
    request: Request,
    usecase: ListenTrackDependency,
):
    start_byte = 0
    end_byte = None

    content_range = request.headers.get("range")
    if content_range is not None:
        start_range, end_range = content_range.split("=")[-1].split("-")
        start_byte = int(start_range)
        if end_range:
            end_byte = int(end_range) + 1

    data = ListenTrackDto(oid=track_oid, start_byte=start_byte, end_byte=end_byte)
    output = await usecase.execute(data=data)

    return StreamingResponse(
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        content=output.stream,
        media_type=output.content_type,
        headers={
            "Accept-Ranges": "bytes",
            "Cache-Control": "no-cache",
            "Content-Length": output.content_length,
            "Content-Range": output.content_range,
        },
    )
