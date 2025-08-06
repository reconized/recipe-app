from django.shortcuts import render
from django.views import View

class LockedOutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'locked_out.html')