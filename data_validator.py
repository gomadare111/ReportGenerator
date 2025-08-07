# examinfoのcsvフォーマットが正しいかどうか判断する関数
def is_examinfo_format_valid( reader:list ) :

    if len( reader[0] ) != 1 :
        return False
    
    elif len( reader[1] ) != len( reader[2] ) :
        return False
    
    else :
        return True

# examinfoのcsvの値が正しいかどうか判断する関数
def is_examinfo_value_valid( reader:list , part_title:list , part_each_num:dict , trash_col:int , necessary_col:int , each_col:int ):
    
    total_problem_num = 0

    for i in range( len( part_title ) ):
        total_problem_num += part_each_num[ part_title[ i ] ]

    if len( reader[0] ) != trash_col + ( necessary_col + total_problem_num ) * each_col :
        return False
    
    else :
        return True