from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html dir="ltr">
    <head>
        <title>سامانه زمانبندی کارکنان | Employee Timetable System</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 900px;
                margin: 50px auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 {
                margin: 0;
                font-size: 28px;
            }
            .header p {
                margin: 10px 0 0;
                opacity: 0.9;
            }
            .content {
                padding: 30px;
            }
            .section {
                margin-bottom: 30px;
            }
            .section h2 {
                color: #333;
                border-bottom: 2px solid #4CAF50;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }
            .links {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 15px;
            }
            .link-card {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
                transition: transform 0.2s, box-shadow 0.2s;
                text-decoration: none;
                display: block;
            }
            .link-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .link-card h3 {
                margin: 0 0 5px;
                color: #4CAF50;
            }
            .link-card p {
                margin: 0;
                color: #666;
                font-size: 12px;
            }
            .badge {
                display: inline-block;
                background: #4CAF50;
                color: white;
                font-size: 10px;
                padding: 2px 8px;
                border-radius: 10px;
                margin-top: 8px;
            }
            .footer {
                background: #f8f9fa;
                padding: 15px;
                text-align: center;
                color: #666;
                font-size: 12px;
                border-top: 1px solid #dee2e6;
            }
            .lang-switch {
                text-align: center;
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #dee2e6;
            }
            .lang-link {
                display: inline-block;
                margin: 0 10px;
                padding: 8px 16px;
                background: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
            .lang-link:hover {
                background: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 سامانه زمانبندی کارکنان</h1>
                <p>Employee Timetable Management System</p>
            </div>

            <div class="content">
                <div class="section">
                    <h2>📋 جداول عملکرد (Performance Tables)</h2>
                    <div class="links">
                        <a href="/api/performance-table/" class="link-card">
                            <h3>🇬🇧 English Table</h3>
                            <p>View performance records in English (LTR)</p>
                            <span class="badge">JSON API Available</span>
                        </a>
                        <a href="/api/performance-table-fa/" class="link-card">
                            <h3>🇮🇷 جدول فارسی</h3>
                            <p>مشاهده رکوردهای عملکرد به زبان فارسی (راست به چپ)</p>
                            <span class="badge">JSON API Available</span>
                        </a>
                    </div>
                </div>

                <div class="section">
                    <h2>🔌 API Endpoints (JSON)</h2>
                    <div class="links">
                        <a href="/api/staff/" class="link-card">
                            <h3>👥 Staff API</h3>
                            <p>/api/staff/</p>
                        </a>
                        <a href="/api/performance/" class="link-card">
                            <h3>📈 Performance API</h3>
                            <p>/api/performance/</p>
                        </a>
                        <a href="/api/position/" class="link-card">
                            <h3>🎯 Position API</h3>
                            <p>/api/position/</p>
                        </a>
                        <a href="/api/unit/" class="link-card">
                            <h3>🏢 Unit API</h3>
                            <p>/api/unit/</p>
                        </a>
                        <a href="/api/contract/" class="link-card">
                            <h3>📄 Contract API</h3>
                            <p>/api/contract/</p>
                        </a>
                        <a href="/api/status/" class="link-card">
                            <h3>⚙️ Status API</h3>
                            <p>/api/status/</p>
                        </a>
                        <a href="/api/month/" class="link-card">
                            <h3>📅 Month API</h3>
                            <p>/api/month/</p>
                        </a>
                        <a href="/api/year/" class="link-card">
                            <h3>📆 Year API</h3>
                            <p>/api/year/</p>
                        </a>
                    </div>
                </div>

                <div class="lang-switch">
                    <a href="/api-auth/login/" class="lang-link">🔐 Login</a>
                    <a href="/admin/" class="lang-link">⚙️ Admin Panel</a>
                    <a href="/api-auth/logout/" class="lang-link">🚪 Logout</a>
                </div>
            </div>

            <div class="footer">
                <p>© 2026 سامانه زمانبندی کارکنان | Employee Timetable System</p>
                <p>تعداد پرسنل: 75 | تعداد رکوردهای عملکرد: 2,474</p>
            </div>
        </div>
    </body>
    </html>
    """)


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('timetables.urls')),
    path('api/', include('timetables.login_urls')),
    path('api-auth/', include('rest_framework.urls')),
]