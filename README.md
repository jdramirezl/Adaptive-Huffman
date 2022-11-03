# Adaptive-Huffman {#title}

> Adaptive-Huffman es un metodo de compresion Lossless que es una mejora sobre su version original de Huffman Encoding. La version nueva fue mejorado con la propuesta de FGK y Vitter, los cuales generan la compresion en un solo recorrido

## Tabla de contenidos

- [Adaptive-Huffman {#title}](#adaptive-huffman-title)
  - [Tabla de contenidos](#tabla-de-contenidos)
  - [Informacion general](#informacion-general)
  - [Tecnologias usadas](#tecnologias-usadas)
  - [Formulacion](#formulacion)
    - [Criterios de econding](#criterios-de-econding)

## Informacion general

- Esta es una implementacion del Adaptive-Huffman en el lenguaje Python
- Recibe Strings por consola y los comprime en un archivo binario

## Tecnologias usadas

- Python

## Formulacion

- Tamano del alfabeto: 107
- Nodos del arbol (Max): 2n-1 = 213
- Fixed code (e & r): m = 2^e + r -> e = 6, r = 43 -> (107) = (64) + 43

### Criterios de econding
Para el simbolo A_k lo guardamos en binario asi: 
- if 1 <= k <= r(e+1): k - 1 in e + 1 bits
- if k > 2r: k - r - 1 in e bits

