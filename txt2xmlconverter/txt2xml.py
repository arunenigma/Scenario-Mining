import os


class Text2Xml(object):
    def __init__(self, root):
        new_dir = root + '_xml'
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

    def convertTxt2Xml(self, story):
        self.re_struct_txt = ''
        head_tags = '<story>\n<body>'
        end_tags = '</body>\n</story>'
        self.re_struct_txt += head_tags

        for excerpt in story:
            self.re_struct_txt += excerpt
        self.re_struct_txt += end_tags

    def writeXmlFile(self, path):
        path = path.split('/')
        new_path = path[0] + '/' + path[1] + '_xml' + '/' + path[2].split('.')[0] + '.xml'
        f = open(new_path, 'wb')
        f.write(self.re_struct_txt.encode('ascii', 'ignore'))
        f.close()
