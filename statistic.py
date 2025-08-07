import math

# const_statisticの補助関数（ 各大問における平均と二乗平均を返す ）
def get_liner_and_square_average( part_title:list , names:list , personal_score:dict ):

    liner_avg = { "total": 0 }
    squared_avg = { "total": 0 }

    for title in part_title :
        liner_avg[title] = 0
        squared_avg[title] = 0

    for name in names:        
        liner_avg["total"] += sum( list( personal_score[name].values() ) ) / len( names )
        squared_avg["total"] += sum( list( personal_score[name].values() ) )**2 / len( names )

        for title in part_title:
            liner_avg[title] += personal_score[name][title] / len(names)
            squared_avg[title] += personal_score[name][title]**2 / len(names)

    return liner_avg , squared_avg


# const_statisticの補助関数（ 各大問における辞書変数を返す ）
def const_statistic_dict( scoring:int , liner_avg:float , squared_avg:float , decimal_digit:int ):

    return_dict = {}
    return_dict["scoring"]          = scoring
    return_dict["avg"]              = round( liner_avg , decimal_digit )
    return_dict["deviation"]        =  round( math.sqrt(squared_avg - liner_avg**2) , decimal_digit )
    return_dict["avg_scoring_rate"] = round( liner_avg / scoring , decimal_digit )

    return return_dict


# 採点レポートの「受験者によって変化しない値」を返す関数
def const_statistic( part_title:list , names:list , perfect_score:dict , personal_score:dict , decimal_digit:int ):

    liner_avg , squared_avg = get_liner_and_square_average( part_title , names , personal_score )

    total_dict = const_statistic_dict( sum( list( perfect_score.values() ) ) , liner_avg["total"], squared_avg["total"] , decimal_digit )

    const_value = { "total":total_dict }

    for part in part_title:
        const_value[ part ] = const_statistic_dict( perfect_score[part] , liner_avg[part] , squared_avg[part] , decimal_digit  )
    
    return const_value


# 順位を効率よく特定するために、各大問ごとに降順で並び替え
def score_sort( part_title:list , names:list , personal_score:dict ):

    sorted_score = {"total":[]}
    for part in part_title:
        sorted_score[ part ] = []
    
    for name in names:
        sorted_score["total"].append( sum( list( personal_score[name].values() ) ) )

        for part in part_title:
            sorted_score[part].append( personal_score[name][part] )
    
    sorted_score["total"].sort( reverse=True )

    for part in part_title:
        sorted_score[ part ].sort( reverse=True )
    
    return sorted_score


# personal_statisticの補助関数（ 各大問における辞書変数を返す ）
def personal_statistic_dict( score:int , avg:float , deviation:float, sorted_score:list, scoring:int , avg_scoring_rate:float , decimal_digit:int):

    return_dict = {}
    return_dict["score"]              = score
    return_dict["standard_deviation"] = round( ( score - avg ) * 10 / deviation + 50  , decimal_digit )
    return_dict["ranking"]            = sorted_score.index( score ) + 1 
    return_dict["scoring_rate"]       = round( score / scoring , decimal_digit )
    return_dict["differ_rate"]        = round( score / scoring - avg_scoring_rate , decimal_digit ) 

    return return_dict


# 採点レポートの「受験者によって変化する値」を返す関数
def personal_statistic( part_title:list , name:str , const_value:dict , personal_score:dict , sorted_score:dict , decimal_digit:int ):

    total_dict = personal_statistic_dict( sum( list( personal_score[name].values() ) ) , const_value["total"]["avg"] , const_value["total"]["deviation"] , sorted_score["total"] , const_value["total"]["scoring"] , const_value["total"]["avg_scoring_rate"] , decimal_digit )

    personal_value = { "total":total_dict }
    
    for part in part_title:
        personal_value[ part ] = personal_statistic_dict( personal_score[name][part] , const_value[part]["avg"] , const_value[part]["deviation"] , sorted_score[part] , const_value[part]["scoring"] , const_value[part]["avg_scoring_rate"], decimal_digit ) 

    return personal_value
