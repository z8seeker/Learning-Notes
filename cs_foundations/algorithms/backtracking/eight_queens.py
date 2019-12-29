# 使用回溯算法求解八皇后问题

# 全局变量，下标表示行，值表示 queen 放置在哪一列
result = [None] * 8
all_numbers = []


def cal8queens(row):
    global result
    if row == 8:
        print_queens(result)
        return
    for column in range(8):
        if is_ok(row, column):
            result[row] = column
            cal8queens(row+1)


# 判断 row 行，column 列放置是否合适
def is_ok(row, column):
    leftup = column - 1
    rightup = column + 1
    # 逐行往上考察每一行
    for i in range(row-1, -1, -1):
        if result[i] == column:  # 考察column 列是否有 queen
            return False
        if leftup >= 0 and result[i] == leftup:  # 考察左上对角线是否有 queen
            return False
        if rightup < 8 and result[i] == rightup:  # 考察右上对角线是否有 queen
            return False
        leftup -= 1
        rightup += 1
    
    return True


def print_queens(alist):
    global result, all_numbers
    for row in range(8):
        for column in range(8):
            if result[row] == column:
                print('Q', end=' ')
            else:
                print('*', end=' ')
        print('\n')
    print('\n')
    all_numbers.append(alist)


if __name__ == '__main__':
    cal8queens(0)
    print(len(all_numbers))
