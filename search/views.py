

from projects.models import AlignmentHit
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Create your views here.
def search(request):
    if request.method == 'GET':
        print(request.GET)
        query = request.GET.get('search')
        print(query)

        if query != None:

            # q_object = 
            results_list = AlignmentHit.objects.filter(Q(Cluster_Name__icontains=query) | Q(Lowest_taxon_of_the_cluster__icontains=query))

        else:    
            results_list = []
            query = ''

        paginator = Paginator(results_list, 10) # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            results = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            results = paginator.page(paginator.num_pages)

    return render(request, 'search/search.html', {
        'results': results,
        'query': query
        })