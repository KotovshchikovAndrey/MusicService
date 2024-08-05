from fastapi import APIRouter

from adapters.rest.v1.track.routes import router as track_router

router = APIRouter(prefix="/v1")
router.include_router(track_router)
