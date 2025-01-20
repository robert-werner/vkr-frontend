from frontend.db import async_session_local
from frontend.db.models.download_status import DownloadStatus


async def add_download(s2_uri: str):
    async with async_session_local() as session:
        async with session.begin():
            new_download = DownloadStatus(request=s2_uri,
                                          downloaded=False)
            session.add(new_download)
            await session.commit()

async def change_download_status(download_uri: str, status = True):
    async with async_session_local() as session:
        async with session.begin():
            download = await session.get(DownloadStatus, download_uri)
            download.downloaded = status
            await session.commit()

async def get_download_status(download_uri: str):
    async with async_session_local() as session:
        async with session.begin():
            download = await session.get(DownloadStatus, download_uri)
            if not download:
                return False
            return download.downloaded