from django.shortcuts import render

from projects.models import AlignmentHit

# Create your views here.
def search(request):
    if request.method == 'POST':
        print(request.POST)
        query = request.POST['search']
        print(query)
        results = AlignmentHit.objects.filter(Cluster_Name__icontains=query)
        # print(results)
    else:    
        pass
        results = {} 
        query = ''
    return render(request, 'search/search.html', {
        'results': results,
        'query': query
        })