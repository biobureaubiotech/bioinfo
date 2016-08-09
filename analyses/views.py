from django.http import Http404

from analyses.models import Analysis#, Task
from analyses.forms import AnalysisForm
from analyses.tasks import StartAnalysis

from projects.models import Project


from django.shortcuts import render, redirect


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


def add(request, project_id):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AnalysisForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            project = Project.objects.get(pk=project_id)
            
            print('project', project.id)

            analysis = Analysis()
            analysis.user = request.user
            analysis.project = project

            analysis.name = form.cleaned_data['name']
            analysis.analysis_type = form.cleaned_data['analysis_type']

            analysis.description = form.cleaned_data['description']
            analysis.save()

            #delay pipeline execution
            StartAnalysis.delay(analysis.id)

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return redirect('analysis-list')
            # return HttpResponseRedirect('/thanks/')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnalysisForm()

    return render(request, 'analyses/analysis_add.html', {'form': form})