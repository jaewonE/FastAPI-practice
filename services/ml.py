# services/ml.py
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Any

from fastapi import UploadFile

from error.exceptions import ImageNotFoundError, UnauthorizedError


class MLService:
    def __init__(self, *, storage_dir: str | Path = "S3") -> None:
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    async def predict(self, image: UploadFile, *, user_id: str) -> dict[str, Any]:
        # 파일명 생성: {user_id}-{upload_time}.{ext}
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        # includes leading dot, e.g. ".png"
        ext = Path(image.filename or "").suffix
        filename = f"{user_id}-{ts}{ext}" if ext else f"{user_id}-{ts}"
        save_path = self.storage_dir / filename

        content = await image.read()
        save_path.write_bytes(content)

        return {
            "url": str(save_path.as_posix()),
            "filename": filename,
            "size": len(content),
            "content_type": image.content_type,
        }

    def get_my_image_path(self, img_url: str, *, user_id: str) -> Path:
        # 단일 파일 이름만 허용하여 traversal 방지
        img_name = Path(img_url).name
        # 소유권 검증: 저장 규칙상 "{user_id}-..." 이어야 함
        if not img_name.startswith(f"{user_id}-"):
            raise UnauthorizedError()

        img_path = self.storage_dir / img_name
        if not img_path.exists() or not img_path.is_file():
            raise ImageNotFoundError()
        return img_path


# 싱글톤 인스턴스 & DI 팩토리
ml_service = MLService()


def get_ml_service() -> MLService:
    return ml_service
