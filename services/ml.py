# services/ml.py
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Any

from fastapi import UploadFile

from error.exceptions import ImageNotFoundError, UnauthorizedError
from joblib import load
import numpy as np
from PIL import Image


class MLService:
    def __init__(self, *, storage_dir: str | Path = "S3") -> None:
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        # 모델 경로 및 지연 로딩 캐시
        project_root = Path(__file__).resolve().parents[1]
        self.model_path = project_root / "assets" / "ratron-random_forest_model.joblib"
        self._model = None

    def _ensure_model(self):
        """모델을 지연 로딩하여 재사용."""
        if self._model is None:
            # 신뢰된 파일만 로드(고정 경로)
            self._model = load(self.model_path.as_posix())
        return self._model

    async def predict(self, image: UploadFile, *, user_id: str) -> dict[str, Any]:
        # 파일명 생성: {user_id}-{upload_time}.{ext}
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        # includes leading dot, e.g. ".png"
        ext = Path(image.filename or "").suffix
        filename = f"{user_id}-{ts}{ext}" if ext else f"{user_id}-{ts}"
        save_path = self.storage_dir / filename

        content = await image.read()
        save_path.write_bytes(content)

        # ML 예측 수행: 업로드된 이미지를 전처리하여 입력으로 사용
        model = self._ensure_model()
        # 실제 이미지 기반 전처리: 회색조 28x28 → 평탄화(1, 784)
        try:
            with Image.open(save_path) as im:
                im = im.convert("L")
                im = im.resize((28, 28), Image.BILINEAR)
                arr = np.asarray(im, dtype=np.float32)  # 0..255 범위 유지
        except Exception as e:
            # 이미지 디코딩 실패 시 예외 전파(라우터에서 500 처리)
            raise e

        x = arr.reshape(1, 28 * 28)
        pred = model.predict(x)
        # JSON 직렬화를 위해 Python 기본 타입으로 변환
        try:
            predict_value: Any = pred[0].item()  # numpy 스칼라 → Python 스칼라
        except Exception:
            predict_value = (
                pred[0].tolist() if hasattr(pred[0], "tolist") else pred[0]
            )

        return {
            "url": str(save_path.as_posix()),
            "filename": filename,
            "size": len(content),
            "content_type": image.content_type,
            "predict": predict_value,
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
