from django.http import Http404

from analyses.models import Analysis#, Task
from analyses.forms import AnalysisForm, AnalysisGBSSEForm
from analyses.tasks import StartAnalysis

from projects.models import Project
from django.shortcuts import render, redirect
from django.contrib import messages

import json

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

            analysis_type = form.cleaned_data['analysis_type']
            print('analysis_type', analysis_type)
            if analysis_type == 'gbs_se':
                return redirect('analysis-add-gbs-se', project_id)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnalysisForm()

    return render(request, 'analyses/analysis_add.html', {'form': form})

def add_gbs_se(request, project_id):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AnalysisGBSSEForm(request.POST, project_id=project_id)
        # check whether it's valid:
        if form.is_valid():

            analysis = form.save(commit=False)
            
            parameters = {
                'barcodes':form.cleaned_data['barcodes'],
                'adapters':form.cleaned_data['adapters'],
                'file':form.cleaned_data['file'].id
                }

            analysis.parameters = parameters
            project = Project.objects.get(pk=project_id)
            analysis.project = project
            analysis.user = request.user
            analysis.analysis_type = 'gbs_se'

            analysis.save()
            StartAnalysis.delay(analysis.id)

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return redirect('project-detail', project_id)
            # return HttpResponseRedirect('/thanks/')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnalysisGBSSEForm(project_id=project_id)

    return render(request, 'analyses/analysis_add.html', {'form': form})

def action(request):
    
    if request.method == 'POST':
        
        action = request.POST.get('action')
        analyses = request.POST.getlist('analyses')

        if action == 'rerun':
            for analsyis_id in analyses:
                analysis = Analysis.objects.get(pk=analsyis_id)
                StartAnalysis.delay(analysis.id)
            messages.add_message(request, messages.INFO, 'Analysis will be executed again!')

        elif action == 'delete':
            for analsyis_id in analyses:
                analysis = Analysis.objects.get(pk=analsyis_id)
                analysis.delete()
            
            messages.add_message(request, messages.INFO, 'Analysis were deleted!')

    return redirect('analysis-list')