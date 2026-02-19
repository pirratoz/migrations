from pathlib import Path
import hashlib

import aiofiles


class SqlFile:
    def __init__(self, file: str | Path):
        self.path = Path(file).resolve()
        self._content: bytes | None = None

        if self.path.suffix.lower() != ".sql":
            raise ValueError(f"File ({file}) must be a .sql file.")
            
        if not self.path.is_file():
            raise FileNotFoundError(f"File not found: {self.path.absolute()}")

    async def _get_raw_data(self) -> bytes:
        if self._content is None:
            async with aiofiles.open(self.path.absolute(), mode="rb") as fp:
                self._content = await fp.read()
        return self._content

    async def read(self) -> str:
        data = await self._get_raw_data()
        return data.decode("utf-8")
    
    async def get_checksum(self) -> str:
        data = await self._get_raw_data()
        return hashlib.sha256(data).hexdigest()
