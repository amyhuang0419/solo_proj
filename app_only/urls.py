from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    # path('login_page', views.login_page),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('login_register', views.login_page),
    path('user_dashboard', views.user_dashboard),
    path('create_sneaker_page', views.create_sneaker_page),
    path('create_sneaker', views.create_sneaker),

    path('sneakers/<int:sneaker_id>/delete', views.delete_sneaker),
    path('sneakers/<int:comment_id>/delete_comment', views.delete_comment),

    path('sneakers/<int:sneaker_id>/edit_page', views.edit_sneaker_page),
    path('sneakers/<int:sneaker_id>/edit', views.edit_sneaker),

    path('like/<int:sneaker_id>', views.like),
    path('unlike/<int:sneaker_id>', views.unlike),

    path('survey', views.survey),

    path('unlike/<int:sneaker_id>/user_dashboard', views.unlike_in_user_dashboard),
    path('like/<int:sneaker_id>/survey_page', views.like_in_survey_page),
    path('unlike/<int:sneaker_id>/survey_page', views.unlike_in_survey_page),

    path('sneakers/<int:sneaker_id>/upload_comment', views.upload_comment),
    path('upload_image', views.upload_image),
    path('sneakers/<int:sneaker_id>', views.sneaker_dashboard),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)