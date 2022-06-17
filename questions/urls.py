from .views import QuestionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("questions/", QuestionViewSet, basename="question")
urlpatterns = router.urls
