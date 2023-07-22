from logicaMenu import logicaMenu
from helpers import pedirRuta
# from obtenerHtml import exportarHtml

import ply.yacc as yacc
import lexer
from lexer import tokens

from importlib import reload
import re

exportarTxt = list()
contadorErrores = 0


# ---- PRODUCCIONES DE LA GRAMATICA ---- #
# Mayusculas = No Terminales
# Minusculas = Terminales (etiquetas/tokens)

def p_SIGMA(p): # Simbolo distinguido
    '''SIGMA : doctype ARTICLE
    '''
    exportarTxt.append(['Prod. SIGMA -->', p.slice])
    p[0] = f'{p[2]}'

def p_ARTICLE(p):                                                           # SI ALGUN ARTICLE DERIVA EN UN TITLE, INMEDIATAMENTE DEBERIA SER UN H1
    '''ARTICLE : article INFO TITLEH1 CONT_A_S cierreArticle
				| article INFO TITLEH1 CONT_A_S SECTIONS cierreArticle           
				| article TITLEH1 CONT_A_S cierreArticle
                | article TITLEH1 CONT_A_S SECTIONS cierreArticle
                | article INFO CONT_A_S cierreArticle
                | article INFO CONT_A_S SECTIONS cierreArticle
                | article CONT_A_S cierreArticle
    '''
    if(len(p) == 4):
        p[0] = f'{p[2]}'
    elif(len(p) == 5):
        p[0] = f'{p[2]}\n{p[3]}'
    elif(len(p) == 6):
        p[0] = f'{p[2]}\n{p[3]}\n{p[4]}'
    elif(len(p) == 7):
        p[0] = f'{p[2]}\n{p[3]}\n{p[4]}\n{p[5]}'
    exportarTxt.append(['Prod. ARTICLE -->', p.slice])
    
def p_INFO(p):
    '''INFO : info CONT_INFO cierreInfo
    '''
    p[0] = f'{p[2]}'
    exportarTxt.append(['Prod. INFO -->', p.slice])

def p_CONT_INFO(p):
    '''CONT_INFO : ELEM_INFO CONT_INFO
				| ELEM_INFO
    '''
    if(len(p) == 3):                    #CONSIDERO QUE CUALQUIER ETIQUETA DENTRO DE UN INFO, ES UN CONTENIDO DE INFO
        p[0] = f'<p style="background-color:green; color: white; font-size:8px">{p[1]}</p>\n{p[2]}'    # EN CASO QUE SEA RECURSIVO, EL PRIMERO SE DERIVA EN UN INFO, Y EL SIGUIENTE COMO ES RECURSIVOP, SE LE APLICARA EN EL SEGUNDO CASO CUANDO SE DECIDA TERMINAR LA RECURSIVDAD          
    elif(len(p) == 2):
        p[0] = f'<p style="background-color:green; color: white; font-size:8px">{p[1]}</p>'
        
    exportarTxt.append(['Prod. CONT_INFO -->', p.slice])
    
def p_ELEM_INFO(p):                     # SUPONEMOS QUE TODO TITLE AFUERA DE UN SECTION DEBE SER TRANSFORMADO A H1
    '''ELEM_INFO : MEDIA_OBJECT
				| ABSTRACT
                | ADDRESS
                | AUTHOR
                | DATE
                | COPYRIGHT
                | TITLE
    '''
    exportarTxt.append(['Prod. ELEM_INFO -->', p.slice])
    p[0] = f'{p[1]}'
    
def p_SECTION(p):                                                   # TODO TITULO QUE SE ENCUNTRE DIRECTAMENTE DENTRO DE UN H2, SERA TRANSFORMADO EN H2
    '''SECTION : section CONT_A_S cierreSection
				| section CONT_A_S SECTIONS cierreSection
				| section INFO CONT_A_S cierreSection
                | section INFO CONT_A_S SECTIONS cierreSection
                | section TITLEH2 CONT_A_S cierreSection
                | section TITLEH2 CONT_A_S SECTIONS cierreSection
                | section INFO TITLEH2 CONT_A_S cierreSection
                | section INFO TITLEH2 CONT_A_S SECTIONS cierreSection
                | section TITLEH2 cierreSection
    '''
    if(len(p) == 4):
        p[0] = f'<div>{p[2]}</div>'
    elif(len(p) == 5):
        p[0] = f'<div>{p[2]}\n{p[3]}</div>'
    elif(len(p) == 6):
        p[0] = f'<div>{p[2]}\n{p[3]}\n{p[4]}</div>'
    elif(len(p) == 7):
        p[0] = f'<div>{p[2]}\n{p[3]}\n{p[4]}\n{p[5]}</div>'
    exportarTxt.append(['Prod. SECTION -->', p.slice])

def p_SECTIONS(p):
    '''SECTIONS : SECTION 
				| SECTION SECTIONS
                | SIMPLE_SEC
                | SIMPLE_SEC SECTIONS
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}\n{p[2]}'
    exportarTxt.append(['Prod. SECTIONS -->', p.slice])

def p_CONT_A_S(p):
    '''CONT_A_S : CONT_1
				| CONT_1 CONT_A_S
                | SECTION
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}\n{p[2]}'
    exportarTxt.append(['Prod. CONT_A_S -->', p.slice])

def p_CONT_1(p):
    '''CONT_1 :   ITEMIZED_LIST
				| IMPORTANT
                | PARA
                | SIMPARA
                | ADDRESS
                | MEDIA_OBJECT
                | INFORMAL_TABLE
                | COMMENT
                | ABSTRACT
    '''
    p[0] = f'{p[1]}'
    exportarTxt.append(['Prod. CONT_1 -->', p.slice])

def p_SIMPLE_SEC(p):
    '''SIMPLE_SEC : simpleSection CONT_SS cierreSimpleSection
				| simpleSection INFO CONT_SS cierreSimpleSection
                | simpleSection TITLE CONT_SS cierreSimpleSection
                | simpleSection INFO TITLE CONT_SS cierreSimpleSection
    '''
    if len(p)==4:
        p[0] = f'<div>{p[2]}</div>'
    elif len(p)==5:
        p[0] = f'<div>{p[2]}\n{p[3]}</div>'
    else:
        p[0] = f'<div>{p[2]}\n{p[3]}\n{p[4]}</div>'
    exportarTxt.append(['Prod. SIMPLE_SEC -->', p.slice])

def p_CONT_SS(p):
    '''CONT_SS : CONT_1
				| CONT_1 CONT_SS
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}\n{p[2]}'
    exportarTxt.append(['Prod. CONT_SS -->', p.slice])

def p_ABSTRACT(p):
    '''ABSTRACT : abstract TITLE cierreAbstract
				| abstract TITLE PARAS cierreAbstract
    '''
    if(len(p) == 4):
        p[0] = f'{p[2]}'
    elif(len(p)==5):
        p[0] = f'{p[2]}{p[3]}'
    exportarTxt.append(['Prod. ABSTRACT -->', p.slice])

def p_TITLE(p):
    '''TITLE : title CONT_TITLE cierreTitle
    '''
    p[0] = f'{p[2]}'
    exportarTxt.append(['Prod. TITLE -->', p.slice])
    
def p_TITLEH1(p):
    '''TITLEH1 : title CONT_TITLE cierreTitle
    '''
    p[0] = f'<h1>{p[2]}</h1>'
    exportarTxt.append(['Prod. TITLEH1 -->', p.slice])
    
def p_TITLEH2(p):
    '''TITLEH2 : title CONT_TITLE cierreTitle
    '''
    p[0] = f'<h2>{p[2]}</h2>'
    exportarTxt.append(['Prod. TITLEH1 -->', p.slice])
    
def p_CONT_TITLE(p):
    '''CONT_TITLE : ELEM_TITLE
				| ELEM_TITLE CONT_TITLE
    '''
    if(len(p)==2):
        p[0] = f'{p[1]}'
    elif(len(p) == 3):
        p[0] = f'{p[1]}{p[2]}'
    exportarTxt.append(['Prod. CONT_TITLE -->', p.slice])

def p_ELEM_TITLE(p):
    '''ELEM_TITLE : contenido_texto
				| EMPHASIS
                | LINK
                | EMAIL
    '''
    p[0] = f'{p[1]}'
    exportarTxt.append(['Prod. ELEM_TITLE -->', p.slice])
    
def p_PARAS(p):
    '''PARAS : PARA
				| SIMPARA
                | PARA PARAS
                | SIMPARA PARAS
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}\n{p[2]}'
    exportarTxt.append(['Prod. PARAS -->', p.slice])

def p_PARA(p):
    '''PARA : para CONT_PARA cierrePara
    '''
    p[0] = f'<p>{p[2]}</p>'
    exportarTxt.append(['Prod. PARA -->', p.slice])

def p_CONT_PARA(p):
    '''CONT_PARA : ELEM_PARA
				| ELEM_PARA CONT_PARA
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}\n{p[2]}'
    exportarTxt.append(['Prod. CONT_PARA -->', p.slice])

def p_ELEM_PARA(p):
    '''ELEM_PARA : contenido_texto
				| EMPHASIS
                | LINK
                | EMAIL
                | AUTHOR
                | COMMENT
                | ITEMIZED_LIST
                | IMPORTANT
                | ADDRESS
                | MEDIA_OBJECT
                | INFORMAL_TABLE
    '''
    p[0] = f'{p[1]}'
    exportarTxt.append(['Prod. ELEM_PARA -->', p.slice])

def p_ITEMIZED_LIST(p):
    '''ITEMIZED_LIST : itemizedlist LIST_ITEM cierreItemizedlist
    '''
    p[0] = f'<ul>\n{p[2]}\n</ul>'
    exportarTxt.append(['Prod. ITEMIZED_LIST -->', p.slice])

def p_LIST_ITEM(p):
    '''LIST_ITEM : listItem CONT_ITEM cierreListItem
                |  LIST_ITEM listItem CONT_ITEM cierreListItem
    '''
    if len(p)==4:
        p[0] = f'<li>\n{p[2]}\n</li>'
    else:
        p[0] = f'{p[1]}\n<li>{p[3]}\n</li>'
    exportarTxt.append(['Prod. LIST_ITEM -->', p.slice])

def p_CONT_ITEM(p):
    '''CONT_ITEM : CONT_1
				| CONT_1 CONT_ITEM
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}{p[2]}'
    exportarTxt.append(['Prod. CONT_ITEM -->', p.slice])

def p_MEDIA_OBJECT(p):
    '''MEDIA_OBJECT : mediaObject INFO CONT_MEDIA_OBJECT cierreMediaObject
				| mediaObject CONT_MEDIA_OBJECT cierreMediaObject
    '''
    if len(p)==4:
        p[0] = f'<p>{p[2]}</p>'
    else:
        p[0] = f'<p>{p[2]}{p[3]}</p>'
    exportarTxt.append(['Prod. MEDIA_OBJECT -->', p.slice])

def p_CONT_MEDIA_OBJECT(p):
    '''CONT_MEDIA_OBJECT : IMAGE_OBJECT
				| VIDEO_OBJECT
                | IMAGE_OBJECT MEDIA_OBJECT
                | VIDEO_OBJECT MEDIA_OBJECT
    '''
    p[0] = f'{p[1]}'
    exportarTxt.append(['Prod. CONT_MEDIA_OBJECT -->', p.slice])

def p_IMAGE_OBJECT(p):
    '''IMAGE_OBJECT : imageObject INFO imageData cierreImageObject
				| imageObject imageData cierreImageObject
    '''
    pattern = r'<imagedata\s+fileref=["\']((?:(http[s]?|ftp[s]?)://)?(?:[\w.-]+/)*[\w.-]+\.[\w.-]+(?:\S+)?)["\']\s*/>'
    if len(p)==4:
        atrr_value = re.match(pattern, p[2])
        p[0] = f'<img src="{atrr_value}">'
    else:
        atrr_value = re.match(pattern, p[3])
        p[0] = f'<img src="{atrr_value}">{p[2]}</img>'
    exportarTxt.append(['Prod. IMAGE_OBJECT -->', p.slice])

def p_VIDEO_OBJECT(p):
    '''VIDEO_OBJECT : videoObject INFO imageData cierreVideoObject
				| videoObject videoData cierreVideoObject
    '''
    pattern = r'<videodata\s+fileref=["\']((?:(http[s]?|ftp[s]?)://)?(?:[\w.-]+/)*[\w.-]+\.[\w.-]+(?:\S+)?)["\']\s*/>'
    if len(p)==4:
        atrr_value = re.match(pattern, p[2]).group(2)
        p[0] = f'<video src="{atrr_value}"></video>'
    else:
        atrr_value = re.match(pattern, p[3]).group(2)
        p[0] = f'<video src="{atrr_value}">{p[2]}</video>'
    exportarTxt.append(['Prod. VIDEO_OBJECT -->', p.slice])

def p_AUTHOR(p):
    '''AUTHOR : author CONT_AUTHOR cierreAuthor
    '''
    p[0] = f'{p[2]}'
    exportarTxt.append(['Prod. AUTHOR -->', p.slice])

def p_CONT_AUTHOR(p):
    '''CONT_AUTHOR : FIRSTNAME
				| SURNAME
                | EMAIL
                | FIRSTNAME SURNAME
                | FIRSTNAME EMAIL
                | SURNAME EMAIL
                | FIRSTNAME SURNAME EMAIL
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}\n{p[2]}'
    elif(len(p)==4):
        p[0] = f'{p[1]}\n{p[2]}\n{p[3]}'
        
    exportarTxt.append(['Prod. CONT_AUTHOR -->', p.slice])

def p_ADDRESS(p):
    '''ADDRESS : address cierreAddress
                | address CONT_ADDRESS cierreAddress
    '''
    if(len(p) == 4):
        p[0] = f'{p[2]}'
    exportarTxt.append(['Prod. ADDRESS -->', p.slice])

def p_CONT_ADDRESS(p):
    '''CONT_ADDRESS : ELEM_ADDRESS
				| ELEM_ADDRESS CONT_ADDRESS
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}\n{p[2]}'
        
    exportarTxt.append(['Prod. CONT_ADDRESS -->', p.slice])

def p_ELEM_ADDRESS(p):
    '''ELEM_ADDRESS : STREET
				| CITY
                | STATE
                | PHONE
                | EMAIL
                | contenido_texto
    '''
    p[0] = f'{p[1]}'
    exportarTxt.append(['Prod. ELEM_ADDRESS -->', p.slice])

def p_COPYRIGHT(p):
    '''COPYRIGHT : copyright YEAR cierreCopyright
				| copyright YEAR HOLDER cierreCopyright 
    '''
    if(len(p) == 4):
        p[0] = f'{p[2]}'
    elif(len(p)==5):
        p[0] = f'{p[2]}\n{p[3]}'
    exportarTxt.append(['Prod. COPYRIGHT -->', p.slice])

def p_SIMPARA(p):
    '''SIMPARA : simpara CONT_SECL cierreSimpara
    '''
    p[0] = f'<p>{p[2]}</p>'
    exportarTxt.append(['Prod. SIMPARA -->', p.slice])

def p_EMPHASIS(p):
    '''EMPHASIS : emphasis CONT_SECL cierreEmphasis
    '''
    p[0] = f'<strong>{p[2]}</strong>'
    exportarTxt.append(['Prod. EMPHASIS -->', p.slice])

def p_COMMENT(p):
    '''COMMENT : comment CONT_SECL cierreComment
    '''
    p[0] = f'<i>{p[2]}</i>'
    exportarTxt.append(['Prod. COMMENT -->', p.slice])

def p_LINK(p):
    '''LINK : link CONT_SECL cierreLink
    '''
    pattern = r'(<link\s+xlink:href=["\'])((?:(http[s]?|ftp[s]?)://)?(?:[\w.-]+/)*[\w.-]+\.[\w.-]+(?:\S+)?)["\']\s*>'
    attr_value = re.match(pattern, p[1]).group(2)
    p[0] = f'<a href="{attr_value}">{p[2]}</a>'
    exportarTxt.append(['Prod. LINK -->', p.slice])

def p_CONT_SECL(p):
    '''CONT_SECL : CONT_2
				| CONT_2 CONT_SECL
    '''
    if(len(p)==2):
        p[0] = f'{p[1]}'
    elif(len(p) == 3):
        p[0] = f'{p[1]}{p[2]}'
    exportarTxt.append(['Prod. CONT_SECL -->', p.slice])
    
def p_CONT_2(p):
    '''CONT_2 : contenido_texto
				| EMPHASIS
                | LINK
                | EMAIL
                | AUTHOR
                | COMMENT
    '''
    p[0]= f'{p[1]}'
    exportarTxt.append(['Prod. CONT_2 -->', p.slice])
    
def p_IMPORTANT(p):
    '''IMPORTANT : important TITLE CONT_IMPORTANT cierreImportant
				| important CONT_IMPORTANT cierreImportant
    '''
    if(len(p) == 4):
        p[0] = f'<div style="background-color: red; color:white;">{p[2]}</div>'
    elif(len(p)==5):
        p[0] = f'<div style="background-color: red; color:white;">{p[2]}{p[3]}</div>'
    exportarTxt.append(['Prod. IMPORTANT -->', p.slice])

def p_CONT_IMPORTANT(p):
    '''CONT_IMPORTANT : CONT_1
				| CONT_1 CONT_IMPORTANT
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}{p[2]}'
    
    exportarTxt.append(['Prod. CONT_IMPORTANT -->', p.slice])

def p_CONT_VAR(p):
    '''CONT_VAR : CONT_3
				| CONT_3 CONT_VAR
    '''
    if(len(p)==2):
        p[0] = f'{p[1]}'
    elif(len(p) == 3):
        p[0] = f'{p[1]}{p[2]}'
    exportarTxt.append(['Prod. CONT_VAR -->', p.slice])

def p_CONT_3(p):
    '''CONT_3 : contenido_texto
				| LINK
                | EMPHASIS
                | COMMENT
    '''
    p[0] = f'{p[1]}'
    exportarTxt.append(['Prod. CONT_3 -->', p.slice])

def p_FIRSTNAME(p):
    '''FIRSTNAME : firstname CONT_VAR cierreFirstname
    '''
    p[0] = f'{p[2]}'
    exportarTxt.append(['Prod. FIRSTNAME -->', p.slice])

def p_SURNAME(p):
    '''SURNAME : surname CONT_VAR cierreSurname
    '''
    p[0] = f'{p[2]}'
    exportarTxt.append(['Prod. SURNAME -->', p.slice])

def p_STREET(p):
    '''STREET : street CONT_VAR cierreStreet
    '''
    p[0] = f'{p[2]}'
    exportarTxt.append(['Prod. STREET -->', p.slice])

def p_CITY(p):
    '''CITY : city CONT_VAR cierreCity
    '''
    p[0] = f'{p[2]}'

    exportarTxt.append(['Prod. CITY -->', p.slice])

def p_STATE(p):
    '''STATE : state CONT_VAR cierreState
    '''
    p[0] = f'{p[2]}'

    exportarTxt.append(['Prod. STATE -->', p.slice])

def p_PHONE(p):
    '''PHONE : phone CONT_VAR cierrePhone
    '''
    p[0] = f'{p[2]}'
    exportarTxt.append(['Prod. PHONE -->', p.slice])

def p_EMAIL(p):
    '''EMAIL : email CONT_VAR cierreEmail
    '''
    p[0]=f''
    exportarTxt.append(['Prod. EMAIL -->', p.slice])

def p_DATE(p):
    '''DATE : date CONT_VAR cierreDate
    '''
    p[0] = f'{p[2]}'

    exportarTxt.append(['Prod. DATE -->', p.slice])
    
def p_YEAR(p):
    '''YEAR : year CONT_VAR cierreYear
    '''
    p[0] = f'{p[2]}'
    exportarTxt.append(['Prod. YEAR -->', p.slice])

def p_HOLDER(p):
    '''HOLDER : holder CONT_VAR cierreHolder
    '''
    p[0] = f'{p[2]}'

    exportarTxt.append(['Prod. HOLDER -->', p.slice])

def p_INFORMAL_TABLE(p):
    '''INFORMAL_TABLE : informalTable TABLE_MEDIA cierreInformalTable
				| informalTable TABLE_GROUP cierreInformalTable
    '''
    p[0] = f'<table>{p[2]}</table>'
    exportarTxt.append(['Prof. INFORMAL_TABLE -->', p.slice])

def p_TABLE_MEDIA(p):
    '''TABLE_MEDIA : MEDIA_OBJECT
				| MEDIA_OBJECT TABLE_MEDIA
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}{p[2]}'
    exportarTxt.append(['Prod. TABLE_MEDIA -->', p.slice])

def p_TABLE_GROUP(p):
    '''TABLE_GROUP : TGROUP
				| TGROUP TABLE_GROUP
    '''
    if len(p)==2:
        p[0] = f'<div>{p[1]}</div>'
    else:
        p[0] = f'<div>{p[1]}</div>\n{p[2]}'
    exportarTxt.append(['Prod. TABLE_GROUP -->', p.slice])

def p_TGROUP(p):
    '''TGROUP : tgroup THEAD TBODY TFOOT cierreTgroup
				| tgroup THEAD TBODY cierreTgroup
                | tgroup TBODY TFOOT cierreTgroup
                | tgroup TBODY cierreTgroup
    '''
    if len(p)==4:   #Si la tabla solo tiene cuerpo
        p[0] = f'{p[2]}'
    elif len(p)==5:
        p[0] = f'{p[2]}\n{p[3]}'
    else:
        p[0] = f'{p[2]}\n{p[3]}\n{p[4]}'
    exportarTxt.append(['Prod. TGROUP -->', p.slice])

#-------------- Header table
def p_THEAD(p):
    '''THEAD : thead CONT_TH cierreThead
    '''
    p[0] = f'{p[2]}'
    exportarTxt.append(['Prod. THEAD -->', p.slice])

def p_CONT_TH(p):
    '''CONT_TH : ROWH
				| ROWH CONT_TH
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}\n{p[2]}'
    exportarTxt.append(['Prod. CONT_TH -->', p.slice])

def p_ROWH(p):
    '''ROWH : row CONT_ROWH cierreRow
    '''
    p[0] = f'<tr>{p[2]}</tr>'
    exportarTxt.append(['Prod. ROWH -->', p.slice])

def p_CONT_ROWH(p):
    '''CONT_ROWH : ENTRYH
				| ENTRYH CONT_ROWH
                | ENTRYTBLH
				| ENTRYTBLH CONT_ROWH
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}{p[2]}'
    exportarTxt.append(['Prod. CONT_ROWH -->', p.slice])

def p_ENTRYH(p):
    '''ENTRYH : entry CONT_ENTRY cierreEntry
    '''
    p[0] = f'<th>{p[2]}</th>'
    exportarTxt.append(['Prod. ENTRYH -->', p.slice])

def p_ENTRYTBLH(p):
    '''ENTRYTBLH : entrytbl THEAD TBODY cierreEntrytbl
				| entrytbl TBODY cierreEntrytbl
    '''
    if len(p)==4:
        p[0] = f'<th><div>{p[2]}</div></th>'
    else:
        p[0] = f'<th>{p[2]}\n{p[3]}</th>'
    exportarTxt.append(['Prod. ENTRYTBL -->', p.slice])
#----------- fin header table

def p_CONT_T(p):
    '''CONT_T : ROW
				| ROW CONT_T
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}\n{p[2]}'
    exportarTxt.append(['Prod. CONT_T -->', p.slice])

def p_TFOOT(p):
    '''TFOOT : tfoot CONT_T cierreTfoot
    '''
    p[0] = f'{p[2]}'
    exportarTxt.append(['Prod. TFOOT -->', p.slice])
    
def p_TBODY(p):
    '''TBODY : tbody CONT_T cierreTbody
    '''
    p[0] = f'{p[2]}'
    exportarTxt.append(['Prod. TBODY -->', p.slice])

def p_ROW(p):
    '''ROW : row CONT_ROW cierreRow
    '''
    p[0] = f'<tr>{p[2]}</tr>'
    exportarTxt.append(['Prod. ROW -->', p.slice])

def p_CONT_ROW(p):
    '''CONT_ROW : ENTRY
				| ENTRY CONT_ROW
                | ENTRYTBL
				| ENTRYTBL CONT_ROW
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}{p[2]}'
    exportarTxt.append(['Prod. CONT_ROW -->', p.slice])

def p_ENTRY(p):
    '''ENTRY : entry CONT_ENTRY cierreEntry
    '''
    p[0] = f'<td>{p[2]}</td>'
    exportarTxt.append(['Prod. ENTRY -->', p.slice])

def p_ENTRYTBL(p):
    '''ENTRYTBL : entrytbl THEAD TBODY cierreEntrytbl
				| entrytbl TBODY cierreEntrytbl
    '''
    if len(p)==4:
        p[0] = f'<td><div>{p[2]}</div></td>'
    else:
        p[0] = f'<td><div>{p[2]}\n{p[3]}</div></td>'
    exportarTxt.append(['Prod. ENTRYTBL -->', p.slice])

def p_CONT_ENTRY(p):
    '''CONT_ENTRY : contenido_texto
				| contenido_texto CONT_ENTRY
                | ITEMIZED_LIST
                | ITEMIZED_LIST CONT_ENTRY
                | IMPORTANT
                | IMPORTANT CONT_ENTRY
                | PARA
                | PARA CONT_ENTRY
                | SIMPARA
                | SIMPARA CONT_ENTRY
                | COMMENT
                | COMMENT CONT_ENTRY
                | ABSTRACT
                | ABSTRACT CONT_ENTRY
                | MEDIA_OBJECT
                | MEDIA_OBJECT CONT_ENTRY
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}{p[2]}'
    exportarTxt.append(['Prod. CONT_ENTRY -->', p.slice])


def p_error(p):
    # p regresa como un objeto del Lexer.
    # p.__dict__ -> ver propiedades del objeto.
    global contadorErrores
    if (p):
        print(f'Error en el parser --> Tipo: {p.type} | Valor: {p.value}')
        print('Error sintáctico en la LINEA:', p.lineno)
        exportarTxt.append(['!!! Error parser -->', p])
        
    contadorErrores += 1

parser = yacc.yacc()  # Ignorar warnings.
# error log=yacc.NullLogger()

opcionesMenu = {
    1: 'Analizar texto desde un archivo, indicando su ruta.',
    2: 'Escanear texto línea por línea (escribiendo en terminal).',
    3: 'Salir.',
}

def analizarPorRuta():
    cleanPath = pedirRuta()
    global contadorErrores
    # Ejecución "analisis de archivo de texto"
    try:
        file = open(cleanPath, "r", encoding='utf8')
        strings = file.read()
        file.close()
        result = parser.parse(strings)
        try:
            with open(f'producciones-analizadas.txt', 'w', encoding='UTF8') as f:
                f.write('Producciones analizadas por el parser:\n====================\n')
                contador = 0
                for line in exportarTxt:
                    contador += 1
                    f.write(f'{contador}) {line[0]} | {line[1]}\n')
                    f.write('---------------\n')
                f.write('====================\n')
                f.write(f'Total de tokens analizados: {contador}.\n')
            f.close()
        except:
            print('Error creando logs')
        if contadorErrores > 0:
            print('(⨉) Ocurrió un error sintáctico.')
            # Resetear contador
            contadorErrores = 0		
            reload(lexer)
            reload(yacc)
        else:
            print('✅ El archivo es sintacticamente correcto!')
            # Ejecutar exportacion de html
            # exportarHtml(strings, cleanPath)
            searchStr = '\\' if ("\\" in cleanPath) else '/'  # Reviso si el archivo se encuentra en una ruta con barras diagonales invertidas (\) o barras diagonales (/)
            rawFileName = cleanPath.split(searchStr)[-1]  # Obtengo el nombre del archivo sin la ruta
            fileName = rawFileName.split('.xml')[0]  # Obtengo el nombre del archivo sin la extensión
            contentArr = []  # Lista para almacenar el contenido del archivo HTML
            contentArr.append(
                f'''<!DOCTYPE html>\n<html>\n<head>\n\t<meta charset="utf-8">\n\t<title>{fileName}</title>\n</head>\n<body>\n'''
            )
            contentArr.append(result)

            contentArr.append('\n</body>\n</html>')  # Agrega el cierre del archivo HTML

    
    
            with open(f'{fileName}.html', 'w', encoding='UTF8') as f:
                for line in contentArr:
                    f.write(line)
            f.close()
            
            print('(✅) Sintácticamente correcto.')
            print('(!) Se exportó un .txt con las producciones analizadas.')
            reload(lexer)
            reload(yacc)
    except IOError:
        print('Ocurrió un error leyendo archivo:', cleanPath)


def analizarPorLinea():
    # Ejecución "normal"
    print('Para interrumpir la ejecucion: [ctrl] + [C] | Para volver al menu principal: _salir')
    while True:
        s = input('>> ')
        if s == '_salir':
            break
        result = parser.parse(s)
        print(result)


if __name__ == "__main__":
    logicaMenu(
        'Parser',
        opcionesMenu,
        analizarPorRuta,
        analizarPorLinea,
    )
