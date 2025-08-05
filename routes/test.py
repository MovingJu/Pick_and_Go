from fastapi import APIRouter
import modules

router = APIRouter(
    prefix="/test",
    tags=["테스트 전용 엔드포인트임"]
)


@router.get("/image_compare")
async def image_compare(image1_link: str, image2_link: str):


    features = modules.Image_comparison.extract_features(
        image1_link,
        modules.Image_comparison.get_feature_extractor()
    )
    features1 = modules.Image_comparison.extract_features(
        image2_link,
        modules.Image_comparison.get_feature_extractor()
    )

    return {"result" : float(modules.Image_comparison.cosine_similarity(
        features, features1
    ))}