from django.shortcuts import render
from notice.models import Notice

def landing(request):
    recent_notices = Notice.objects.order_by('-pk')[:3]
    return render(
        request, 
        'single_pages/landing.html',
        {
            'recent_notices': recent_notices,
        }
    )

    
def about_me(requset):
    return render(
        requset, 
        'single_pages/about_me.html'
    )


# Create your views here.
