from django.urls import path, re_path
from . import views


app_name = 'diary'

urlpatterns = [
    path('records/<int:pk>', views.RecordDetailView.as_view(), name='record_detail'),
    re_path(r'^records/(?P<date_from>.+)?(?P<date_to>.+)?(?P<is_important>.+)?',
            views.RecordListView.as_view(), name='records_list'),
    path('record_types/<int:pk>', views.RecordTypeDetailView.as_view(), name='recordtype_detail'),
    path('record_types', views.RecordTypeListView.as_view(), name='recordtype_list'),
    path('register', views.UserCreateView.as_view(), name='user_create'),
    path('login', views.UserLoginView.as_view(), name='user_login'),
    path('logout', views.UserLogoutView.as_view(), name='user_logout'),
]
