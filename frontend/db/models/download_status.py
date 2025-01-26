from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

from frontend.db.models.base import Base

class DownloadStatus(Base):

    __tablename__ = 'download_status'

    request: Mapped[str] = mapped_column(primary_key=True)
    downloaded: Mapped[bool] = mapped_column(Boolean)