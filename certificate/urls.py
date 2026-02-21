from django.urls import path
from .views.upload_certificate import CertificateUploadView


urlpatterns = [
    path(
    "upload/<int:event_id>/",CertificateUploadView.as_view(),name="bulk-certificate-upload"
)


]
