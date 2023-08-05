import docx


def get_ins_del(p):
    from pymdocx.common.utils import print_xml_node
    ins_list = get_ins_in_paragraph(p)
    for ins in ins_list:
        print_xml_node(ins)
    del_list = get_del_in_paragraph(p)
    for del_ in del_list:
        print_xml_node(del_)


def get_revision(doc_file_path):
    document = docx.Document(docx=doc_file_path)
    for p in document.paragraphs:
        get_ins_del(p)


def has_revision_ins(p):
    return 1 if get_ins_in_paragraph(p) else 0


def has_revision_del(p):
    return 1 if get_del_in_paragraph(p) else 0


def has_revision(p):
    return has_revision_del(p) or has_revision_ins(p)


def get_ins_in_paragraph(p):
    from pymdocx.common.utils import get_label_in_paragraph
    # 获取新增修订
    return get_label_in_paragraph(p, 'ins')


def get_del_in_paragraph(p):
    from pymdocx.common.utils import get_label_in_paragraph
    # 获取删除修订
    return get_label_in_paragraph(p, 'del')