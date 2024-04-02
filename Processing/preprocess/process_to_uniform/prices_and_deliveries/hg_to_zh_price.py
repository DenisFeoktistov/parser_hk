def hg_to_zh(x):
    x += (x + 149) // 150
    y = x

    if x > 5000:  # 5200+-? 5000+-?
        y = int(x * 1.1395)

    return y
