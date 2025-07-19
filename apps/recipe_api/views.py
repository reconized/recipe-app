from django.shortcuts import render

def locked_out_view(request):
    return render(request, 'locked_out.html')