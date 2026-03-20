from ninja import Router

from api.v1.admin.handlers import router as admin_router
from api.v1.auth.handlers import router as auth_router
from api.v1.posts.handlers import router as post_router
from api.v1.profile.handlers import router as profile_router


router = Router(tags=['v1'])

router.add_router('posts/', post_router)
router.add_router('profile/', profile_router)
router.add_router('auth/', auth_router)
router.add_router('admin/', admin_router)
