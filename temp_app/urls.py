from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from temp_app import views

urlpatterns = [
    path('create_app/', views.CreateTempAppMaster.as_view()),
    path('create_app_step_one/<pk>/', views.BusinessLogoUploadAndStepOneView.as_view()),
    path('create_app_step_two/<session>/', views.CreateTempUsersAndStepTwoView.as_view()),
    path('create_app_step_three/', views.MultipleUploadImgAndStepThreeView.as_view()),
    path('create_app_step_last/<pk>/', views.UserRegistrationAndStepLastView.as_view()),
    path('create_app_details/<appmaster_id>/', views.TempAppDetailsView.as_view()),
    path('create_app_details_by_session/<session>/', views.TempAppMasterListDetailBySessionView.as_view()),
    path('app_user_details/<session>/', views.TempUsersDetailView.as_view()),
    path('update_category_maping/<pk>/', views.UpdateTempAppCategoryMapingsById.as_view()),
    path('edit_category_maping/<pk>/', views.CategoryMapingsUpdate.as_view()),
    path('all_local_appmaster/', views.TempAppMasterListView.as_view()),
    path('insert_app_url/<pk>/', views.InsertAppUrlTempAppMasterView.as_view()),
    path('create_product_category/', views.CreateTempAppProductCategoriesView.as_view()),
    path('create_product/', views.CreateTempAppProductView.as_view()),
    path('all_product/', views.TempAppProductListView.as_view()),
    path('all_product/<pk>/', views.TempAppProductByIdView.as_view()),
    path('search_product_by_category/<categort_id>/', views.SearchTempAppProductByCategoryView.as_view()),
    path('edit_product_category/<pk>/', views.EditTempAppProductCategoriesView.as_view()),
    path('add_category_product/', views.AddCategoryAndProductView.as_view()),
    path('edit_product_Categories/<appmaster_id>/', views.EditTempAppProductCategoriesView.as_view()),
    path('edit_product/<appmaster_id>/', views.EditTempAppProductsView.as_view()),

]