def sci():
    p = float(input('Enter principal amount: '))
    t = float(input('Enter time period: '))
    r = float(input('Enter interest rate: '))
    si = (p*t*r)/100
    ci = p * ( (1+r/100)**t - 1)
    print('Simple interest is: %f' % (si))
    print('Compound interest is: %f' %(ci))
    return