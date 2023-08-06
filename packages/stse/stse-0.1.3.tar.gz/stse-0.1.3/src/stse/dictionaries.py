def branches(data:dict):
    vals = []
    keys = []
    def __base_list(dd, key:str):
        if isinstance(dd, dict):
            [list(__base_list(dd[d], f'{key}_{d}')) for d in list(dd.keys())]
        else:
            vals.append(dd)
            keys.append(key)
            yield dd
    list(__base_list(data, ''))
    
    out = {}
    for k, v in zip(keys, vals):
        out[k] = v
    return out
