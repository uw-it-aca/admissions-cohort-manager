import json

from django.http import HttpResponse
from django.views import View


class UploadView(View):
    def post(self, request):
        upload_file = request.FILES['file']
        upload_text = ""
        for line in upload_file:
            upload_text = upload_text + line.decode()
        return HttpResponse(upload_text)

