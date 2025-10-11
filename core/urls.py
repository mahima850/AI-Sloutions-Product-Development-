from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('solutions/', views.solutions, name='solutions'),
    path('solutions/<int:solution_id>/', views.solution_detail, name='solution_detail'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('articles/', views.articles, name='articles'),
    path('gallery/', views.gallery, name='gallery'),
    path('events/', views.events, name='events'),
    path('add_article/', views.add_article, name='add_article'),
    path('add_event/', views.add_event, name='add_event'),
    path('add_gallery_item/', views.add_gallery_item, name='add_gallery_item'),
    path('articles/', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('events/', views.event_list, name='event_list'),
    path('gallery/', views.gallery, name='gallery'),
    
    
    # AJAX endpoints
    path('api/feedback/', views.submit_feedback, name='submit_feedback'),
    path('api/newsletter/', views.newsletter_signup, name='newsletter_signup'),
    path('api/chatbot/', views.chatbot_response, name='chatbot_response'),
    path('api/download-article/<int:article_id>/', views.download_article, name='download_article'),
    path('api/register-event/<int:event_id>/', views.event_registration, name='event_registration'),
]