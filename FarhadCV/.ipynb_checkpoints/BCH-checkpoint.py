import bchlib





def BCHgenetrator(secret,BCH_POLYNOMIAL, BCH_BITS, number_zeros, sevensize ):  
    #print(tcolors.RED, secret, tcolors.ENDC)
    bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)
    data = bytearray(secret + ' '*(sevensize-len(secret)), 'utf-8')
    ecc = bch.encode(data)
    packet = data + ecc
    packet_binary = ''.join(format(x, '08b') for x in packet)
    secret = [int(x) for x in packet_binary]
    secret.extend([0 for i in range(number_zeros)])
    return secret