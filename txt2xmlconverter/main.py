from txt2xml import Text2Xml
import codecs
import os

if __name__ == '__main__':
    for root, directory, files in os.walk('./maha'):
        for f in files:
            if f.endswith('.txt'):
                path = os.path.join(root, f)
                story = codecs.open(path, 'r', encoding='utf-8', errors='ignore')
                t = Text2Xml(root)
                t.convertTxt2Xml(story.readlines())
                t.writeXmlFile(path)




