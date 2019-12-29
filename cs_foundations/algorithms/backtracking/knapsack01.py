# 使用回溯算法解决 0-1 背包问题


# 全局变量
max_weight = 0

def solution01(i, cw, items, n, w):
    """
    i 表示考察到哪个物品了，
    cw 表示当前背包的重量，
    items 表示物品重量的数组
    n 表示背包可以装多少个物品
    w 表示背包可承受的最大重量
    """
    global max_weight
    if cw == w or i == n:  # 背包达到极限
        if cw > max_weight:
            max_weight = cw
        return
    # 不装该物品
    solution01(i+1, cw, items, n, w)
    # 装下该物品
    if (cw + items[i]) <= w:
        solution01(i+1, cw+items[i], items, n, w)


if __name__ == '__main__':
    items = [15, 18, 20, 25, 32]
    n = 5
    w = 69
    solution01(0, 0, items, n, w)
    print(max_weight)
