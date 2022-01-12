from django.urls import path
from labrequests import views

urlpatterns = [
    # Requests View
    path('create/', views.CreateRequestView.as_view(), name='requests-create'),
    path('view/', views.ViewRequestsView.as_view(), name='requests-view'),
    path('manage/', views.ManageRequestsView.as_view(), name='requests-manage'),
    path('view/<cluster_id>/', views.ViewSingleRequestView.as_view(), name='view-single-request'),
    path('deny/<cluster_id>/', views.ViewSingleRequestView.as_view(), name='deny-request'),
    path('approve/<cluster_id>/', views.ViewSingleRequestView.as_view(), name='approve-request'),
    path('manage/<cluster_id>/', views.ManageSingleRequestView.as_view(), name='manage-single-request'),
    path('create/submit/', views.create_request),
]
