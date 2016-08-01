import zipfile

full_path = '/home/raony/dev/bitbucket/bioinfo_biobureau/bioinfo_biobureau/media/alignments/1/Achyrocline_alata_results.tab.zip'
# full_path = '/home/raony/dev/bitbucket/bioinfo_biobureau/bioinfo_biobureau/media/alignments/1/Casearia_sylvestris_results.tab.zip'

archive = zipfile.ZipFile(full_path, 'r')
filename = archive.namelist()[0]
infile = archive.open(filename, 'r')

for line in infile:
    hit = line.decode('utf-8').split('\t')
    
    # print(len(hit))
    # print(hit)

    if hit[0] == '17':
        print len(hit)
        print hit
        die()

    # if len(hit) < 19:
    #     diff = 19 - len(hit)
    #     # print diff
    #     for i in range(0,diff):
    #         hit.append('')

    # print(len(hit))
    # if len(hit) == 18:
    #     print(hit)
    #     print(hit[-1])
        # die()
    # print(hit[18])
    # if len(hit) == 19:
    #     print(hit[-1])