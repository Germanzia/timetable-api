from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect

def home(request):
    return HttpResponse("""
        <h1>Welcome to Timetable API</h1>
        <p>You are logged in!</p>
        <p>API endpoints:</p>
        <ul>
            <li><a href="/api/staff/">/api/staff/</a></li>
            <li><a href="/api/performance/">/api/performance/</a></li>
            <li><a href="/api/position/">/api/position/</a></li>
            <li><a href="/api/unit/">/api/unit/</a></li>
            <li><a href="/api/month/">/api/month/</a></li>
            <li><a href="/api/year/">/api/year/</a></li>
            <li><a href="/api/contract/">/api/contract/</a></li>
            <li><a href="/api/status/">/api/status/</a></li>
        </ul>
        <p><a href="/admin/">Django Admin</a></p>
        <p><a href="/api-auth/logout/">Logout</a></p>
    """)

urlpatterns = [
    path('', home),  # ← Add this line
    path('admin/', admin.site.urls),
    path('api/', include('timetables.urls')),
    path('api/', include('timetables.login_urls')),
    path('api-auth/', include('rest_framework.urls')),
]