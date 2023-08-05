import os

from pymdocx.common.utils import get_doc
from pymdocx.doc.paragraph import merge_paragraph_comment_revision


DIR_PATH = './../data/test_p'


def test_merge_paragraph_comment_revision():

    doc_file_path_o = os.path.join(DIR_PATH, "pt0_0.docx")
    doc_file_path_a = os.path.join(DIR_PATH, "pt0_a.docx")
    doc_file_path_c = os.path.join(DIR_PATH, "pt0_c.docx")

    doc_o = get_doc(doc_file_path_o)
    doc_a = get_doc(doc_file_path_a)
    doc_c = get_doc(doc_file_path_c)
    merge_paragraph_comment_revision(doc_o, [doc_a, doc_c])
    doc_o.save('pt0_new.docx')