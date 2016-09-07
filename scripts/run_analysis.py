#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from subprocess import call
import json
import pprint

class PrepareSeqs():

    def __init__(self, name):
        self.name = name
        self.tricks = []    # creates a new empty list for each dog
        
        json_data=open('parameters.json').read()
        self.parameters = json.loads(json_data)
        # print(data)
        #create dirs
        dirs = ['input', 'ouput', 'programs']
        for dir_path in dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        self.start_path = os.getcwd()

        self.fastq = os.path.splitext(self.parameters['aws'][0]['name'])[0]

        #write barcodes
        barcodes = self.parameters['analysis']['parameters']['barcodes']
        barcodes_file = open('input/barcodes.txt', 'w')
        
        for line in barcodes:
            barcodes_file.writelines(line)
            # self.species.append(line.split(' ')[1])
        self.species = []
        for line in barcodes.splitlines():
            self.species.append(line.split(' ')[1].split('.')[0])
        barcodes_file.close()

        #adapters
        self.adapters = self.parameters['analysis']['parameters']['adapters'].splitlines()
        # print('adapters', self.adapters)



    def install_requirements(self):

        command = 'sudo apt-get update'
        call(command, shell=True)
        command = 'sudo apt-get -y upgrade'
        call(command, shell=True)
        command = 'sudo apt-get -y install s3cmd git make htop gcc virtualenvwrapper python-dev locate python-pip zlib1g-dev'
        call(command, shell=True)
        command = 'sudo pip install cutadapt'
        call(command, shell=True)
        
        os.chdir('programs')
        command = 'git clone https://github.com/najoshi/sabre.git'
        call(command, shell=True)
        os.chdir('sabre')
        command = 'make'
        call(command, shell=True)
        os.chdir(self.start_path)

        # command = "wget -nc http://spades.bioinf.spbau.ru/release3.9.0/SPAdes-3.9.0-Linux.tar.gz"


    def run(self):
        
        # self.install_requirements()
        # self.download_fastq()
        # self.demultiplexing()
        # self.removeadapters()
        #upload results to S3
        self.upload_to_s3()

    def download_fastq(self):
        print('Download FASTQ')

        os.chdir('input')

        aws = self.parameters['aws']
        for file in aws:
            # command = """wget -c "%s" -O input/%s""" % (file['link'], file['name'])
            # print(command)
            command = "s3cmd get --progress --continue s3://bioinfobiobureau/input/%s" % (file['name'])
            output = call(command, shell=True)
            
            print(output)
            print("Extract FASTQ")
            name = os.path.splitext(file['name'])[0]
            print(name)
            command = "gunzip -c %s > %s" % (file['name'], name)
            output = call(command, shell=True)            
            print(output)

        os.chdir('../')
    def demultiplexing(self):
        print('Demultiplexing')
        path = 'output/demultiplexing'
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        print(os.getcwd())
        command = '../../programs/sabre/sabre se -f ../../input/%s -b ../../input/barcodes.txt -m 1 -u unknown_barcode.fastq' % (self.fastq)
        output = call(command, shell=True)            
        print(output)
    def removeadapters(self):
        print('Removing Adapters')
        os.chdir(self.start_path)
        path = 'output/removeadapters'
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        for specie in self.species:
            # print(specie)
            command = 'cutadapt -b %s -b %s -e 0.1 -o %s.cutadapt.fastq ../demultiplexing/%s.fastq 1>%s.report.txt' % (self.adapters[0], self.adapters[1], specie, specie, specie)
            print(command)
            output = call(command, shell=True)
            print(output)

    def upload_to_s3(self):
        print('Upload results to S3')
        os.chdir(self.start_path)
        path = 'output/demultiplexing'
        os.chdir(path)
        command = "gzip *.fastq"
        output = call(command, shell=True)
        os.chdir(self.start_path)
        path = 'output/removeadapters'
        os.chdir(path)
        command = "gzip *.fastq"
        output = call(command, shell=True)
        os.chdir(self.start_path)
        command = "s3cmd sync output s3://bioinfobiobureau/output/analysis_%s/" % (self.parameters['analysis']['id'])
        output = call(command, shell=True)




if __name__ == '__main__':
    name = 'Bioinfo'
    bioinfo = PrepareSeqs(name)
    bioinfo.run()