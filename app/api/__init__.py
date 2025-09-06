from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.api.apiRoutes import users,auth,operatorRoutes,productListRoute,webchatRoute
router = APIRouter()

router.include_router(users.userController,prefix='/user')
router.include_router(auth.authController,prefix='/auth')
router.include_router(operatorRoutes.operatorController,prefix='/operator')
router.include_router(productListRoute.productListController,prefix='/product')
router.include_router(webchatRoute.webchatController,prefix='/ws')