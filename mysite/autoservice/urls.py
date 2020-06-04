from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobiliai/<int:automobilis_id>', views.automobilis, name='automobilis'),
    path('uzsakymai/', views.UzsakymaiListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:pk>', views.UzsakymasDetailView.as_view(), name='uzsakymas'),
    path('search/', views.search, name='search'),
    path('search/<int:automobilis_id>', views.automobilis, name='automobilis'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
    path('manouzsakymai/', views.UzsakymaiByUserListView.as_view(), name='mano-uzsakymai'),
    path('manouzsakymai/<int:pk>', views.UzsakymaiByUserDetailView.as_view(), name='mano-uzsakymas'),
    path('manouzsakymai/naujas', views.UzsakymaiByUserCreateView.as_view(), name='naujas-uzsakymas'),
    path('manouzsakymai/<int:pk>/redaguoti', views.UzsakymaiByUserUpdateView.as_view(), name='redaguoti-mano-uzsakyma'),
    path('manouzsakymai/<int:pk>/istrinti', views.UzsakymaiByUserDeleteView.as_view(), name='istrinti-mano-uzsakyma'),
]
