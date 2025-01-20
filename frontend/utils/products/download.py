import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

import s3fs
from s3fs import S3FileSystem

from frontend.db.download_status import change_download_status, add_download

S3_GCS_ENDPOINT = 'https://storage.googleapis.com'
GCS_ESA_S2_BUCKET = 'gcp-public-data-sentinel-2'


class AsyncS3Copy:
    def __init__(
            self,
            source_fs: s3fs.S3FileSystem,
            dest_fs: s3fs.S3FileSystem,
            max_workers: int = 4
    ):
        self.source_fs = source_fs
        self.dest_fs = dest_fs
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def copy_file(self, source_path: str, dest_path: str):
        """Copy a single file asynchronously"""
        loop = asyncio.get_running_loop()

        def _copy():
            with self.source_fs.open(source_path, 'rb') as source:
                with self.dest_fs.open(dest_path, 'wb') as dest:
                    dest.write(source.read())

        await loop.run_in_executor(self.executor, _copy)

    def list_files(self, path: str):
        """List all files in directory recursively"""
        if path.endswith('/*'):
            path = path[:-2]
        if path.endswith('/'):
            path = path[:-1]

        files = []
        for filepath in self.source_fs.glob(f"{path}/**"):
            if not self.source_fs.isdir(filepath):
                files.append(filepath)
        return files

    async def copy_directory(self, source_path: str, dest_path: str):
        """Copy directory contents asynchronously"""
        files = self.list_files(source_path)
        tasks = []

        for file in files:
            relative_path = file.replace(source_path, '').lstrip('/')
            dest_file = f"{dest_path}/{relative_path}"

            # Ensure destination directory exists
            dest_dir = dest_file.rsplit('/', 1)[0]
            if not self.dest_fs.exists(dest_dir):
                self.dest_fs.makedirs(dest_dir)

            tasks.append(self.copy_file(file, dest_file))

        await asyncio.gather(*tasks)


async def download(s2_uri):
    gcs_s3 = S3FileSystem(anon=True,
                          endpoint_url=S3_GCS_ENDPOINT)

    vkr_s3 = S3FileSystem(endpoint_url=os.environ['S3_VKR_ENDPOINT'],
                          key=os.environ['S3_VKR_USER'],
                          secret=os.environ['S3_VKR_PASSWORD'])
    copier = AsyncS3Copy(gcs_s3, vkr_s3)

    await add_download(s2_uri)

    esa_mgrs_tile = s2_uri.split('_')[5][1:]
    utm_zone_latitude = esa_mgrs_tile[0:2]
    horizont = esa_mgrs_tile[2]
    vertical = esa_mgrs_tile[3:]

    s3_esa_s2_location = f'gcp-public-data-sentinel-2/tiles/{utm_zone_latitude}/{horizont}/{vertical}/{s2_uri}'

    await copier.copy_directory(s3_esa_s2_location, f'data-sentinel-2/{s2_uri}')

    await change_download_status(s2_uri)
