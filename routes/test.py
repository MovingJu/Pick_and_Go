from fastapi import APIRouter
import modules

router = APIRouter(
    prefix="/test",
    tags=["테스트 전용 엔드포인트임"]
)


@router.get("/image_compare")
async def image_compare(image1_link: str, image2_link: str):
    img_tool = modules.Image_comparison()

    features = img_tool.extract_features(
        image1_link,
    )
    features1 =img_tool.extract_features(
        image2_link,
    )

    return {"result" : float(modules.Image_comparison.cosine_similarity(
        features, features1
    ))}