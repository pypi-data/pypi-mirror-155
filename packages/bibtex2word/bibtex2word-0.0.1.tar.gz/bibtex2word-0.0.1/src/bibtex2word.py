#!/usr/bin/env python3

import os,sys
from optparse import OptionParser
import xml.etree.cElementTree as ET

def create(bibtexfile, xmlfile):
    from pybtex.database.input import bibtex
    parser = bibtex.Parser()
    try:
        bibdata = parser.parse_file(bibtexfile)
    except NameError:
        print('Need an input filename. See --help')
        sys.exit(1)

    root = ET.Element('b:Sources', {'xmlns:b': "http://schemas.microsoft.com/office/word/2004/10/bibliography"""})
    if False:
        try:
            ET.register_namespace('', "http://schemas.microsoft.com/office/word/2004/10/bibliography")
            ET.register_namespace('b', "http://schemas.microsoft.com/office/word/2004/10/bibliography")
            root = ET.parse(options.inxml).getroot()
        except TypeError:
            root = ET.Element('b:Sources', {'xmlns:b': "http://schemas.microsoft.com/office/word/2004/10/bibliography"""})

    #print(bibdata)
    print(bibdata.entries)
    #help(bibdata)
    for key, entry in bibdata.entries.items():
        if False: #options.debug:
            print(key)
        source = ET.SubElement(root, 'b:Source')
        tag = ET.SubElement(source, 'b:Tag')
        tag.text = key
        b = bibdata.entries[key].fields

        srctypes = {'book': 'Book',
                    'article': 'ArticleInAPeriodical',
                    'incollection': 'ArticleInAPeriodical',
                    'inproceedings': 'ConferenceProceedings',
                    'misc': 'Misc',
                    'phdthesis': 'Report',
                    'techreport': 'Report'}

        try:
            srctype = ET.SubElement(source, 'b:SourceType')
            srctype.text = srctypes.get(entry.type, default='UNKNOWN')
        except KeyError:
            source.remove(srctype)

        def add_element(source, tagname, keyname):
            try:
                tag = ET.SubElement(source, tagname)
                tag.text = b[keyname]
            except KeyError:
                source.remove(tag)
            return source

        # mapping of MSFT tag to Bibtex field names
        xlate = (('b:Title', 'title'), ('b:Year', 'year'), ('b:City', 'city'),
                ('b:Publisher', 'publisher'), ('b:ConferenceName', 'organization'),
                ('b:URL', 'url'), ('b:BookTitle', 'booktitle'), ('b:ChapterNumber', 'chapter'),
                ('b:Edition', 'edition'), ('b:Institution', 'institution'), ('b:JournalName', 'journal'),
                ('b:Month', 'month'), ('b:Volume', 'number'), ('b:Pages', 'pages'), 
                ('b:Type', 'type'), ('b:URL', 'howpublished'))

        for msft, bibtex in xlate:
            source = add_element(source, msft, bibtex)

        authors0 = ET.SubElement(source, 'b:Author')
        authors1 = ET.SubElement(authors0, 'b:Author')
        namelist = ET.SubElement(authors1, 'b:NameList')
        for author in bibdata.entries[key].persons["author"]:
            person = ET.SubElement(namelist, 'b:Person')
            first = ET.SubElement(person, 'b:First')
            try:
                first.text = author.first()[0]
            except IndexError:
                first.text = ''
            last = ET.SubElement(person, 'b:Last')
            last.text = author.last()[0]

    # hack, unable to get register_namespace to work right when parsing the doc
    output = ET.tostring(root).decode("utf-8").replace('ns0:', 'b:').replace('ns0=', 'b=')
    try:
        with open(xmlfile, 'w+') as f:
            f.write(output)
    except TypeError:
        print(output)

def main():
    parser = OptionParser()
    #parser.add_option('-a', '--append', dest='inxml', action='store',help='existing filename (e.g. Sources.xml) to append elements to')
    #parser.add_option('-d', '--debug', dest='debug', action='store_true', default=False, help='debug (useful for broken .bib entries)')
    parser.add_option('-i', '--input', dest='bibtexfile', type='string', help='input bibtex filename', action='store')
    parser.add_option('-o', '--output', dest='xmlfile', type='string',default=sys.stdout,help='output filename', action='store')

    print('Starting')
    (options, args) = parser.parse_args()

    if len(args) > 0:
        print('Warning: extra arguments ignored: ' + ' '.join(args))
    create(options.bibtexfile, options.xmlfile)

if __name__ =='__main__':
    sys.exit(main())


