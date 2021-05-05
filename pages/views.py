from django.shortcuts import render
from deployments.models import deployment

def index(request):
    # listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]

    # context = {
    #     'listings': listings,
    #     'state_choices': state_choices,
    #     'bedroom_choices':bedroom_choices,
    #     'price_choices':price_choices
    # }

    return render(request, 'pages/index.html')#, context)

def status(request):
    deployments = deployment.objects.all()

    context = {
        'deployments': deployments,
    }

    return render(request, 'pages/status.html', context)