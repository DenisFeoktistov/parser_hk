def count_missing_values(sizes, table):
    cnt = 0
    for size in sizes:
        for row_name, sizes in table.items():
            if size in sizes:
                break
        else:
            cnt += 1

    return cnt
