# import re

# documentTitleExpr = r'<article>[\w\W]+?<title>([\w\W]+?)(?=<\/)'

# sectionTitleExpr = r'<section>[\w\W]+?<title>([\w\W]+?)(?=<\/)'

# paraExpr = r'<para>([\w\W]+?)(?=<\/)</para>'
# simparaExpr = r'<simpara>([\w\W]+?)(?=<\/)</simpara>'

# infoContentExpr = r'<info>([\w\W]*?)<\/info>'

# importantExpr = r'<important>([\w\W]*?)<\/important>'

# itemizedListExpr = r'<itemizedlist>([\w\W]*?)<\/itemizedlist>'
# listItemExpr = r'<listitem>([\w\W]*?)<\/listitem>'

# tagContentExpr = r'<([^>]+)>(.*?)<\/\1>'
# innerTagsExpr = r'<(\w+)>([\w\W]*?)<\/\>'

# linkExpr = r'<link xlink:href="([^"]*)" >([^<]*)</link>'

# tableExpr = r'<informaltable>([\w\W]*?)</informaltable>'

# theadExpr = r'<thead>([\w\W]*?)</thead>'
# tbodyExpr = r'<tbody>([\w\W]*?)</tbody>'
# tfootExpr = r'<tfoot>([\w\W]*?)</tfoot>'




# tagExpr = r'<\/?[a-zA-Z]+\b[^>]*>'


# def exportarHtml(fileContent, pathFile):  # Recibo el contenido del archivo y su path
  
#     searchStr = '\\' if ("\\" in pathFile) else '/'  # Reviso si el archivo se encuentra en una ruta con barras diagonales invertidas (\) o barras diagonales (/)

#     rawFileName = pathFile.split(searchStr)[-1]  # Obtengo el nombre del archivo sin la ruta
#     fileName = rawFileName.split('.xml')[0]  # Obtengo el nombre del archivo sin la extensión
    
#     contentArr = []  # Lista para almacenar el contenido del archivo HTML
#     contentArr.append(
#         f'''<!DOCTYPE html>\n<html>\n<head>\n\t<meta charset="utf-8">\n\t<title>{fileName}</title>\n</head>\n<body>'''
#     )
    
 
#     # Extraer información del canal
#     cdocumentTitle = f'<H1>{re.findall(documentTitleExpr, fileContent)[0].strip()}</H1>'  # Busca y captura el título del Documento y lo envuelve en la etiqueta <h1>
#     contentArr.extend([cdocumentTitle])  
        
#     csectionsTitle = re.findall(sectionTitleExpr, fileContent)   # Busca y captura todos los titulos de secciones
    
#     for section in csectionsTitle:
#       csectionTitle = f'<H2>{section}</H2>'  # Busca y captura todos los titulos de secciones y lo envuelve en la etiqueta <h2>
#       contentArr.extend([csectionTitle])  

#     cInfo = re.findall(infoContentExpr, fileContent)  # DETECTO TODO EL CONTENIDO DEL INFO
    
#     tagsIntoInfo = detectTagsIntoInfo(cInfo)  # Detecto cada tag dentro de info y lo devuelvo
    
#     for tags in tagsIntoInfo:
#       contentArr.extend([tags])   # Por cada tag de info correcto, lo anado al html de salida
      
#     cImportant = re.findall(importantExpr, fileContent)
#     tagsIntoImportant = detectTagsIntoImportant(cImportant)
    
#     for tagsImpo in tagsIntoImportant:
#       contentArr.extend([tagsImpo]) 
      
#     citemizedlist = re.findall(itemizedListExpr, fileContent)
    
#     tagsIntoIL = tagsIntoItemizedList(citemizedlist)
    
#     for tags in tagsIntoIL:
#       contentArr.extend([tags])
      
#     cPara = re.findall(paraExpr, fileContent)
    
#     tagsPara = tagsIntoPara(cPara)
    
#     for tagsP in tagsPara:
#       contentArr.extend([tagsP])
      
#     cSimPara = re.findall(simparaExpr, fileContent)
    
#     tagsSimPara = tagsIntoSimPara(cSimPara)
    
#     for tagsSP in tagsSimPara:
#       contentArr.extend([tagsSP])
      
#     linksTagsContent = re.findall(linkExpr,fileContent)
#     for links in linksTagsContent:
#       clink = f' <a href="{links[0]}"> {links[1]} </a>'
#       contentArr.extend([clink])
    
#     tableTagsContent = re.findall(tableExpr, fileContent)
#     tagsOfTable = tagsIntoTable(tableTagsContent)
    
#     for tagsTable in tagsOfTable:
#       contentArr.extend([tagsTable])

        
      
    
    
    
    
#     # for important in cimportant:
#     #   removido = f'<div style="background-color:red; color: white; font-size:8px;"> {removeTags(important)} </div>' 
#     #   contentArr.extend([removido])  

#     # cparas = re.findall(paraExpr, fileContent)

#     # for para in cparas:
#     #   cpara = f'<p>{para}</p>'
#     #   contentArr.extend([cpara])  


#     contentArr.append('\n</body>\n</html>')  # Agrega el cierre del archivo HTML
    
    
    
#     with open(f'{fileName}.html', 'w', encoding='UTF8') as f:
#       for line in contentArr:
#         f.write(line)
#     f.close()
    
# def removeTags(match):
#     content = match
#     encontrado = re.findall(tagExpr, match)
#     print(
#           )
    
#     # if encontrado != []:
#     #   cparas = re.findall(paraExpr, match)
#     #   for para in cparas:
#     #     cpara = f'<p>{para}</p>'
#     #     return [cpara] 
    
# def detectTagsIntoInfo(match):
#   tagsArray = []
#   for content in match:
#     detectados = re.findall(tagContentExpr, content) # POR CADA TAG, DEBO CONVERTIRLO A UN PARRAFO CON FONDO VERDE, LETRA DE COLOR BLANCO Y 8 PX
#     for detectado in detectados:
#       if(detectado[0] != 'title') and (detectado[0] != 'para') and (detectado[0] != 'simpara') and (detectado[0] != 'link')  :
#         tagsArray.append(f'<p style= background-color:green; color:white; font-size:8px>{detectado[1]}</p>')   # VER SI ES TITLE Y TRANSFORMARLO A H1, SI ES PARA, TRANSFORMARLO A PARA, SI ES SIMPARA, TRANSFORMARLO EN SIMPARA
#   return tagsArray  

# def detectTagsIntoImportant(match):
#   tagsArray=[]
#   if(match == []):
#     return []
#   tagsArray.append(f'<div style="background-color:red; color:white;">')
#   for content in match:
#     detectados = re.findall(tagContentExpr, content)
#     for detectado in detectados:
#       if(detectado[0] == 'para'):
#         tagsArray.append(f'<p> {detectado[1]} </p>')
#       elif(detectado[0] != 'title') and (detectado[0] != 'para') and (detectado[0] != 'simpara') and (detectado[0] != 'link')and (detectado[0] != 'link'):
#         tagsArray.append(f'{detectado[1]}')
#   tagsArray.append(f'</div>')
#   return tagsArray


# def tagsIntoItemizedList(match):
#   tagsArray =[]
#   if(match == []):
#     return []
#   tagsArray.append('<ul>')   
#   for content in match:
#     detectados = re.findall(listItemExpr, content)
#     for detectado in detectados:
#       tagsArray.append(f'<li> {detectado} </li> ')
#   tagsArray.append('</ul>')
#   return tagsArray

# def tagsIntoPara(match):
#   tagsArray = []
#   for content in match:
#     tagsArray.append(f'<p> {content} </p>')
#   return tagsArray

# def tagsIntoSimPara(match):
#   tagsArray  = []
#   for content in match:
#     tagsArray.append(f'<p> {content} </p>')
#   return tagsArray


# def tagsIntoTable(match):
#   tagsArray = []
#   if(match == []):
#     return []
#   tagsArray.append('<table>')   
#   for content in match:
#     detectados = re.findall(theadExpr, content)
#     tagsArray.append('<thead>')
#     for detectado in detectados:
#         detectados2 = re.findall(tagContentExpr, detectado)
#         tagsArray.append('<tr>')
#         for detectado2 in detectados2:
#           tagsArray.append(f'<th>{detectado2[1]}</th> ')
#         tagsArray.append('</tr>')
#     tagsArray.append('</thead>')
  
#     detectadosBody = re.findall(tbodyExpr, content)
#     tagsArray.append('<tbody>')
#     for detectadoeEnBody in detectadosBody:
#       detectarRows = re.findall(tagContentExpr, detectadoeEnBody)
#       tagsArray.append('<tr>')
#       for detectarEntrys in detectarRows:
#           tagsArray.append(f'<td>{detectarEntrys[1]}</td> ')
#       tagsArray.append('</tr>')
#     tagsArray.append('</tbody>')
#   tagsArray.append('</table>')
  
#   return tagsArray
    




          

      