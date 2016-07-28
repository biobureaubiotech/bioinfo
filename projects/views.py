from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from projects.forms import UploadForm
from projects.models import Project, AlignmentFile

from projects.tasks import import_alignment
from django.contrib import messages
from django.db import transaction


class ProjectList(LoginRequiredMixin, ListView):
    queryset = Project.objects.all()
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'description', 'aligner']
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
        # print(dir(request))
        # print(request.META)
        
        alignment_files = request.POST.getlist('alignment_files')
        # first_object = alignment_files[0]
        # aln_object = AlignmentFile.objects.get(pk=first_object)
        # project_id = aln_object.project.id
        for aln_file in alignment_files:
            import_alignment.delay(aln_file)
        messages.add_message(request, messages.INFO, 'Files being reinserted!')

    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect(reverse('project-detail', kwargs={'pk': project_id}))

