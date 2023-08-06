from time import sleep
from typing import List, Union, Dict
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import datetime
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from shittywebserver.tools import (
    generate_random_bytes,
    InterruptableAndDecelerateableStreamingResponse,
)
import uuid
import asyncio
import time

tags_metadata = [
    {
        "name": "Shitty",
        "description": "Weird and bad webserver behaviour",
    },
    {
        "name": "Normal",
        "description": "Expected webserver behaviour",
    },
]


def get_v1_router(randomizer_seed: int = 346245):
    v1router = APIRouter()
    GLOBAL_REG: Dict = {}

    @v1router.get(
        "/download/static-content-static-etag",
        tags=["Normal"],
        response_class=StreamingResponse,
        description="Download a static byte sequence with a static etag",
        # name="List all existing requests",
    )
    async def serve_static_content_with_static_etag(size_bytes: int = 1048576):
        headers: Dict = {}
        headers["Content-Length"] = str(size_bytes)
        headers["Content-Disposition"] = 'attachment; filename="rand_bytes.bytes"'
        headers["etag"] = "43098534032456436745"
        return StreamingResponse(
            generate_random_bytes(size_bytes=size_bytes, seed=randomizer_seed),
            media_type="application/octet-stream",
            headers=headers,
        )

    @v1router.get(
        "/download/static-content-random-etag",
        tags=["Shitty"],
        response_class=StreamingResponse,
        description="Download a static byte sequence, but changes the etag every request",
        # name="List all existing requests",
    )
    async def serve_static_content_with_random_etag(size_bytes: int = 1048576):
        headers: Dict = {}
        headers["Content-Length"] = str(size_bytes)
        headers["Content-Disposition"] = 'attachment; filename="rand_bytes.bytes"'
        headers["etag"] = uuid.uuid4().hex
        return StreamingResponse(
            generate_random_bytes(size_bytes=size_bytes, seed=randomizer_seed),
            media_type="application/octet-stream",
            headers=headers,
        )

    @v1router.get(
        "/download/random-content-static-etag",
        tags=["Shitty"],
        response_class=StreamingResponse,
        description="Download random byte sequence, but have a static etag",
        # name="List all existing requests",
    )
    async def serve_random_content_with_static_etag(size_bytes: int = 1048576):
        headers: Dict = {}
        headers["Content-Length"] = str(size_bytes)
        headers["Content-Disposition"] = 'attachment; filename="rand_bytes.bytes"'
        headers["etag"] = "f4bf80b6e788464780be6f6d600de9cb"
        return StreamingResponse(
            generate_random_bytes(size_bytes=size_bytes, seed=None),
            media_type="application/octet-stream",
            headers=headers,
        )

    @v1router.get(
        "/download/interrupted",
        tags=["Shitty"],
        response_class=StreamingResponse,
        description="Serve random byte sequence, but suddenly stop",
        # name="List all existing requests",
    )
    async def serve_file_but_interrupt_midstream(
        size_bytes: int = 1048576,
        interrupt_every_n_download: int = 2,
        interrupt_at_byte: int = 524288,
    ):
        if not "serve_file_but_interrupt" in GLOBAL_REG:
            GLOBAL_REG["serve_file_but_interrupt"] = 0
        else:
            GLOBAL_REG["serve_file_but_interrupt"] += 1
        headers: Dict = {}
        headers["Content-Length"] = str(size_bytes)
        headers["Content-Disposition"] = 'attachment; filename="rand_bytes.bytes"'
        headers["etag"] = "f4bf80b6e788464780be6f6d600de9cb"

        resp = InterruptableAndDecelerateableStreamingResponse(
            generate_random_bytes(size_bytes=size_bytes, seed=None),
            media_type="application/octet-stream",
            headers=headers,
        )
        if GLOBAL_REG["serve_file_but_interrupt"] % interrupt_every_n_download == 0:
            resp.set_interrupt_after_byte(interrupt_at_byte)
        return resp

    @v1router.get(
        "/download/slow",
        tags=["Shitty"],
        response_class=StreamingResponse,
        description="Serve file but very slow",
        name="Serve file but very slow",
    )
    async def serve_file_with_pauses(
        size_bytes: int = 1048576,
        chunk_wait_time: float = 0.02,
    ):
        headers: Dict = {}
        headers["Content-Length"] = str(size_bytes)
        headers["Content-Disposition"] = 'attachment; filename="rand_bytes.bytes"'
        headers["etag"] = "f4bf80b6e788464780be6f6d600de9cb"

        resp = InterruptableAndDecelerateableStreamingResponse(
            generate_random_bytes(size_bytes=size_bytes, seed=None),
            media_type="application/octet-stream",
            headers=headers,
        )
        resp.set_every_chunk_wait_times(chunk_wait_time)

        return resp

    @v1router.get(
        "/download/disappear",
        tags=["Shitty"],
        response_class=StreamingResponse,
        description="Download file at url, which will be disappear at next download (404)",
        # name="List all existing requests",
    )
    async def serve_file_but_disappear(
        size_bytes: int = 1048576,
        disappear_every_n_download: int = 2,
    ):
        if not "serve_file_but_disappear" in GLOBAL_REG:
            GLOBAL_REG["serve_file_but_disappear"] = 0
        else:
            GLOBAL_REG["serve_file_but_disappear"] += 1
        headers: Dict = {}
        headers["Content-Length"] = str(size_bytes)
        headers["Content-Disposition"] = 'attachment; filename="rand_bytes.bytes"'
        headers["etag"] = "f4bf80b6e788464780be6f6d600de9cb"

        if GLOBAL_REG["serve_file_but_disappear"] % disappear_every_n_download == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            return StreamingResponse(
                generate_random_bytes(size_bytes=size_bytes, seed=None),
                media_type="application/octet-stream",
                headers=headers,
            )

    @v1router.get(
        "/download/do-nothing",
        tags=["Shitty"],
        description="Just do nothing and end in a timeout",
        # name="List all existing requests",
    )
    async def just_do_nothing(
        timeout_after_sec=60,
    ):
        timeout = False
        start: float = time.time()
        while not timeout:
            await asyncio.sleep(1)
            if start - time.time() > timeout_after_sec:
                timeout = True
        return

    @v1router.get(
        "/download/do-nothing-and-error",
        tags=["Shitty"],
        description="Just do nothing and error",
        # name="List all existing requests",
    )
    async def just_do_nothing_and_scream_afterwards(
        timeout_after_sec=5,
    ):
        timeout = False
        start: float = time.time()
        while not timeout:
            await asyncio.sleep(1)
            if start - time.time() > timeout_after_sec:
                timeout = True
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @v1router.get(
        "/download/too-many-requests",
        tags=["Shitty"],
        response_class=StreamingResponse,
        description="Simulates an endpoint that is very sensibel with request counts",
        # name="List all existing requests",
    )
    async def serve_files_but_moan_often(
        size_bytes: int = 1048576,
        moan_every_n_download: int = 2,
        demand_retry_after_time_sec: int = 2,
    ):
        if not "too-many-requests" in GLOBAL_REG:
            GLOBAL_REG["too-many-requests"] = {}
            GLOBAL_REG["too-many-requests"]["download-count"] = -1
        elif (
            GLOBAL_REG["too-many-requests"]["download-count"] % moan_every_n_download
            == 0
            and time.time() - GLOBAL_REG["too-many-requests"]["last-download-time"]
            < demand_retry_after_time_sec
        ):

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                headers={
                    "Retry-After": demand_retry_after_time_sec
                    - (
                        time.time()
                        - GLOBAL_REG["too-many-requests"]["last-download-time"]
                    )
                },
            )
        headers: Dict = {}
        headers["Content-Length"] = str(size_bytes)
        headers["Content-Disposition"] = 'attachment; filename="rand_bytes.bytes"'
        headers["etag"] = "7d3bdcec9fe545f990de46c3bfed651a"
        GLOBAL_REG["too-many-requests"]["download-count"] += 1
        GLOBAL_REG["too-many-requests"]["last-download-time"] += time.time()
        return StreamingResponse(
            generate_random_bytes(size_bytes=size_bytes, seed=randomizer_seed),
            media_type="application/octet-stream",
            headers=headers,
        )

    return v1router
