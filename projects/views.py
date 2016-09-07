from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from projects.forms import UploadForm
from projects.models import Project, AlignmentFile, AlignmentHit, File, Task

from projects.tasks import import_alignment, process_task, start_instance, stop_instance, terminate_instance

from analyses.tasks import StartAnalysis

from django.contrib import messages
from django.db import transaction
from django.conf import settings

from analyses.models import Analysis, Instance
import boto3

import os

from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI

class ProjectList(LoginRequiredMixin, ListView):
    queryset = Project.objects.all()
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'description', 'prefix']
    success_url = reverse_lazy('project-list')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()        
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['name', 'description']
    success_url = reverse_lazy('project-list')
    def get_queryset(self):
        qs = super(ProjectUpdate, self).get_queryset()
        return qs.filter(user=self.request.user)

class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        # print('context')
        # print(context)
        # Add in a QuerySet of all the books
        context['alignment_files'] = AlignmentFile.objects.filter(project=context['project']).order_by('name')
        context['tasks'] = Task.objects.filter(project=context['project']).order_by('name')
        context['files'] = File.objects.filter(project=context['project']).order_by('name')
        context['instances'] = Instance.objects.filter(project=context['project'])
        context['analyses'] = Analysis.objects.filter(project=context['project'])

        return context

class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('project-list')

class UploadView(FormView):
    template_name = 'projects/fileupload.html'
    form_class = UploadForm
    # success_url = reverse_lazy('project-list')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        
        path = self.request.path
        path = path.split('/')
        project_id = path[2]
        
        for afile in self.request.FILES.getlist('file'):
            # print(afile.name)
            aln_file = AlignmentFile()
            aln_file.project = Project.objects.get(pk=project_id)
            aln_file.alnfile = afile
            aln_file.name = afile.name
            aln_file.status = 'new'
            aln_file.save()
            import_alignment.delay(aln_file.id)

        # form.send_email()
        return super(UploadView, self).form_valid(form)
    
    def get_success_url(self):

        path = self.request.path
        path = path.split('/')
        project_id = path[2]
        
        return reverse('project-detail', args=(project_id,))

def action(request):
    if request.method == 'POST':
        
        action = request.POST.get('action')
        # print(action)

        alignment_files = request.POST.getlist('alignment_files')

        if action == 'reinsert':    
            for aln_file in alignment_files:
                import_alignment.delay(aln_file)
            messages.add_message(request, messages.INFO, 'Files are being reinserted!')
        elif action == 'delete':
            for aln_file_id in alignment_files:
                
                aln_file = AlignmentFile.objects.get(pk=aln_file_id)
                #deleete hits
                AlignmentHit.objects.filter(alnfile=aln_file).delete()
                # print(aln_file.alnfile)
                full_path = '%s/%s' % (settings.MEDIA_ROOT, aln_file.alnfile)
                os.remove(full_path)
                AlignmentFile.objects.filter(pk=aln_file_id).delete()
            messages.add_message(request, messages.INFO, 'Files were deleted!')

    return redirect(request.META.get('HTTP_REFERER'))

def task_action(request, project_id):
    
    if request.method == 'POST':
    
        action = request.POST.get('action')
        tasks = request.POST.getlist('tasks')

        if action == 'rerun':
            for task_id in tasks:
                task = Task.objects.get(pk=task_id)
                process_task.delay(task.id)
            messages.add_message(request, messages.INFO, 'Tasks will be executed again!')
        elif action == 'delete':
            for task_id in tasks:
                task = Task.objects.get(pk=task_id)
                task.delete()
            
            messages.add_message(request, messages.INFO, 'Tasks were deleted!')

    return redirect('project-detail', project_id)

def analysis_action(request, project_id):
    
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

    return redirect('project-detail', project_id)

def instance_action(request, project_id):
    
    if request.method == 'POST':
    
        action = request.POST.get('action')
        instances = request.POST.getlist('instances')
        print(request.POST)
        print('instances',instances)
        if action == 'start':
            for instance_id in instances:
                start_instance.delay(instance_id)
            messages.add_message(request, messages.INFO, 'Instances are being started!')
        if action == 'stop':
            for instance_id in instances:
                stop_instance.delay(instance_id)
            messages.add_message(request, messages.INFO, 'Instances are being stopped!')
        elif action == 'terminate':
            for instance_id in instances:
                terminate_instance.delay(instance_id)
            
            messages.add_message(request, messages.INFO, 'Instances are being terminated!')
        elif action == 'delete':
            for instance_id in instances:
                instance = Instance.objects.get(pk=instance_id)
                instance.delete()
            
            messages.add_message(request, messages.INFO, 'Instances were deleted!')

    return redirect('project-detail', project_id)

def import_files(request, project_id):
    #get files form S3 Folder
    
    if request.method == 'POST':

        selected_files = request.POST.getlist('files')
        for file in selected_files:
            print(file)
            file_obj = File()
            file_obj.project = Project.objects.get(pk=project_id)
            file_obj.user = request.user
            file_obj.name = file
            file_obj.key = file

            file_obj.save()

        return redirect('project-detail', project_id)

        # form = ImportFileForm(request.data)





    else:
        
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('bioinfobiobureau')
        files = []
        for key in bucket.objects.filter(Prefix='input/'):
            files.append(key.key.replace('input/', ''))
        files = files[1:]

        # form = ImportFileForm()
        form = []

    return render(request, 'projects/file_import.html', {'form': form, 'files':files})



def import_files_from_basespace(request, project_id):
    #get files form S3 Folder
    project = Project.objects.get(pk=project_id)
    
    if request.method == 'POST':

        # print(request.POST)
        projects = request.POST.getlist('projects')
        # print(projects)

        if len(projects) > 0:
            # for basespace_project_name in projects:
            #add to task of imporintg project
            # print(basespace_project_name)
            task = Task()
            task.project = project
            task.user = request.user
            task.name = "Import Files from BaseSpace"
            task.task_type = "import_from_basespace"
            task.status = "new"
            task.task_data = {'projects':projects}
            task.save()
            # print('task.id', task.id)
            process_task.delay(task.id)

            # import_files_from_basespace_project.delay(project_id, basespace_project_name)
            return redirect('project-detail', project_id)


    myAPI = BaseSpaceAPI()
    projects = myAPI.getProjectByUser()
    # else:
        # s3 = boto3.resource('s3')
        # bucket = s3.Bucket('bioinfobiobureau')
        # files = []
        # for key in bucket.objects.filter(Prefix='input/'):
        #     files.append(key.key)
        # files = files[1:]

        # form = ImportFileForm()
        

    return render(request, 'projects/file_import_basespace.html', {'projects':projects})