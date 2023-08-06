import concurrent.futures
from functools import partial
import requests
from tqdm import tqdm
from ..settings import GWLAB_FILE_DOWNLOAD_ENDPOINT


def _get_file_map_fn(file_id, file_path, progress_bar):
    download_url = GWLAB_FILE_DOWNLOAD_ENDPOINT + str(file_id)
    content = b''

    with requests.get(download_url, stream=True) as request:
        for chunk in request.iter_content(chunk_size=1024 * 16, decode_unicode=True):
            progress_bar.update(len(chunk))
            content += chunk
    return (file_path, content)


def _save_file_map_fn(file_id, file_path, progress_bar):
    download_url = GWLAB_FILE_DOWNLOAD_ENDPOINT + str(file_id)
    file_path.parents[0].mkdir(parents=True, exist_ok=True)

    with requests.get(download_url, stream=True) as request:
        with file_path.open("wb+") as f:
            for chunk in request.iter_content(chunk_size=1024 * 16):
                progress_bar.update(len(chunk))
                f.write(chunk)


def _download_files(map_fn, file_ids, file_paths, total_size):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        progress = tqdm(total=total_size, leave=True, unit='B', unit_scale=True)
        files = list(
            executor.map(
                partial(
                    map_fn,
                    progress_bar=progress
                ),
                file_ids, file_paths
            )
        )
        progress.close()
    return files
