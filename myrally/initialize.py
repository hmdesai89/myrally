from myrally import ipc
from myrally import parse
import yaml
import os
import logging

def main(argv):

    #print os.path.abspath()
    file_name = argv[0]


    # create logger
    logger = logging.getLogger('myrally')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


    
    try:
        fh = open(file_name, 'r')
    except IOError:
        print "Error: can\'t find file or read data"

    doc = yaml.load(fh)
    logger.info( doc)
    #try:
    #     parse_dict = json.loads(fh)

    #except:
    #     print ('File is not in dict format')
    p = parse.Parser()
    p.start(doc)
    return True

    
