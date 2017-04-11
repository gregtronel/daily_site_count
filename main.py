import os
import sys
import time
import datetime
import shutil
import numpy as np
import urlparse 
import pdb
from pprint import pprint

import config
import datautil
import parseutil


"""
    TASK: to automate a task that catalog performs manually: daily/weekly site counts of items. 
    
    INPUT: a .tsv (i.e, "data/latest/Daily Site Counts - 2017.tsv").
    This file is a tab-delimited export of the (similarly-named) spreadsheet maintained by catalog. 
    If the input file is not in data/latest/, the original file can be found in data/original/

    OUTPUT: a .tsv (i.e, "data/latest/Daily Site Counts - 2017.tsv")
    The output file is the same as the input file, where a new row is prepended on top.
    When the ouput is saved in data/latest/, a copy is also to data/updates/ for reversability and backlogging.

    NOTES: this update process is performed by scraping the smp websites (both stage and prod) 
    for counts of a particular item (e.g, total # of skus on website) and reports this information
    as a new row (on top) in the spreadsheet.
"""

# load config
config = config.get_config()

# custom lambdas
#flatten = lambda l: [item for sublist in l for item in sublist]   

""" --------------------------------------------------------------------------------------------------- """


def scrape_all(links, load_pickled=False):
    """
    """
    if load_pickled:
        if os.path.isfile(config['pickled_datapath']):
            return datautil.load_pickle(config['pickled_datapath'])
        else:
            print "cannot load pickled data because '{}' does not exist.\
                \nRe-scraping data instead".format(config['pickled_datapath'])
        
    headers = [col for col in links.keys()]
    scraped = {}
    for category,urls in links.items():
        print "\n{} start.".format(category)
        
        if urls['sales'] == 'No':
            stage = {urls['stage']: parseutil.parse_static_for_num_items(urls['stage'])}
            prod = {urls['prod']: parseutil.parse_static_for_num_items(urls['prod'])}

        elif urls['sales'] == 'Yes':
            # for "Sales", provided URL is parent URL of all the current sales.
            # since they are subject to change, a fixed (static) URL cannot be relied upon.
            # goal is therefore to descend through the child URLs of current sales categories 
            # and report the number of "items found" for each type of sale.
            stage = parseutil.parse_sales(urls[u'stage'])
            prod = parseutil.parse_sales(urls[u'prod'])

        scraped[category.lower()] = {u'stage':stage, u'prod':prod}
        print "{} finish.".format(category)
    print '\n'  
    # dump data to pickle locally so we don't have to scrape again when debugging
    datautil.dump_pickle(scraped, config['pickled_datapath'])
    
    return scraped
    


def update_spreadsheet(content, new_entry):
    """
    """
    # initilize row placeholders, append current date and 'stage' or 'prod'
    curdate = time.strftime("%m/%d/%Y")
    stage_row = [curdate] 
    stage_row.append('Stage')
    prod_row = [curdate] 
    prod_row.append('Prod')
    
    # if spreadsheet was already updated today, replace 2 entries with latest scrape.
    if content[1][0] == curdate:
        del content[2] # removing today's stage entry
        del content[1] # removing today's prod entry

    # populate each field for both the 'stage' and 'prod' rows
    _sales_done = False
    content[0] = config['output_headers']
    headers_lower = [h.lower() for h in content[0][2:]]
    sorted_stage_keys = np.sort(new_entry['sales landing page']['stage'].keys())
    sorted_prod_keys = np.sort(new_entry['sales landing page']['prod'].keys())
    for header in headers_lower:
        if header in new_entry.keys():
            stage_row.append(new_entry[header]['stage'].values()[0])
            prod_row.append(new_entry[header]['prod'].values()[0])
        
        elif header == "time checked":
            stage_row.append("{0} {1}".format(time.strftime("%I:%M"), time.strftime("%p")))
            prod_row.append("{0} {1}".format(time.strftime("%I:%M"), time.strftime("%p")))

        elif header == "notes":
            stage_row.append("")
            prod_row.append("")
            
        elif "sale" in header and not _sales_done:
            for k in sorted_stage_keys:
                stage_row.append(urlparse.urlsplit(k).path.split('/')[-2])
                stage_row.append(new_entry['sales landing page']['stage'][k])
            for k in sorted_prod_keys:
                prod_row.append(urlparse.urlsplit(k).path.split('/')[-2])
                prod_row.append(new_entry['sales landing page']['prod'][k])
            _sales_done = True
        
        else:
            continue

    # prepend new row to existing spreadsheet
    updated_content = [[] for _ in range(len(content)+2)]
    for idx,row in enumerate(updated_content):
        if not idx:
            updated_content[idx] = content[idx]
        elif idx == 1:
            updated_content[idx] = prod_row
        elif idx == 2:
            updated_content[idx] = stage_row
        else:
            break
    updated_content[idx:] = content[1:]
    
    return updated_content


def truncate_spreadsheet(content, ndays=30):
    cutoff_date = datetime.date.today() + datetime.timedelta(-ndays)
    content_rev_no_header = content[::-1][:-1]
    row_idx = len(content_rev_no_header)
    for row in content_rev_no_header: # [:-1] ignores the header row
        if 'b' in row[0]:
            row[0] = row[0].replace('17 b', '2017')
        date_obj = datetime.datetime.strptime(row[0], '%m/%d/%Y')
        if date_obj.date() < cutoff_date:
            del content[row_idx]
        row_idx -= 1
    
    return content


def main():
    # read-in data from spreadsheets
    spreadsheet_content = datautil.read_tsv(config['spreadsheet_inpath'])
    links_content = datautil.read_tsv(config['links_inpath'])
    links = datautil.format_links_content(links_content)

    # in the original spreadsheet, new entries were appended at the bottom -> we want them on top!
    if "original/" in config['spreadsheet_inpath']: 
        spreadsheet_content[1:] = spreadsheet_content[1:][::-1]

    # for each given URL, return the numbers of items found on page
    new_entry = scrape_all(links, load_pickled=True)
    print '- count data scraped.'

    # update existing spreadsheet with new data
    if config['_UPDATE_SPREADSHEET']:
        print "- updating spreadsheet."
        updated_content = update_spreadsheet(spreadsheet_content, new_entry)
    
    # truncate spreadsheet to only display "ndays" worth of history
    if config['_TRUNCATE_SPREADSHEET']:
        print "- truncating to keep only the last {} days.".format(config['ndays'])
        updated_content = truncate_spreadsheet(updated_content, ndays=config['ndays'])
    
    # dump the updated spreadsheet
    if config['_WRITE_SPREADSHEET']:
	outpath = config['spreadsheet_outpath_latest']
        print "- saving updated spreadsheet."
        datautil.write_tsv(updated_content, outpath)
	print "spreadsheet successfully updated and saved in: {}.\n".format(os.path.split(outpath)[0])
        shutil.copy(config['spreadsheet_outpath_latest'], 
                    config['spreadsheet_outpath_update'].replace('2017.tsv', time.strftime("%m-%d-%Y")+'.tsv'))


if __name__ == "__main__":
    main()  

