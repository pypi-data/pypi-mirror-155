from pymdocx.common.comment import has_comment
from pymdocx.common.revision import has_revision
from pymdocx.common.utils import add_p_comment_next


def detect_comment_revision_in_table(doc_obj_list):
    """
    {
    table_index_1: {cell_index: {p_index: [doc_index_list]}}
    }
    """
    m = {}
    for doc_index, doc_obj in enumerate(doc_obj_list):
        for t_index, t in enumerate(doc_obj.tables):
            for c_index, c in enumerate(t._cells):
                for p_index, p in enumerate(c.paragraphs):
                    if has_comment(p) or has_revision(p):
                        if t_index not in m:
                            m[t_index] = {c_index: {p_index: [doc_index]}}
                        elif c_index in m[t_index] and p_index not in m[t_index][c_index]:
                            m[t_index][c_index][p_index] = [doc_index]
                        elif c_index in m[t_index] and p_index in m[t_index][c_index]:
                            m[t_index][c_index][p_index].append(doc_index)
                        elif c_index not in m[t_index]:
                            m[t_index][c_index] = {p_index: [doc_index]}
    return m


def merge_table_comment_revision(doc_base_obj, merge_doc_list):
    detect_dict = detect_comment_revision_in_table(merge_doc_list)
    for t_index, t_v in detect_dict.items():
        for c_index, c_v in t_v.items():
            has_add_p_count = 0
            remove_p_list = []
            for p_index, doc_index_list in c_v.items():
                base_p = last_p = doc_base_obj.tables[t_index]._cells[c_index].paragraphs[p_index + has_add_p_count]
                remove_p_list.append(last_p)
                for doc_index in doc_index_list:
                    merge_doc_obj = merge_doc_list[doc_index]
                    if merge_doc_obj.tables[t_index]._cells[c_index].paragraphs:
                        target_p = merge_doc_obj.tables[t_index]._cells[c_index].paragraphs[p_index]
                        add_p_comment_next(last_p, target_p, doc_base_obj.comments_part.element)
                        last_p = target_p
                        has_add_p_count += 1
                    else:
                        if base_p in remove_p_list:
                            remove_p_list.remove(base_p)
            [rp.delete() for rp in remove_p_list]