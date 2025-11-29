from api.v1.posts.handlers import router as post_router
from ninja import Router


router = Router(tags=['v1'])

router.add_router('posts/', post_router)
