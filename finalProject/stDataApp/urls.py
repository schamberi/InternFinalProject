from django.urls import path
from stDataApp.views import RawUpload, RawDataAPI,Prova,ProvaDyte,ProvaTrete

urlpatterns = [
    # ... your existing urlpatterns
    
    path('raw-upload/', RawUpload.as_view(), name='raw-upload'), #ketu prap ishte prove
    path('get-rawdata/', RawDataAPI.as_view(), name='raw-upload'), #ketu ishte prove
    path('prova/', Prova.as_view(), name='st-upload'),
    path('provadyte/', ProvaDyte.as_view(), name='sta-upload'),
    path('provatrete/', ProvaTrete.as_view(), name='stat-upload'),
    
]


