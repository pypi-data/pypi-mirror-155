from typing import AsyncGenerator
import random
import time

from fastapi.responses import StreamingResponse
from starlette.types import Send
import asyncio


async def generate_random_bytes(
    size_bytes: int = 12288,
    chunk_size_bytes: int = 1024,
    seed: int = None,
) -> AsyncGenerator[bytes, None]:
    random.seed(seed)
    remaining_bytes = size_bytes
    while remaining_bytes > 0:

        chunk_size = (
            chunk_size_bytes if chunk_size_bytes < remaining_bytes else remaining_bytes
        )
        yield random.randbytes(chunk_size)
        remaining_bytes -= chunk_size


class InterruptableAndDecelerateableStreamingResponse(StreamingResponse):
    def set_interrupt_after_byte(self, interrupt_after_byte: int):
        self.interrupt_after_byte = interrupt_after_byte

    def set_every_chunk_wait_times(self, every_chunk_wait_time_sec: float):
        self.every_chunk_wait_time_sec = every_chunk_wait_time_sec

    async def stream_response(self, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )
        byte_count_send: int = 0
        interrupted: bool = False
        async for chunk in self.body_iterator:
            byte_count_send += len(chunk)
            if not isinstance(chunk, bytes):
                chunk = chunk.encode(self.charset)
            await send({"type": "http.response.body", "body": chunk, "more_body": True})
            if hasattr(self, "every_chunk_wait_time_sec") and isinstance(
                self.every_chunk_wait_time_sec, (float, int)
            ):
                await asyncio.sleep(self.every_chunk_wait_time_sec)
            if (
                hasattr(self, "interrupt_after_byte")
                and self.interrupt_after_byte
                and byte_count_send >= self.interrupt_after_byte
            ):
                interrupted = True
                break
        if not interrupted:
            await send({"type": "http.response.body", "body": b"", "more_body": False})
