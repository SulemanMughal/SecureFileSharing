from django.urls import path



from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('t/<str:token>/<str:filename>', views.redirect_to_original_url, name="redirect_to_original_url"),
    path('t/<str:token>/', views.redirect_to_original_url, name="redirect_to_original_url"),
    path('manage/<str:document_id>', views.manage_files, name="manage_files_url"),
    path('abuse', views.abuse, name="abuse_url"),

    path('send_notification/', views.send_notification_to_telegram, name='send_notification'),



    


]