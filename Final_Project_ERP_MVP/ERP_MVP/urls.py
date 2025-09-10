from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', include('users.api.urls')),
    path('api/teams/', include('teams.api.urls')),
    path('api/tasks/', include('tasks.api.urls')),
    path('api/meetings/', include('meetings.api.urls')),
    path('api/evaluations/', include('evaluations.api.urls')),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

    path('users/', include('users.urls')),
    path('tasks/', include('tasks.urls')),
    path('teams/', include('teams.urls')),
    path('evaluations/', include('evaluations.urls')),
    path('meetings/', include('meetings.urls')),
    path('calendar/', include('calendar_app.urls')),
    path('', RedirectView.as_view(pattern_name='user_detail',
                                  permanent=False))
]
