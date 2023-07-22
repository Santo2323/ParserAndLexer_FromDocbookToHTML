# Importaciones
import ply.lex as lex
import re
from logicaMenu import cls, logicaMenu
from helpers import pedirRuta

# Variable global que cuenta los errores encontrados
contadorErrores = 0

# SIMBOLOS TERMINALES
tokens = [
    # Etiquetas Docbook/XML
    
    'doctype',
    
    'article',
    'cierreArticle',
    
    'section',
    'cierreSection',
    
    'info',
    'cierreInfo',
    
    'simpleSection',
    'cierreSimpleSection',
    
    'title',
    'cierreTitle',
    
    'itemizedlist',
    'cierreItemizedlist',

    'important',
    'cierreImportant',
    
    'para',
    'cierrePara',
    
    'simpara',
    'cierreSimpara',

    'address',
    'cierreAddress',

    'mediaObject',
    'cierreMediaObject',
    
	'videoObject',
    'cierreVideoObject',
    
	'imageObject',
    'cierreImageObject',
    
	'videoData',
    
    'imageData',

    'informalTable',
    'cierreInformalTable',
    
    'comment',
    'cierreComment',

    'abstract',
    'cierreAbstract',
    
    'author',
    'cierreAuthor',
    
    'date',
    'cierreDate',
    
    'copyright',
    'cierreCopyright',
    
    'street',
    'cierreStreet',
    
    'city',
    'cierreCity',
    
    'state',
    'cierreState',
    
    'phone',
    'cierrePhone',
    
    'email',
    'cierreEmail',
    
    'firstname',
    'cierreFirstname',
    
    'surname',
    'cierreSurname',
    
    'year',
    'cierreYear',
    
    'holder',
    'cierreHolder',
    
    'emphasis',
    'cierreEmphasis',
    
    'listItem',
    'cierreListItem',
    
    'tgroup',
    'cierreTgroup',
    
    'thead',
    'cierreThead',
    
    'tfoot',
    'cierreTfoot',
    
    'tbody',
    'cierreTbody',
    
    'row',
    'cierreRow',
    
    'entry',
    'cierreEntry',
    
    'entrytbl',
    'cierreEntrytbl',
     
    'cierreLink',
    'link',
    
    # Contenido entre etiquetas
    'contenido_texto',
]

# Terminos referentes a expresiones regulares
# \w = caracter alfanumerico
# \s = espacio en blanco
# \S = contrario a 's'
# \d = digito decimal
# * = 0 o mas repeticiones
# + = 1 o mas repeticiones

# PLY detecta funciones que empiecen con 't_' reconociendolas como tokens
# Tokens
def t_doctype(t): r'<!DOCTYPE article>'; return(t);

def t_article(t): r'<article>'; return(t);
def t_cierreArticle(t): r'</article>'; return(t);

def t_section(t): r'<section>'; return(t);
def t_cierreSection(t): r'</section>';  return(t);

def t_info(t): r'<info>'; return(t);
def t_cierreInfo(t): r'</info>'; return(t);

def t_simpleSection(t): r'<simplesect>'; return(t);
def t_cierreSimpleSection(t): r'</simplesect>'; return(t);

def t_title(t): r'<title>'; return(t);
def t_cierreTitle(t): r'</title>'; return(t);

def t_itemizedlist(t): r'<itemizedlist>'; return (t);
def t_cierreItemizedlist(t): r'</itemizedlist>'; return (t);

def t_important(t): r'<important>'; return (t);
def t_cierreImportant(t): r'</important>'; return (t);

def t_para(t): r'<para>'; return (t);
def t_cierrePara(t): r'</para>'; return (t);

def t_simpara(t): r'<simpara>'; return (t);
def t_cierreSimpara(t): r'</simpara>'; return (t);

def t_address(t): r'<address>'; return (t);
def t_cierreAddress(t): r'</address>'; return (t);

def t_informalTable(t): r'<informaltable>'; return (t);
def t_cierreInformalTable(t): r'</informaltable>'; return (t);

def t_comment(t): r'<comment>'; return (t);
def t_cierreComment(t): r'</comment>'; return (t);

def t_abstract(t): r'<abstract>'; return (t);
def t_cierreAbstract(t): r'</abstract>'; return (t);

def t_author(t): r'<author>'; return (t);
def t_cierreAuthor(t): r'</author>'; return (t);

def t_date(t): r'<date>'; return (t);
def t_cierreDate(t): r'</date>'; return (t);

def t_copyright(t): r'<copyright>'; return (t);
def t_cierreCopyright(t): r'</copyright>'; return (t);

def t_street(t): r'<street>'; return (t);
def t_cierreStreet(t): r'</street>'; return (t);

def t_city(t): r'<city>'; return (t);
def t_cierreCity(t): r'</city>'; return (t);

def t_state(t): r'<state>'; return (t);
def t_cierreState(t): r'</state>'; return (t);

def t_phone(t): r'<phone>'; return (t);
def t_cierrePhone(t): r'</phone>'; return (t);

def t_email(t): r'<email>'; return (t);
def t_cierreEmail(t): r'</email>'; return (t);

def t_firstname(t): r'<firstname>'; return (t);
def t_cierreFirstname(t): r'</firstname>'; return (t);

def t_surname(t): r'<surname>'; return (t);
def t_cierreSurname(t): r'</surname>'; return (t);

def t_year(t): r'<year>'; return (t);
def t_cierreYear(t): r'</year>'; return (t);

def t_holder(t): r'<holder>'; return (t);
def t_cierreHolder(t): r'</holder>'; return (t);

def t_emphasis(t): r'<emphasis>'; return (t);
def t_cierreEmphasis(t): r'</emphasis>'; return (t);

def t_listItem(t): r'<listitem>'; return (t);
def t_cierreListItem(t): r'</listitem>'; return (t);

def t_tgroup(t): r'<tgroup>'; return (t);
def t_cierreTgroup(t): r'</tgroup>'; return (t);

def t_thead(t): r'<thead>'; return (t);
def t_cierreThead(t): r'</thead>'; return (t);

def t_tfoot(t): r'<tfoot>'; return (t);
def t_cierreTfoot(t): r'</tfoot>'; return (t);

def t_tbody(t): r'<tbody>'; return (t);
def t_cierreTbody(t): r'</tbody>'; return (t);

def t_row(t): r'<row>'; return (t);
def t_cierreRow(t): r'</row>'; return (t);

def t_entry(t): r'<entry>'; return (t);
def t_cierreEntry(t): r'</entry>'; return (t);

def t_entrytbl(t): r'<entrytbl>'; return (t);
def t_cierreEntrytbl(t): r'</entrytbl>'; return (t);

def t_mediaObject(t): r'<mediaobject>'; return (t);
def t_cierreMediaObject(t): r'</mediaobject>'; return (t);

def t_videoObject(t): r'<videoobject>'; return (t);
def t_cierreVideoObject(t): r'</videoobject>'; return (t);

def t_imageObject(t): r'<imageobject>'; return (t);
def t_cierreImageObject(t): r'</imageobject>'; return (t);

def t_imageData(t):
    r'<imagedata\s+fileref=["\']((?:(http[s]?|ftp[s]?)://)?(?:[\w.-]+/)*[\w.-]+\.[\w.-]+(?:\S+)?)["\']\s*/>'
    return (t)

def t_videoData(t):
    r'<videodata\s+fileref=["\']((?:(http[s]?|ftp[s]?)://)?(?:[\w.-]+/)*[\w.-]+\.[\w.-]+(?:\S+)?)["\']\s*/>'
    return (t)

def t_link(t):
    r'<link\s+xlink:href=["\']((?:(http[s]?|ftp[s]?)://)?(?:[\w.-]+/)*[\w.-]+\.[\w.-]+(?:\S+)?)["\']\s*>'
    return (t)

def t_cierreLink(t): r'</link>'; return (t);

def t_contenido_texto(t): r'[^<>\n\r]+'; return (t)

# token que ignora los saltos de linea y tabulaciones
t_ignore = ' \t\r'

# Funcion que se ejecuta al encontrar un error lexico
def t_error(t):
    global contadorErrores
    line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
    column = find_column(t.lexer.lexdata, t)
    print(f'Caracter ilegal! : \'{t.value[0]}\'| En linea: {t.lineno} | Posición: {column}')
    contadorErrores += 1
    t.lexer.skip(1)

def find_column(text, token):
    last_cr = text.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr)
    return column

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Funciones correspondientes al MENU DE OPCIONES DEL USUARIO
menu_options = {
    1: 'Analizar tokens desde un archivo, indicando su ruta.',
    2: 'Escanear tokens línea por línea.',
    3: 'Salir.',
}

def analizarPorRuta():
    pathClean = pedirRuta()
    lexer = lex.lex(reflags=re.IGNORECASE) # Bandera para que ignore mayuscula/minuscula
    # Ejecución "analisis de archivo de texto"
    try:
        file = open(pathClean,"r",encoding='utf8')
        strings = file.read()
        file.close()
        lexer.input(strings)
        analizarTokens('archivo', lexer)
    except IOError:
        print('Ocurrió un error leyendo archivo:', pathClean)

def analizarPorLinea():
    lexer = lex.lex(reflags=re.IGNORECASE) # Bandera para que ignore mayuscula/minuscula

    # Ejecución "normal"
    print('Terminar la ejecución: [ctrl] + [C] | Para volver al menú principal escribir: _salir')
    while True:
        s = input('>> ')
        if s == '_salir':
            cls()
            break;
        lexer.input(s)
        analizarTokens('normal', lexer)


# Exportacion de TOKENS ENCONTRADOS a un archivo .txt
def exportarTokens(arrAnalizar):
    global contadorErrores
    fileNameExport = f'tokens-analizados.txt'
    with open(fileNameExport, 'w', encoding='UTF8') as f:
        f.write('TOKEN | VALOR\n')
        f.write('-------------\n')
        contador = 0
        for line in arrAnalizar:
            contador += 1
            f.write(f'{contador}- {line[0]}: {line[1]}')
            f.write('\n')
        f.write('-------------\n')
        f.write(f'Total de tokens válidos analizados: {contador}.\n')
        if (contadorErrores > 0):
            f.write(f'Total de tokens NO válidos: {contadorErrores}.')
    f.close()
    if (contadorErrores > 0):
        print('(⨉) El lexer NO acepta este archivo.')
    else:
        print('(✅) El lexer ACEPTA este archivo.')
    print('(!) Se exportó un .txt con los tokens analizados.')

# Se pasa como argumento al objeto lexer ya que,
# la expresion de `t_contenido_texto` debe ser sobreescrita
# según el modo de ejecución.
def analizarTokens(modoEjecucion, lexer):
        global contadorErrores
        exportArray = []
        while True:
                tok = lexer.token()
                if not tok:
                    if (modoEjecucion == 'archivo'):
                        exportarTokens(exportArray)
                    break
                if (modoEjecucion == 'archivo'):
                    exportArray.append([tok.type,tok.value]);
                else: print(f'Tipo: {tok.type} | Valor: {tok.value}')

# Solo si se ejecuta desde lexer.py hacer...
if __name__ == "__main__":
    logicaMenu(
        'Lexer',
        menu_options,
        analizarPorRuta,
        analizarPorLinea,
    )
else:
    # Se exporta al `lexer` para que pueda ser ocupado desde,
    # por ejemplo, el parser.
    lexer = lex.lex(reflags=re.IGNORECASE) # Bandera para que ignore mayuscula/minuscula
