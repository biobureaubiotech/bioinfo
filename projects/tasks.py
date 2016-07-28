from celery.decorators import task
from django.conf import settings

from projects.models import AlignmentFile, AlignmentHit

import zipfile

from django import db
from django.db import transaction

@task(name="sum_two_numbers")
def add(x, y):
    print('HELLO TASKS')
    print(x + y)
    return x + y


@task(name="import_alignment_to_database")
def import_alignment(alignment_file_id):
    
    print('Import FILE', alignment_file_id)

    aln_file = AlignmentFile.objects.get(pk=alignment_file_id)
    #delete hits from files before inserting
    AlignmentHit.objects.filter(alnfile=aln_file).delete()

    print(aln_file.alnfile)

    full_path = '%s/%s' % (settings.MEDIA_ROOT, aln_file.alnfile)

    if aln_file.name.endswith('.zip'):
        archive = zipfile.ZipFile(full_path, 'r')
        filename = archive.namelist()[0]
        infile = archive.open(filename, 'r')

    else:
        infile = open(full_path, 'r')

    count = 0
    
    
    hits = []
    for line in infile:
        
        count += 1

        # bulk insert variants objects
        if count == 10000:
            # with transaction.atomic():
            # print("Inserting ...")
            AlignmentHit.objects.bulk_create(hits)
            # db.reset_queries()
            # print ' Done!'
            count = 0
            del hits
            hits = []
        

        hit = line.decode('utf-8').split('\t')
        # print(hit)
        # print(len(hit))

        if hit[0] != 'qseqid':
        
            aln_hit = AlignmentHit()
            aln_hit.project = aln_file.project
            aln_hit.alnfile = aln_file

            aln_hit.qseqid = hit[0]
            aln_hit.sseqid = hit[1]
            aln_hit.pident = hit[2]
            aln_hit.length = hit[3]
            aln_hit.mismatch = hit[4]
            aln_hit.gapopen = hit[5]
            aln_hit.qstart = hit[6]
            aln_hit.qend = hit[7]
            aln_hit.sstart = hit[8]
            aln_hit.send = hit[9]
            aln_hit.evalue = hit[10]
            aln_hit.bitscore = hit[11]
            aln_hit.GI = hit[12]
            aln_hit.GeneID = hit[13]
            aln_hit.NCBI_taxon_of_the_reference = hit[14]
            aln_hit.Lowest_taxon_of_the_cluster = hit[15]
            aln_hit.RepID = hit[16]
            aln_hit.Cluster_Name = hit[17]

            # aln_hit.save()
            hits.append(aln_hit)

    # with transaction.atomic():
    # print("Inserting Final...")
    AlignmentHit.objects.bulk_create(hits)
    # db.reset_queries()
    del hits

    
    aln_file.status = 'inserted'
    aln_file.save()
    print('Finished!')