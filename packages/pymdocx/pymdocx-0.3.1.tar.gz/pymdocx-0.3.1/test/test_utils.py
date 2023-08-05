import os

from pymdocx.common.utils import print_doc

DIR_PATH = './../data/other'


def test_print_doc():
    doc_path = os.path.join(DIR_PATH, 'pt1.docx')
    print_doc(doc_path)