from django.urls import path
from labrequests import views

urlpatterns = [
    # Requests View
    path('create/', views.CreateRequestView.as_view(), name='requests-create'),
    path('view/', views.ViewRequestsView.as_view(), name='requests-view'),
    path('view/<cluster_id>/', views.ViewSingleRequestView.as_view(), name='view-single-request'),
    path('manage/', views.ManageRequestsView.as_view(), name='requests-manage'),
    path('manage/<cluster_id>/', views.ManageSingleRequestView.as_view(), name='manage-single-request'),
    path('create/submit/', views.create_request),
]
