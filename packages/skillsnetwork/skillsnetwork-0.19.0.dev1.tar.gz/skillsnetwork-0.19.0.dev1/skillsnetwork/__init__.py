import IPython

from pathlib import Path
from tqdm.auto import tqdm
from urllib.parse import urlparse

from os import environ


DEFAULT_CHUNK_SIZE = 8 << 10


def is_jupyterlite():
    return (
        environ.get("JUPYTERLITE").lower() == "true"
        if environ.get("JUPYTERLITE")
        else IPython.sys.platform == "emscripten"
    )


async def _get_chunks(url, chunk_size):
    desc = Path(urlparse(url).path).name
    if is_jupyterlite():
        import io
        from js import fetch

        response = await fetch(url)
        reader = response.body.getReader()
        pbar = tqdm(
            miniters=1, desc=desc, total=int(response.headers.get("content-length", 0))
        )
        while True:
            res = (await reader.read()).to_py()
            value, done = res["value"], res["done"]
            if done:
                break
            value = value.tobytes()
            yield value
            pbar.update(len(value))
        pbar.close()
    else:
        import requests

        with requests.get(url, stream=True) as response:
            pbar = tqdm(
                miniters=1,
                desc=desc,
                total=int(response.headers.get("content-length", 0)),
            )
            for chunk in response.iter_content(chunk_size=chunk_size):
                yield chunk
                pbar.update(len(chunk))
            pbar.close()


async def download(url, filename=None, chunk_size=DEFAULT_CHUNK_SIZE):
    if filename is None:
        filename = Path(urlparse(url).path).name
    with open(filename, "wb") as f:
        async for chunk in _get_chunks(url, chunk_size):
            f.write(chunk)
    print(f"Saved as {filename}")


async def read(url, chunk_size=DEFAULT_CHUNK_SIZE):
    return b"".join([chunk async for chunk in _get_chunks(url, chunk_size)])


if is_jupyterlite():
    tqdm.monitor_interval = 0

# For backwards compatibility
download_dataset = download
read_dataset = read
