import xml.etree.ElementTree as xml
from HTMLRemove import strip_tags, stripCode, stripLinks, removePeriods, removeCharacters,getCode, containsAPI
import re
import nltk

questions_remove = []
questions = []
answers = {}
tags_list = ['java','api','c#','python','string','c++']

def create_sub_xml():
    xml_file = open('parsed.xml','w')
    print "Started to parse the xml file into tree"
    posts_file = open('C:\Users\Ankur Bansal\Desktop\Posts.xml')
    print "Finished parsing the tree"
    num = 0
    while num < 100000:
        xml_file.write(posts_file.readline())
        if num % 1000 == 0:
            print num
        num += 1
    xml_file.write('\n')
    xml_file.write('</posts>')
    xml_file.close()
    posts_file.close()


def parse_xml():
    csv_file = open('data.txt','w')
    xml_tree = xml.parse('parsed.xml')
    xml_root = xml_tree.getroot()
    count_posts = 0
    count_threads = 0
    for row in xml_root:
        count_posts += 1
        post_id = row.attrib['Id']
        post_type = row.attrib['PostTypeId']

        if post_type == '1':
            if 'Tags' not in row.attrib or ('Tags' in row.attrib and not(any(tag in row.attrib['Tags'].lower() for tag in tags_list))):
                questions_remove.append(post_id)
                xml_root.remove(row)
            else:
                questions.append(post_id)
                count_threads += 1
                csv_file.write(re.sub('\n','',row.attrib['Body'].encode('ascii',errors='ignore'),flags=re.DOTALL) + '\n')
        elif post_type == '2':
            parent_id = row.attrib['ParentId']
            if parent_id in questions_remove:
                xml_root.remove(row)
            elif parent_id in questions:
                csv_file.write(re.sub('\n','',row.attrib['Body'].encode('ascii',errors='ignore'),flags=re.DOTALL) + '\n')

        if count_threads > 200:
            if count_posts > 1000:
                break

    csv_file.close()

def cleanPosts():
    read = open('data.txt','r')
    write = open('cleanData.txt','w')
    for line in read:
        line = re.sub('<pre><code>.*?</code></pre>', '', line, flags=re.DOTALL)
        line = strip_tags(line)
        line = stripLinks(line)
        write.write(line)
    read.close()
    write.close()

def tokenize():
    f = open('cleanData.txt','r')
    tok = open('tokens.txt','w')
    for line in f:
        tokens = nltk.word_tokenize(line)
        for token in tokens:
            tok.write(token + '\tO\n')
    f.close()
    tok.close()

tokenize()
