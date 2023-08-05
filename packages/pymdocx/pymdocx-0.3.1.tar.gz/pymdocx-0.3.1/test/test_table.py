import os

from pymdocx.common.utils import get_doc
from pymdocx.doc.table import merge_table_comment_revision

DIR_PATH = './../data/test_table'


def test_detect_comment_revision_in_table():
    doc_o_path = os.path.join(DIR_PATH, 'table.docx')
    doc_a_path = os.path.join(DIR_PATH, 'table_a.docx')
    doc_b_path = os.path.join(DIR_PATH, 'table_b.docx')
    doc_o = get_doc(doc_o_path)
    doc_a = get_doc(doc_a_path)
    doc_b = get_doc(doc_b_path)
    merge_table_comment_revision(doc_o, [doc_a, doc_b])
    doc_o.save('table_new.docx')