import numpy as np

from pymdocx.common.utils import add_p_comment_next, get_element_comment_revision_matrix


def get_merge_res(m_list):
    # 返回一个字典，每个被批注和修订的段落的索引，以及对应的文档索引
    # key: p index
    # value: 文件 index
    #
    # {0: [0], 1: [1, 0], 2: [0], 8: [0], 10: [0]}
    m_merge = np.array(m_list)
    print('m_merge:')
    print(m_merge)

    print('merge doc modify')
    m_modify = np.max(m_merge, axis=1)
    print(m_modify)

    print('修改')
    m_arg = np.argwhere(m_modify > 0)
    print(m_arg)

    merge_arg_dict = {}
    for doc_index, p_index in m_arg:
        if merge_arg_dict.get(p_index):
            merge_arg_dict.get(p_index).append(doc_index)
        else:
            merge_arg_dict[p_index] = [doc_index]
    return merge_arg_dict


def merge_paragraph_comment_revision(doc_base_obj, doc_list):
    def _get_actual_p_index(has_add_mapping, doc_index, p_index):
        if doc_index in has_add_mapping.keys():
            has_add_mapping[doc_index] += 1
        else:
            has_add_mapping[doc_index] = 0
        return p_index - has_add_mapping[doc_index]

    m_list = [get_element_comment_revision_matrix(doc) for doc in doc_list]
    merge_arg_dict = get_merge_res(m_list)

    has_add_mapping = {}
    has_add_p_count = 0
    remove_p_list = []
    for p_index, doc_index_list in merge_arg_dict.items():
        last_p = doc_base_obj.paragraphs[p_index + has_add_p_count]
        remove_p_list.append(last_p)
        for doc_index in doc_index_list:
            actual_p_index = _get_actual_p_index(has_add_mapping, doc_index, p_index)
            target_p = doc_list[doc_index].paragraphs[actual_p_index]
            # 添加段落后，target_p所在文档结构发生变化
            add_p_comment_next(last_p, target_p, doc_base_obj.comments_part.element)
            last_p = target_p
            has_add_p_count += 1
    [rp.delete() for rp in remove_p_list]
