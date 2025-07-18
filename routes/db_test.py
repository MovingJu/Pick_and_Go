from fastapi import APIRouter

router = APIRouter(
    prefix="/db",
    tags=["testing db functions"]
)

@router.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None) -> dict[str, int | str | None]:
    return {"item_id": item_id, "q": q}