from django.shortcuts import render_to_response

# Create your views here.

def get_resume_index(request):
    return render_to_response('index.html', {})
