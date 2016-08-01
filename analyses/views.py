from django.http import Http404
from django.shortcuts import render
from analyses.models import Analysis, Task

def analysis_list(request):
    analyses = Analysis.objects.all()
    # try:
    #     p = Poll.objects.get(pk=poll_id)
    # except Poll.DoesNotExist:
    #     raise Http404("Poll does not exist")
    return render(request, 'analyses/analysis_list.html', {'analyses': analyses})

def task_list(request):
    tasks = Task.objects.all()
    # try:
    #     p = Poll.objects.get(pk=poll_id)
    # except Poll.DoesNotExist:
    #     raise Http404("Poll does not exist")
    return render(request, 'analyses/task_list.html', {'tasks': tasks})
