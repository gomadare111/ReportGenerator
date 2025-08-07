import os
import csv
import math

from data_validator import is_examinfo_format_valid , is_examinfo_value_valid
from converter import convert_examinfo, convert_googleform
from statistic import const_statistic , personal_statistic , score_sort
from draw_report import DrawReport


# ディレクトリ設定
infor_dir = "CSV_Examinfo/"
result_dir = "CSV_GoogleForm/"
export_dir = "Report/"
files_name = os.listdir( result_dir )


# google formのフォーマット設定
trash_col = 3 # csvファイルの最初の必要のない列数（ timestanp, username, など ）
necessary_col = 1 # 問題とは関係ない質問
each_col = 3 # 一つの問題あたりの列数
offset_index = trash_col + necessary_col * each_col - 1 # 点数のついている問題のindexまでオフセット


# 出力設定
decimal_digit = 2 # 少数の桁数


# csvファイルの数だけfor文で回す
for file in files_name:

    # 模試の科目名、各大問名、各大問の問題数を得る
    with open( infor_dir + file , encoding='utf-8' ) as f:
        reader = list( csv.reader( f ) )

        if ( is_examinfo_format_valid( reader ) ):
            exam_title , part_title , part_each_num = convert_examinfo( reader )
        else :
            print("examinfo file format is invalid.")
            continue
    
    # print(exam_title)
    # print(part_title)
    # print(part_each_num)


    # 各受験者の結果を取得
    with open( result_dir + file , encoding='utf-8' ) as f:
        reader = list( csv.reader( f ) )

        if ( is_examinfo_value_valid( reader , part_title ,part_each_num , trash_col , necessary_col , each_col ) ):
            num_examinee = len( reader ) - 1
            date = reader[1][0].split(" ")[0]
            names , perfect_score , personal_score = convert_googleform( reader , part_title , part_each_num , offset_index )
        else :
            print("examinfo file value is invalid.")
            print("check the number of problems in each part.")
            continue
    
    # print(num_examinee)
    # print(date)
    # print(names)
    # print(perfect_score)
    # print(personal_score["山田太郎"])
    # print(personal_score["田中次郎"])

    # レポート内で「受験生によって変化しない値」を取得
    const_value = const_statistic( part_title , names , perfect_score , personal_score , decimal_digit )

    # print( const_value["total"] )
    # print( const_value["論理回路"] )
    # print( const_value["プログラム"] )
    # print( const_value["アルゴリズム"] )

    sorted_score = score_sort( part_title , names , personal_score )

    # print( sorted_score )

    
    # 各受験者にレポートを作成
    for name in names:

        # レポート内で「受験生によって変化する値」を取得
        personal_value = personal_statistic( part_title , name , const_value , personal_score , sorted_score , decimal_digit )

        # print( personal_value["total"] )
        # print( personal_value["論理回路"] )
        # print( personal_value["プログラム"] )
        # print( personal_value["アルゴリズム"] )
        # print()

        DrawReport( exam_title , date , num_examinee , part_title , const_value , name , personal_value , export_dir )
    
        