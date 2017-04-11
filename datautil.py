import sys
import cPickle as pk
import codecs

"""
    Data utility script.
    Handles reading/formatting/writing the data files needed for daily_site_count.

"""

def dump_pickle(data, fname):
    """
    """
    with open(fname, 'wb') as f:
        pk.dump(data, f)

def load_pickle(fname):
    """
    """
    with open(fname, 'rb') as f:
        return pk.load(f)

def read_tsv(inpath):
    """
    """
    content = []
    with codecs.open(inpath, 'r', 'utf-8') as f:
        for row in f:
            row = row.split('\n')[0].split('\t')
            if '\r' in row[-1]:
                row[-1] = row[-1].replace('\r', '')
            content.append(row)
    return content

def write_tsv(content, outpath):
    """
    """
    with codecs.open(outpath, 'w', 'utf-8') as f:
        for row in content:
            f.write('\t'.join(row)+'\n')


def format_links_content(link_content):
    """ 
    """
    links = {}
    for idx,row in enumerate(link_content):   
        if not idx:
            continue # header row
        if row[-1]:
            links[row[0]] = {'prod':row[1], 'stage':row[2], 'sales':''}
            if 'Sales' in row[0]:
                links[row[0]]['sales'] = 'Yes'
            else:
                links[row[0]]['sales'] = 'No'
    return links
