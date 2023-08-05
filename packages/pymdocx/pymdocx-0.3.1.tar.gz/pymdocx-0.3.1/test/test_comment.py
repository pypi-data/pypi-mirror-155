import os

from pymdocx.common.comment import get_comment_xml

DIR_PATH = './../data/test_table'


def test_get_comment_xml():
    doc_path = os.path.join(DIR_PATH, 'table_a.docx')
    comment_xml = get_comment_xml(doc_path)
    print(comment_xml)