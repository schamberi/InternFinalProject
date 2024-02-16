from django.urls import path
from stDataApp.views import TryStoringExcel,DownloadRawData,StandartData

urlpatterns = [
    # ... your existing urlpatterns

    path('uploadexcel/', TryStoringExcel.as_view(), name='stat-upload'), #prov ok po sduhet ishte prove
    path('download-excel/<int:file_id>/', DownloadRawData.as_view(), name='download_excel'), #kjo duhet sepse i ben automatikisht download filet ne browser
    path('upload-file/', StandartData.as_view(), name='standard-upload'), #kjo duhet sepse kjo do bej mapimin 
    
]


