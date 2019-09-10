def Parser(text : str):
    rawCQs = []
    state = -1
    for index in range(0, len(text)):
        if state < 0 and text[index] == '[':
            state = index
        if state >= 0 and text[index] == ']':
            rawCQs.append(text[state + 1: index - 1])
            state = -1
    CQlist = []
    for item in rawCQs:
        attrs = item.split(',')
        attrs[0] = attrs[0].replace(':', '=')
        CQlist.append({attr.split('=')[0]:attr.split('=')[1] for attr in attrs })
    return CQlist