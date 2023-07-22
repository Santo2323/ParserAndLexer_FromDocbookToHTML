import re

def pedirRuta():
  # Pedir ruta del archivo por input
  pathFile = input('Ingrese la ruta del archivo que desea analizar: ')
  # Remover comillas
  pathClean = re.sub(
      r'\'|"',
      '',
      pathFile
  )
  return pathClean.strip()