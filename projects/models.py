from django.db import models

# Create your models here.
from bioinfo_biobureau.users.models import User

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    description = models.TextField()

    ALIGNER_CHOICES = (
        ('bwa', 'BWA'),
        ('diamond', 'DIAMOND'),
    )

    aligner = models.CharField(
        max_length=255,
        choices=ALIGNER_CHOICES
    )
    # database = 

    def __str__(self):
        return self.name


def alignment_file_name(instance, filename):
    return 'alignments/%s/%s' % (instance.project.id, filename)

class AlignmentFile(models.Model):
    project = models.ForeignKey(Project)
    alnfile = models.FileField(upload_to=alignment_file_name)#
    name = models.TextField()
    status = models.TextField()


class AlignmentHit(models.Model):
    project = models.ForeignKey(Project)
    alnfile = models.ForeignKey(AlignmentFile)

    qseqid = models.TextField()
    sseqid = models.TextField()
    pident = models.TextField()
    length = models.TextField()
    mismatch = models.TextField()
    gapopen = models.TextField()
    qstart = models.TextField()
    qend = models.TextField()
    sstart = models.TextField()
    send = models.TextField()
    evalue = models.TextField()
    bitscore = models.TextField()
    GI = models.TextField()
    GeneID = models.TextField()
    NCBI_taxon_of_the_reference = models.TextField()
    Lowest_taxon_of_the_cluster = models.TextField()
    RepID = models.TextField()
    Cluster_Name = models.TextField()
