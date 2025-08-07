from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from math import pi , sin , cos 

# reportlabにおけるA4の分解能
max_width = 596
max_height = 842

# レポートの使用カラー（ RGB ）
header_color = [ 90 /255 , 190/255 , 240/255 ]
thema_color  = [ 207/255 , 250/255 , 255/255 ]
black_color  = [ 0       , 0       , 0       ]
gray_color   = [ 200/255 , 200/255 , 200/255 ]
white_color  = [ 1       , 1       , 1       ]

# 各余白の設定
margine = 20         # レポートの周囲のマージン
y_between_items = 10 # オブジェクト同士の上下間のマージン

# レポートのヘッダー部分を作成する関数
def report_header( page , font_name:str , date:str , exam_title:str , num_examinee:int , name:str ):

    # 実施した日付を表示
    font_size = 7
    page.setFont( psfontname=font_name , size=font_size )

    x_date = max_width - margine
    y_date = max_height - 15
    date_text = "実施日 : " + date

    page.drawRightString( x=x_date , y=y_date , text=date_text )

    # ヘッダーフレームの枠を作成
    page.setStrokeColorRGB( *thema_color )
    page.setLineWidth( 2 )

    width_header_frame = max_width - 2 * margine
    height_header_frame = 40
    
    x_header_frame = margine
    y_header_frame = max_height - ( margine + height_header_frame )

    page.rect( x=x_header_frame , y=y_header_frame , width=width_header_frame, height=height_header_frame, fill=False )


    # ヘッダーフレーム内の文字を配置する（ レポートの名前 ）
    font_size = 15
    page.setFont( psfontname=font_name , size=font_size )

    x_offset1 = 10
    y_offset1 = 20
    frame_text1 = "全国大学編入模試 : " + exam_title + "   個人成績表   " + name + "  さん"

    page.drawString( x=x_header_frame+x_offset1 , y=y_header_frame+y_offset1 , text=frame_text1 )


    # ヘッダーフレーム内の文字を配置する（ 受験者数の記述 ）
    font_size = 10
    page.setFont( psfontname=font_name , size=font_size )

    x_offset2 = int( 0.77 * width_header_frame )
    y_offset2 = 5
    frame_text2 = "（ 受験者数 : " + str( num_examinee ) + " 名　）"

    page.drawString( x=x_header_frame+x_offset2 , y=y_header_frame+y_offset2 , text=frame_text2 )

    return y_header_frame


# 各レポート項目のヘッダーを作成する関数 
def item_header( page , font_name:str , item_num:int , item_name:str , y_min:int ):

    # 枠を作成
    page.setStrokeColorRGB( *header_color )
    page.setFillColorRGB( *thema_color )
    page.setLineWidth( 1 )

    width_item_frame = max_width - 2 * margine
    height_item_frame = 20
    
    x_item_frame = margine
    y_item_frame = y_min - ( y_between_items + height_item_frame )

    page.rect( x=x_item_frame , y=y_item_frame , width=width_item_frame, height=height_item_frame, fill=True )

    # 字を配置
    font_size = 10
    page.setFont( psfontname=font_name , size=font_size )
    page.setFillColorRGB( *black_color )

    x_offset = 5
    y_offset = 6
    item_text = "■" + str( item_num ) + " " + item_name

    page.drawString( x=x_item_frame+x_offset , y=y_item_frame+y_offset , text=item_text )

    return y_item_frame


# 表の１行を作り、各セルの中央の座標を返す関数
def create_row( page , x_list:list , y:int , row_width:int , row_height:int , fill_color:list , stroke_color:list , line_width:list ):

    page.setFillColorRGB( *fill_color )
    page.setStrokeColorRGB( *stroke_color )
    page.setLineWidth( line_width )

    page.rect( x=x_list[0] , y=y , width=row_width, height=row_height, fill=True )

    center_x_list = [ ( x_list[0] + x_list[1] ) / 2 ]
    y_center = y + row_height / 2

    for i in range( len( x_list ) ):
        if 0 < i and i < len( x_list ) - 1 :
            page.line( x1=x_list[i], y1=y , x2=x_list[i] , y2=y+row_height )
            center_x_list.append( ( x_list[i] + x_list[i+1] ) / 2  )

    return center_x_list , y_center


# 水平に文字列を並べる関数
def holdisp_str( page , font_name:str , x_center_list:list , y_center:int , str_list:list ):

    # データ数があっているか確認
    if len( x_center_list ) != len( str_list ) :
        print("x_center_list length is not str_list length.")
        return 
    
    # 字を配置
    font_size = 10
    page.setFont( psfontname=font_name , size=font_size )
    page.setFillColorRGB( *black_color )

    
    for i in range( len( x_center_list ) ):
        page.drawCentredString( x=x_center_list[i] , y=y_center-font_size/2.5 , text=str_list[i] )
        

# 項目１の内容部分を作成する関数
def item1_content( page , font_name:str , y_min:int , part_title:list , const_value:dict , personal_value:dict , num_examinee:int ):

    # 枠を作成
    # 枠の大きさを設定
    width_item1_frame = max_width - 2 * margine
    height_item1_frame = 30

    x_item1_frame_list = [ 
        margine ,
        margine + int( 0.2 * width_item1_frame ) ,
        margine + int( 0.4 * width_item1_frame ) , 
        margine + int( 0.6 * width_item1_frame ) , 
        margine + int( 0.8 * width_item1_frame ) , 
        margine + width_item1_frame
    ]
    y_item1_frame = y_min - ( height_item1_frame + y_between_items )
    
    # １行目の枠を設定
    x_center_list , y_center = create_row( page , x_item1_frame_list , y_item1_frame , width_item1_frame , height_item1_frame , thema_color , header_color , 1 )

    # １行１列のセルだけ色を変える
    page.setFillColorRGB( *header_color )
    page.setLineWidth( 1 )
    page.rect( x=x_item1_frame_list[0] , y=y_item1_frame , width=x_item1_frame_list[1]-x_item1_frame_list[0], height=height_item1_frame, fill=True , stroke=False )

    # １行目の文字を配置
    str_list = [
        "科目・大問",
        "得点 / 配点",
        "偏差値",
        "席次",
        "平均点"
    ]
    holdisp_str( page , font_name , x_center_list , y_center , str_list )

    # 科目の行を作成
    # 行の枠の作成
    y_item1_frame = y_item1_frame - height_item1_frame
    x_center_list , y_center = create_row( page , x_item1_frame_list , y_item1_frame , width_item1_frame , height_item1_frame , white_color , header_color , 1 )

    # 文字を配置
    str_list = [
        "合計",
        str( personal_value["total"]["score"] ) + " / " + str( const_value["total"]["scoring"] ),
        str( personal_value["total"]["standard_deviation"] ),
        str( personal_value["total"]["ranking"] ) + " / " + str( num_examinee ),
        str( const_value["total"]["avg"] )
    ]
    holdisp_str( page , font_name , x_center_list , y_center , str_list )

    # 各大問ごとに行を作成
    for i in range( len( part_title ) ) :

        # 各行の枠を設定
        if i % 2 == 0:
            fill_color = thema_color
        else :
            fill_color = white_color

        y_item1_frame = y_item1_frame - height_item1_frame
        x_center_list , y_center = create_row( page , x_item1_frame_list , y_item1_frame , width_item1_frame , height_item1_frame , fill_color , header_color , 1 )

            # 文字を配置
        str_list = [
            part_title[i],
            str( personal_value[part_title[i]]["score"] ) + " / " + str( const_value[part_title[i]]["scoring"] ),
            str( personal_value[part_title[i]]["standard_deviation"] ),
            str( personal_value[part_title[i]]["ranking"] ) + " / " + str( num_examinee ),
            str( const_value[part_title[i]]["avg"] )
        ]
        holdisp_str( page , font_name , x_center_list , y_center , str_list )

    return y_item1_frame


# 三角形を描画する関数を作成
def create_triangle( page , x:int , y:int , size:int , color:list ):

    initial_phase = - pi/2

    x1 = x + size * cos( 2*pi * ( 0 / 3 ) + initial_phase )
    y1 = y + size * sin( 2*pi * ( 0 / 3 ) + initial_phase )
    x2 = x + size * cos( 2*pi * ( 1 / 3 ) + initial_phase )
    y2 = y + size * sin( 2*pi * ( 1 / 3 ) + initial_phase )
    x3 = x + size * cos( 2*pi * ( 2 / 3 ) + initial_phase )
    y3 = y + size * sin( 2*pi * ( 2 / 3 ) + initial_phase )

    path = page.beginPath()               # お絵かきを開始
    path.moveTo( x1 , y1 )            # 最初の頂点へ移動
    path.lineTo( x2 , y2 )            # 2番目の頂点へ線を引く
    path.lineTo( x3 , y3 )            # 3番目の頂点へ線を引く
    path.close()                       # パスを閉じて三角形を完成させる

    # 6. 作成したパスを描画（塗りつぶしあり、枠線なし）
    page.setFillColorRGB( *color )
    page.drawPath( path , fill=True , stroke=False )


# 得点率のグラフ作成
def create_grade_polygon( page , font_name:str , x:int , y:int , width:int , height:int , part_title:list , const_value:dict , personal_value:dict ):

    # 枠の作成
    page.setStrokeColorRGB( *header_color )
    page.setLineWidth( 1 )
    page.rect( x=x , y=y , width=width, height=height, fill=False )

    # 多角形の作成
    # 多角形を描画する領域の決定
    width_poly_area = int( 0.8 * width )

    # 外形円を描画
    n_poly = len( part_title )
    height_necessary = 1 - cos( 2*pi/n_poly * int(n_poly/2) )
    height_proportion = 0.7

    radius = height * height_proportion / height_necessary

    x_center_poly_area = x + width_poly_area / 2
    y_center_poly_area = y + height*(1-height_proportion)/2 + abs( radius * cos( 2*pi/n_poly * int(n_poly/2) ) )


    # 多角形と全体平均得点率と受験生の得点率の多角形を作成
    num_devision = 4

    for i in range( n_poly ):

        # 多角形の作成
        page.setStrokeColorRGB( *gray_color )
        page.setLineWidth( 0.6 )

        x_vertex_poly = radius * sin( 2 * pi / n_poly * i )
        y_vertex_poly = radius * cos( 2 * pi / n_poly * i )

        x_vertex_poly_next = radius * sin( 2 * pi / n_poly * ( i + 1 ) )
        y_vertex_poly_next = radius * cos( 2 * pi / n_poly * ( i + 1 ) )


        for j in range( 1 , num_devision + 1 ):

            x1 = x_center_poly_area - x_vertex_poly * ( j / num_devision )
            y1 = y_center_poly_area + y_vertex_poly * ( j / num_devision )
            x2 = x_center_poly_area - x_vertex_poly_next * ( j / num_devision )
            y2 = y_center_poly_area + y_vertex_poly_next * ( j / num_devision )

            page.line( x1=x1 , y1=y1 , x2=x2 , y2=y2 )
        

        # 受験生の成績多角形の作成
        # 多角形の作成
        page.setStrokeColorRGB( *header_color )
        page.setLineWidth( 0.6 )

        x1_personal_grade = x_center_poly_area - personal_value[part_title[i%n_poly]]["scoring_rate"] * x_vertex_poly
        y1_personal_grade = y_center_poly_area + personal_value[part_title[i%n_poly]]["scoring_rate"] * y_vertex_poly
        x2_personal_grade = x_center_poly_area - personal_value[part_title[(i+1)%n_poly]]["scoring_rate"] * x_vertex_poly_next
        y2_personal_grade = y_center_poly_area + personal_value[part_title[(i+1)%n_poly]]["scoring_rate"] * y_vertex_poly_next

        page.line( x1=x1_personal_grade , y1=y1_personal_grade , x2=x2_personal_grade , y2=y2_personal_grade )

        # 頂点の作成（ 円 ）
        page.setFillColorRGB( *header_color )
        radius_vertex = 1
        page.circle( x_cen=x1_personal_grade , y_cen=y1_personal_grade , r=radius_vertex , fill=True )


        # 平均の成績多角形の作成
        page.setStrokeColorRGB( *black_color )
        page.setLineWidth( 0.4 )

        x1_const_grade = x_center_poly_area - const_value[part_title[i%n_poly]]["avg_scoring_rate"] * x_vertex_poly
        y1_const_grade = y_center_poly_area + const_value[part_title[i%n_poly]]["avg_scoring_rate"] * y_vertex_poly
        x2_const_grade = x_center_poly_area - const_value[part_title[(i+1)%n_poly]]["avg_scoring_rate"] * x_vertex_poly_next
        y2_const_grade = y_center_poly_area + const_value[part_title[(i+1)%n_poly]]["avg_scoring_rate"] * y_vertex_poly_next

        page.line( x1=x1_const_grade , y1=y1_const_grade , x2=x2_const_grade , y2=y2_const_grade )

        # 頂点の作成（ 三角形 ）
        size_triangle = 2
        create_triangle( page , x1_const_grade , y1_const_grade , size_triangle , black_color )


        # 文字を追加
        font_size_vertex = 7.5
        page.setFont( font_name , font_size_vertex )

        text1_vertex = part_title[i]
        text2_vertex = str( personal_value[part_title[i]]["scoring_rate"] ) + "/" + str( const_value[part_title[i]]["avg_scoring_rate"] )
        y_between_text = 8

        text_width = page.stringWidth( text=text1_vertex , fontName=font_name , fontSize=font_size_vertex )

        if abs( x_vertex_poly ) < 1e-3 :
            extend_radius = 9
            x_vertex_poly_extend = x_center_poly_area - ( radius + extend_radius ) * sin( 2 * pi / n_poly * i )
            y_vertex_poly_extend = y_center_poly_area + ( radius + extend_radius ) * cos( 2 * pi / n_poly * i )
            page.drawCentredString( x=x_vertex_poly_extend , y=y_vertex_poly_extend , text=text1_vertex )
            page.drawCentredString( x=x_vertex_poly_extend , y=y_vertex_poly_extend-y_between_text , text=text2_vertex )

        elif x_vertex_poly > 0 :
            extend_radius = 3
            x_vertex_poly_extend = x_center_poly_area - ( radius + extend_radius ) * sin( 2 * pi / n_poly * i )
            y_vertex_poly_extend = y_center_poly_area + ( radius + extend_radius ) * cos( 2 * pi / n_poly * i )
            page.drawRightString( x=x_vertex_poly_extend , y=y_vertex_poly_extend , text=text1_vertex )
            page.drawCentredString( x=x_vertex_poly_extend-text_width/2 , y=y_vertex_poly_extend-y_between_text , text=text2_vertex )

        else :
            extend_radius = 3
            x_vertex_poly_extend = x_center_poly_area - ( radius + extend_radius ) * sin( 2 * pi / n_poly * i )
            y_vertex_poly_extend = y_center_poly_area + ( radius + extend_radius ) * cos( 2 * pi / n_poly * i )
            page.drawString( x=x_vertex_poly_extend , y=y_vertex_poly_extend , text=text1_vertex )
            page.drawCentredString( x=x_vertex_poly_extend+text_width/2 , y=y_vertex_poly_extend-y_between_text , text=text2_vertex )
    

    # 凡例の作成
    page.setStrokeColorRGB( *gray_color )
    page.setLineWidth( 0.6 )

    margine_legend = 10
    width_legend = 0.25 * width
    height_legend = 0.6 * width_legend
    x_legend = max_width - ( margine + margine_legend + width_legend )
    y_legend = y + height - ( margine_legend + height_legend )

    page.rect( x=x_legend , y=y_legend , width=width_legend, height=height_legend, fill=False )

    font_size_legend = 6
    page.setFont( font_name , font_size_legend )

    radius_legend = 3
    page.setFillColorRGB( *header_color )
    page.circle( x_cen=x_legend+0.2*width_legend , y_cen=y_legend + 2/3*height_legend , r=radius_legend , fill=True , stroke=False )
    page.setFillColorRGB( *black_color )
    page.drawString( x=x_legend+0.3*width_legend , y=y_legend + 2/3*height_legend-font_size_legend/2.5 , text="本人得点率" )

    create_triangle( page , x_legend+0.21*width_legend , y_legend + 1/3*height_legend , 4 , black_color )
    page.drawString( x=x_legend+0.3*width_legend , y=y_legend + 1/3*height_legend-font_size_legend/2.5 , text="平均得点率" )





# 項目2の内容部分を作成する関数
def item2_content( page , font_name:str , y_min:int , part_title:list , const_value:dict , personal_value:dict ):

    # 枠を作成
    # 枠の大きさを設定
    width_item2_frame = int( 0.45 * max_width )
    height_item2_frame = 30

    x_item2_frame_list = [ 
        margine ,
        margine + int( 0.35 * width_item2_frame ) ,
        margine + int( 0.55 * width_item2_frame ) , 
        margine + int( 0.85 * width_item2_frame ) , 
        margine + width_item2_frame
    ]
    y_item2_frame = y_min - ( height_item2_frame + y_between_items )
    
    # １行目の枠を設定
    x_center_list , y_center = create_row( page , x_item2_frame_list , y_item2_frame , width_item2_frame , height_item2_frame , thema_color , header_color , 1 )

    # １行１列のセルだけ色を変える
    page.setFillColorRGB( *header_color )
    page.setLineWidth( 1 )
    page.rect( x=x_item2_frame_list[0] , y=y_item2_frame , width=x_item2_frame_list[1]-x_item2_frame_list[0], height=height_item2_frame, fill=True , stroke=False )

    # １行目の文字を配置
    str_list = [
        "科目・大問",
        "得点率",
        "平均得点率",
        "差分"
    ]
    holdisp_str( page , font_name , x_center_list , y_center , str_list )

    # 科目の行を作成
    # 行の枠の作成
    y_item2_frame = y_item2_frame - height_item2_frame
    x_center_list , y_center = create_row( page , x_item2_frame_list , y_item2_frame , width_item2_frame , height_item2_frame , white_color , header_color , 1 )

    # 文字を配置
    str_list = [
        "合計",
        str( personal_value["total"]["scoring_rate"] ),
        str( const_value["total"]["avg_scoring_rate"] ),
        str( personal_value["total"]["differ_rate"] )
    ]
    holdisp_str( page , font_name , x_center_list , y_center , str_list )

    # 各大問ごとに行を作成
    for i in range( len( part_title ) ) :

        # 各行の枠を設定
        if i % 2 == 0:
            fill_color = thema_color
        else :
            fill_color = white_color

        y_item2_frame = y_item2_frame - height_item2_frame
        x_center_list , y_center = create_row( page , x_item2_frame_list , y_item2_frame , width_item2_frame , height_item2_frame , fill_color , header_color , 1 )

            # 文字を配置
        str_list = [
            part_title[i],
            str( personal_value[part_title[i]]["scoring_rate"] ),
            str( const_value[part_title[i]]["avg_scoring_rate"] ),
            str( personal_value[part_title[i]]["differ_rate"] )
        ]
        holdisp_str( page , font_name , x_center_list , y_center , str_list )


    # 右側のグラフの作成
    x_poly = margine+width_item2_frame+y_between_items
    y_poly = y_item2_frame
    width_poly = max_width - x_poly - margine
    height_poly = height_item2_frame * ( 2 + len( part_title ) )

    create_grade_polygon( page , font_name , x_poly , y_poly , width_poly , height_poly , part_title , const_value , personal_value )

    return y_item2_frame



# 得られた情報から模試のレポートを作成する関数
def DrawReport( exam_title:str , date:str , num_examinee:int , part_title:list , const_value:dict , name:str , personal_value:dict , export_dir:str ):

    # インスタンスの作成
    page = canvas.Canvas( export_dir +exam_title + "_" + name + ".pdf" , pagesize=portrait(A4) )

    # pdfのフォント設定
    font_name = "Font1"
    pdfmetrics.registerFont( TTFont( font_name , "Font/HGRME.TTC" ) )


    # レポートのヘッダー部分の作成
    # yminはその時点でpdfに描画されたオブジェクトの最小y座標を格納する
    y_min = report_header( page , font_name , date , exam_title , num_examinee , name )

    header_bottom_margine = 15

    # 項目１ : 科目・大問別成績
    # ヘッダー部分
    y_min = item_header( page , font_name , 1 , "科目・大問別成績" , y_min - header_bottom_margine )
    # 内容部分
    y_min = item1_content( page, font_name , y_min , part_title , const_value , personal_value , num_examinee )
    
    item1_bottom_margine = 15
    
    # 項目２ : 大問別得点率
    # ヘッダー部分
    y_min = item_header( page , font_name , 2 , "大問別得点率" , y_min - item1_bottom_margine )
    # 内容部分
    y_min = item2_content( page, font_name , y_min , part_title , const_value , personal_value )
    
    

    page.save()

    return


if __name__ == "__main__":

    exam_title = "情報"
    date = "2025/08/05"
    num_examinee = 2
    part_title = ["論理回路","プログラム","アルゴリズム"]

    const_value = {
        "total"       :{ "scoring":100, "avg":47.5, "deviation":17.5, "avg_scoring_rate":0.47 },
        "論理回路"     :{ "scoring":35,  "avg":15.0, "deviation":5.0,  "avg_scoring_rate":0.43 },
        "プログラム"   :{ "scoring":30,  "avg":12.5, "deviation":12.5, "avg_scoring_rate":0.42 },
        "アルゴリズム" :{ "scoring":35,  "avg":20.0, "deviation":10.0, "avg_scoring_rate":0.57 }
    }

    name = "山田太郎"

    personal_value = {
        "total"       :{ "score":30, "standard_deviation":40, "ranking":2, "scoring_rate":0.3,  "differ_rate":-0.17 },
        "論理回路"     :{ "score":20, "standard_deviation":60, "ranking":1, "scoring_rate":0.57, "differ_rate":0.14 },
        "プログラム"   :{ "score":0,  "standard_deviation":40, "ranking":2, "scoring_rate":0.0,  "differ_rate":-0.42 },
        "アルゴリズム" :{ "score":10, "standard_deviation":40, "ranking":2, "scoring_rate":0.29, "differ_rate":-0.28 }
    }
    
    export_dir = "Report/"

    DrawReport( exam_title , date , num_examinee , part_title , const_value , name , personal_value , export_dir )



    