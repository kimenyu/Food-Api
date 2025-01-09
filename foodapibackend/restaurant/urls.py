from .views import RestaurantListView, RestaurantCreateView, RestaurantDetailView, RestaurantUpdateView, RestaurantDeleteView, MenuItemListView, MenuItemCreateView, MenuItemUpdateView, MenuItemDeleteView, OrderListView, OrderCreateView, OrderDetailView, ReviewListView, ReviewCreateView, RestaurantReviewListView
from django.urls import path

urlpatterns = [
    # Restaurant URLs
    path('all/', RestaurantListView.as_view(), name='restaurant-list'),
    path('create/', RestaurantCreateView.as_view(), name='restaurant-create'),
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('<int:pk>/update/', RestaurantUpdateView.as_view(), name='restaurant-update'),
    path('<int:pk>/delete/', RestaurantDeleteView.as_view(), name='restaurant-delete'),

    # MenuItem URLs
    path('<int:restaurant_id>/menu-items/', MenuItemListView.as_view(), name='menu-item-list'),
    path('<int:restaurant_id>/menu-items/create/', MenuItemCreateView.as_view(), name='menu-item-create'),
    path('menu-items/<int:pk>/update/', MenuItemUpdateView.as_view(), name='menu-item-update'),
    path('menu-items/<int:pk>/delete/', MenuItemDeleteView.as_view(), name='menu-item-delete'),

    # Order URLs
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    # Review URLs
    path('<int:restaurant_id>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('<int:restaurant_id>/reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('my-restaurant/reviews/', RestaurantReviewListView.as_view(), name='restaurant-review-list'),
]