def split_text(text, chunk_size=500, chunk_overlap=50):
    """把长文本切割成块，并返回文本块列表"""
    chunk_list = []
    head = 0
    tail = chunk_size
    step = chunk_size - chunk_overlap

    while head < len(text) and text:
        # 判断tail是否超出了文本长度
        if tail > len(text):
            tail = len(text)
        # 防止无效切片出现
        if tail - head <= chunk_overlap:
            return chunk_list

        chunk_list.append(text[head:tail])
        head += step
        tail += step

    return chunk_list
