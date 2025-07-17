from fastapi import APIRouter

router = APIRouter(
    tags=["Pick and Go main services"]
)

@router.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None) -> dict[str, int | str | None]:
    return {"item_id": item_id, "q": q}