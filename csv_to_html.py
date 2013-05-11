# -*- coding: utf-8 -*-
from __future__ import division
import re

__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

class CsvToHtml(object):
    def htmlOutputTable(self, output_csv, output_html):
        r = 0
        output_html.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
        output_html.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
        output_html.write('<head>\n')
        output_html.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
        output_html.write('<title>Fuzzy Input Data</title>\n')
        output_html.write('<style type="text/css">\n')
        output_html.write('<!--\n')
        output_html.write('@import url("style.css");\n')
        output_html.write('-->\n')
        output_html.write('</style>\n')
        output_html.write('</head>\n')
        output_html.write('<body>\n')
        output_html.write('<table id="box-table-a" summary="Fuzzy Input Data">\n')
        output_html.write('<thead>\n')

        for row in output_csv:
            if not r != 0:
                output_html.write('<tr>\n')
                for column in row:
                    output_html.write('<th scope="col">' + column + '</th>')
                output_html.write('</tr>\n')
                output_html.write('</thead>\n')
                output_html.write('<tbody>\n')

            else:
                c = 1
                for num, column in enumerate(row):
                    output_html.write('<td class=\"column_' + str(c) + '\">' + column + '</td>\n')
                    c += 1
                output_html.write('</tr>\n')
            r += 1

        output_html.write('</tbody>\n')
        output_html.write('</table>\n')
        output_html.write('</body>\n')
        output_html.write('</html>\n')
