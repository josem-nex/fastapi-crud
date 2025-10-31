from typing import List, Any

def paginate_list(items: List[Any], page: int, per_page: int):
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    paged = items[start:end]
    return {
        "items": paged,
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page,
    }
