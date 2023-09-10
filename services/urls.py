from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'services'
urlpatterns = [
    path('services/', views.testing_service_list, name='services'),
    path('service_form/', views.create_service_testing, name= 'service_form'),
    path('serviceform/', views.create_service_testing1, name='serviceform'),
    path('services/service-detail/<int:id>', views.service_detail, name='service-detail'),
    path('services/search/', views.search_services, name='search'),
    path('', views.category, name='categories'),
    path('adding_categories', views.adding_categories, name='adding_categories'),
    path('categories/service_by_category/<int:id>/', views.services_by_categories, name='service_by_category'),
    path('services/update/<int:id>', views.update_service, name='update_service'),
    path('services/deleting/<int:id>', views.delete_service, name='delete_service'),
    path('categories/deleting_one_category/<int:id>', views.delete_category, name='deleting_one_category'),
    path('categories/deleting_all_categories/<int:id>', views.delete_all_categories, name='deleting_all_categories'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)