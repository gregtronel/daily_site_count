import os
import pdb

# declare some local file/dir names/paths
data_dirpath = 'data'
original_data_dirpath = os.path.join(data_dirpath, 'original')
last_data_dirpath = os.path.join(data_dirpath, 'latest')
updated_data_dirpath = 'data/updates'
spreadsheet_fname = 'Daily Site Counts - 2017.tsv'
links_fname = 'Daily Site Counts - Links.tsv'
pickled_fname = 'latest_scrape.pk'


config = {

    # define input and output filepaths a
    'spreadsheet_inpath': os.path.join(last_data_dirpath, spreadsheet_fname),
    'links_inpath': os.path.join(original_data_dirpath, links_fname),
    'spreadsheet_outpath_latest': os.path.join(last_data_dirpath, spreadsheet_fname),
    'spreadsheet_outpath_update': os.path.join(updated_data_dirpath, spreadsheet_fname),
    'pickled_datapath': os.path.join(data_dirpath, pickled_fname),

    # global flags
    '_UPDATE_SPREADSHEET': True,
    '_TRUNCATE_SPREADSHEET': True,
    '_WRITE_SPREADSHEET': True,

    # output spreadsheet columns
    'output_headers': [u'Date', u'Prod/Stage', u'Total skus', u'Total Digital', u'HL sku count', u'HX count', u'AP sku count', u'SMP Press sku count', u'time checked', u'notes', u'Sale 1 name', u'Sale 1 sku count', u'Sale 2 name', u'Sale 2 sku count', u'Sale 3 name', u'Sale 3 sku count', u'Sale 4 name', u'Sale 4 sku count', u'Sale 5 name', u'Sale 5 sku count', u'Sale 6 name', u'Sale 6 sku count', u'Sale 7 name', u'Sale 7 sku count', u'Sale 8 name', u'Sale 8 sku count']

}

if not os.path.isfile(config['spreadsheet_inpath']):
    config['spreadsheet_inpath'] = os.path.join(original_data_dirpath, spreadsheet_fname)

def get_config():
    return config
