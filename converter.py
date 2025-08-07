trash_col = 3 # csvファイルの最初の必要のない列数（ timestanp, username, など ）
necessary_col = 1 # 問題とは関係ない質問
each_col = 3 # 一つの問題あたりの列数


# ExamInfoからのcsvデータを扱いやすいように整形
def convert_examinfo( raw_data:list ):

    exam_title = raw_data[0][0]
    exam_title = exam_title.replace("\ufeff","")

    part_title = raw_data[1]

    part_each_num = {}

    for i in range( len( part_title ) ) :
        part_each_num[ part_title[i] ] = int( raw_data[2][i] )

    return exam_title , part_title , part_each_num


# convert_googleformの補助関数（ 点数のスコアを辞書として返す関数 ）
def create_score_dict( raw_data:list , part_title:list , part_each_num:dict , personal_index:int , offset_index:int , pri_or_latter:int  ):

    out_dict = {}

    cnt = 0
    index = 0
    sum = 0

    for i in range( len( raw_data[1] ) ):

        if i - offset_index > 0 and ( i - offset_index ) % each_col == 2:
            cnt += 1
            sum += int( float( raw_data[personal_index][i].split("/")[ pri_or_latter ] ) )

            if cnt == part_each_num[ part_title[ index ] ] and index < len( part_title ):
                out_dict[ part_title[ index ] ] = sum

                cnt = 0
                sum = 0
                index += 1
    
    return out_dict


# GoogleFormからの生データを扱いやすいように整形
def convert_googleform( raw_data:list , part_title:list , part_each_num:dict , offset_index:int):

    perfect_score = create_score_dict( raw_data , part_title , part_each_num , 1 , offset_index , 1 )
        
    names = []

    for i in range( 1 , len( raw_data ) ):
        names.append( raw_data[i][ trash_col ] )

    personal_score = {}

    for i in range( 1 , len( raw_data ) ):
        personal_score[ names[ i - 1 ] ] = create_score_dict( raw_data , part_title , part_each_num , i , offset_index , 0 )

    return names , perfect_score , personal_score