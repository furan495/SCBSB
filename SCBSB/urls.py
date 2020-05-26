import os
from app import viewSet, views
from django.contrib import admin
from django.views.static import serve
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 创建路由器并注册我们的视图。
router = DefaultRouter()
router.register(r'api/roles', viewSet.RoleViewSet)
router.register(r'api/users', viewSet.UserViewSet)
router.register(r'api/events', viewSet.EventViewSet)
router.register(r'api/bomAnas', viewSet.BomAnaViewSet)
router.register(r'api/sections', viewSet.SectionViewSet)
router.register(r'api/projects', viewSet.ProjectViewSet)
router.register(r'api/problems', viewSet.ProblemViewSet)
router.register(r'api/progresses', viewSet.ProgressesViewSet)
router.register(r'api/departments', viewSet.DepartmentViewSet)

# API URL现在由路由器自动确定。
# 另外，我们还要包含可浏览的API的登录URL。
urlpatterns = [
    url(r'^upload/', views.upload),
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api/bomAna/', views.bomAna),
    url(r'^multUpload/', views.multUpload),
    url(r'^api/bomCheck/', views.bomCheck),
    url(r'^api/updatePwd/', views.updatePwd),
    url(r'^api/loginCheck/', views.loginCheck),
    url(r'^api/exportData/', views.exportData),
    url(r'^api/materials/', views.getMaterials),
    url(r'^api/updateProject/', views.updateProject),
    url(r'^api/analyseMaterial/', views.analyseMaterial),
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': BASE_DIR+'/static/appendix'}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
