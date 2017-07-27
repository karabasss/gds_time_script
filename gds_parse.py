#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime

logs_folder = '/home/bass/MyDocs/ota_log_parse/logs'
logs_name_regex = 'gds'
logs_search_string = 'Got bookable product details request message'
results_filename = 'results'
total_result = []

def main(file):
    log_result = []
    for line in file:
        if logs_search_string in line:
            m = re.search('{PRODUCT_ID=(.+?)}', line)
            product_id = m.group(1)
            m2 = re.search('(\d{2}:\d{2}:\d{2},\d{3})', line)
            start_time = m2.group(1)
            for l in file:
                if "Product " + product_id in l:
                    mt = re.search('(\d{2}:\d{2}:\d{2},\d{3})', l)
                    end_time = mt.group(1)
                    writeResults(start_time,end_time)
                    diff = convertToDatetime(end_time) - convertToDatetime(start_time)
                    log_result.append(diff.total_seconds())
                    break
    if log_result:
        writeLogResults(log_result)

def openFile(log_file):
    global f
    f = open(log_file)

def writeResults(s,e):
    with open(results_filename, 'a') as f:
        diff = convertToDatetime(e) - convertToDatetime(s)
        result = s + ' ' + e + ' ' + str(diff.total_seconds()) + ' ' + log + "\n"
        f.write(result)

def writeLogResults(total_result):
    with open(results_filename, 'a') as f:
        f.write('\n')
        result = 'AVERAGE =                ' + str(round(sum(total_result) / float(len(total_result)), 3)) + "\n" + "\n"
        f.write(result)

def convertToDatetime(str_to_time):
    return datetime.strptime(str_to_time, '%H:%M:%S,%f')

def deleteContent(fName):
    with open(fName, "w"):
        pass

#######################################################################
#######################################################################

deleteContent(results_filename)  # Delete content before start
for log in os.listdir(logs_folder):
    if logs_name_regex in log:
        openFile(os.path.join(logs_folder, log))
        main(f)

        # break  #####                                       TEMP to read 1 file only     ################
