
print obj:
    lv obj
    ti STR
    lc '\n'
    bs
    cp write
    rt 0

input string:
    lv string
    lc NULL
    co ==
    jt 2
    lv string
    cp write
    cp read
    rt 1


