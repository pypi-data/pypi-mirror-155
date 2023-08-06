import os
import sys
from multiprocessing import Process
from typing import Union

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "..")
    sys.path.insert(0, os.path.normpath(SCRIPT_DIR))


def run_shitty_webserver(
    host: str = "0.0.0.0",
    port: int = 8000,
    random_seed: int = None,
    run_in_subprocess: bool = False,
) -> Union[None, Process]:
    if run_in_subprocess:

        p = Process(
            target=run_shitty_webserver,
            args=(
                host,
                port,
                random_seed,
                False,
            ),
            name="shittywebserver",
        )
        p.start()
        return p
    else:
        import uvicorn
        from shittywebserver.api import get_v1_router, tags_metadata
        from fastapi import FastAPI

        shittywebserver = FastAPI(openapi_tags=tags_metadata)
        shittywebserver.include_router(get_v1_router(random_seed), prefix="/v1")
        uvicorn.run(shittywebserver, host=host, port=port)


if __name__ == "__main__":
    from Configs import getConfig
    from shittywebserver.config import DEFAULT

    config: DEFAULT = getConfig()
    run_shitty_webserver(
        host=config.HOST,
        port=config.PORT,
        random_seed=config.RANDOM_SEED,
        run_in_subprocess=False,
    )
