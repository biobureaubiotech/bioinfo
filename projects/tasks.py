from celery.decorators import task
from projects.models import AlignmentFile
from django.conf import settings


@task(name="sum_two_numbers")
def add(x, y):
    print('HELLO TASKS')
    print(x + y)
    return x + y

@task(name="import_alignment_to_database")
def import_alignment(alignment_file_id):
    print('Import FILE', alignment_file_id)
    aln_file = AlignmentFile.objects.get(pk=alignment_file_id)
    print(aln_file.alnfile)
    infile = open('%s/%s' % (settings.MEDIA_ROOT, aln_file.alnfile))
    for line in infile:
        print(line)
    