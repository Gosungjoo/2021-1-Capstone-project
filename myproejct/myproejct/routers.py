from rest_framework import routers
import article.viewsets
router = routers.DefaultRouter()

router.register(r'article', article.viewsets.ArticleViewSet)