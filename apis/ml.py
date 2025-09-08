from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from auth.auth_bearer import JWTBearer
from services.ml import MLService, get_ml_service


# 메인 라우터: 전역 JWT 인증 적용
router = APIRouter(
    prefix="/ml",
    tags=["ml"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(JWTBearer())],
)


@router.post(
    "/predict",
    summary="이미지 업로드 후 예측 결과 반환",
)
async def predict(
    image: UploadFile = File(...),
    user_id: str = Depends(JWTBearer()),
    svc: MLService = Depends(get_ml_service),
):
    try:
        result = await svc.predict(image, user_id=user_id)
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")


@router.get(
    "/myImg/{img_url}",
    summary="저장한 이미지 반환",
)
async def my_img(
    img_url: str,
    user_id: str = Depends(JWTBearer()),
    svc: MLService = Depends(get_ml_service),
):
    img_path = svc.get_my_image_path(img_url, user_id=user_id)
    return FileResponse(img_path, media_type="image/png")
