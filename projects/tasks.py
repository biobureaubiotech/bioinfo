from celery.decorators import task
from django.conf import settings

from projects.models import AlignmentFile, AlignmentHit


@task(name="sum_two_numbers")
def add(x, y):
    print('HELLO TASKS')
    print(x + y)
    return x + y

@task(name="import_alignment_to_database")
def import_alignment(alignment_file_id):
    
    print('Import FILE', alignment_file_id)

    aln_file = AlignmentFile.objects.get(pk=alignment_file_id)
    # print(aln_file.alnfile)

    infile = open('%s/%s' % (settings.MEDIA_ROOT, aln_file.alnfile))

    count = 0
    hits = []
    for line in infile:
        # print(line)

        #bulk insert variants objects
        if count == 5000:
            # print "Inserting %s " % (count2),
            AlignmentHit.objects.bulk_create(hits)
            # print ' Done!'
            count = 0
            hits = []
        
        hit = line.split('\t')
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

    AlignmentHit.objects.bulk_create(hits)

    
    aln_file.status = 'inserted'
    aln_file.save()
    print('Finished!')