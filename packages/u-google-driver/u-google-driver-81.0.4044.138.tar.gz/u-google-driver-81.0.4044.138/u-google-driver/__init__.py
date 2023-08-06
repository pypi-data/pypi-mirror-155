__author__ = u'seal-haibao'


def get_mask(l):
    result = []
    for i in range(2 ** l):
        tmp = bin(i)[2:]
        tmp = '0' * (l-len(tmp)) + tmp
        result.append(tmp)
    return result

def get_ips(ip, mask):
    ip = [int(i) for i in ip.split('.')]
    mask = [int(m) for m in mask.split('.')]
    
    ip_str = ''.join(['{:0>8}'.format(bin(i)[2:]) for i in ip])
    mask_str = ''.join(['{:0>8}'.format(bin(m)[2:]) for m in mask])
    zero_index = []
    
    for i in range(len(mask_str)):
        if mask_str[i] == '0':
            zero_index.append(i)

    # print(zero_index)
    
    static_mask = get_mask(len(zero_index))

    result = []

    ip_list = list(ip_str)
    for z in zero_index:
        ip_list[z] = '0'

    for sm in static_mask:
        tmp = ip_list[:]
        for i in range(len(zero_index)):
            if sm[i] == '1':
                tmp[zero_index[i]] = '1'
        tmp = ''.join(tmp)
        tmp_mask = [int('0b' + tmp[0: 8], 2), int('0b' + tmp[8: 16], 2), int('0b' + tmp[16: 24], 2), int('0b' + tmp[24: 32], 2), ]
        result.append('.'.join([str(t) for t in tmp_mask]))
    return result
    

if __name__ == '__main__':
    r = get_ips('10.48.12.64', '255.255.245.224')
    for a in r:
        print(a)
    print(len(r))
