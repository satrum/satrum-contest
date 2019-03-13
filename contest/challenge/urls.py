from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	#path('signup/', views.SignUp.as_view(), name='signup'),
	path('signup/', views.signup, name='signup'),
	path('contests/', views.ContestListView.as_view(), name='contests'),
	path('contests/<int:pk>', views.ContestDetailView.as_view(), name='contest-detail'),
	path('contests/<int:pk>/lb', views.ContestLBView.as_view(), name='contest-lb'),
	path('contests/<int:pk>/sub', views.ContestSubmitView.as_view(), name='contest-submits'),
	path('contests/<int:pk>/upload', views.submit_upload, name='submit-upload'),
	]