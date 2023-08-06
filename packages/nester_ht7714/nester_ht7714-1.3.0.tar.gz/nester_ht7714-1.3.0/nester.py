def print_lol(the_list, indent=False,level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent,level + 1)
        else:
            if indent:
                for tab_stop in range(level):#次for循环可替换代码为print('\t'*level,end='')1.2.7
                    print('\t', end='')
            print(each_item)
