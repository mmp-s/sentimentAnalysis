###############################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)
# Bacharelado em Sistemas de Informacao
# IF968 -- Programacao 1
#
# Autor:    Mateus Maciel Ponciano Da Silva
#
# Email:    mmps@cin.ufpe.br
#
# Data:        2016-06-10
#
# Descricao:  Este e' um modelo de arquivo para ser utilizado para a implementacao
#                do projeto pratico da disciplina de Programacao 1. 
#                 A descricao do projeto encontra-se no site da disciplina e trata-se
#                de uma adaptacao do projeto disponivel em 
#                http://nifty.stanford.edu/2016/manley-urness-movie-review-sentiment/
#                O objetivo deste projeto e' implementar um sistema de analise de
#                sentimentos de comentarios de filmes postados no site Rotten Tomatoes.
#
# Licenca: The MIT License (MIT)
#            Copyright(c) 2016 Mateus Maciel Ponciano Da Silva
#
###############################################################################


import sys
import re

def stopWords(swFile): #verifica se a palavra e uma stop word
    file = open(swFile)
    stops = file.read()
    stopWordsList = list()
    for stopWord in stops.split():
        stopWordsList.append(stopWord)
    file.close()
    return stopWordsList

def clean_up(s):
    ''' Retorna uma versao da string 's' na qual todas as letras sao
        convertidas para minusculas e caracteres de pontuacao sao removidos
        de ambos os extremos. A pontuacao presente no interior da string
        e' mantida intacta.
    '''    
    punctuation = ''''!"',;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result



def split_on_separators(original, separators):
    '''    Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separtors' e' uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' e' uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    '''            
    return filter(lambda x: x != '',re.split('[{0}]'.format(separators),original))
                    
def mediaScore(words):
    for word in words:
        frequency = words[word][1]
        finalScore = words[word][2]/words[word][1]
        words[word] = (word, frequency, finalScore)
    return words

def readTrainingSet(trainSet, stopWordsList):
    '''    Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,freq,escore) com o escore
        medio das palavras no comentarios.
    '''
    file = open(trainSet)
    lines = file.readlines()
    frequency = 0
    words = dict()

    for line in lines:
        line = list(split_on_separators(line, " ,.\t\n"))
        for word in line[1:]:
            word = clean_up(word)
            if (word not in words) and (word not in stopWordsList) and (word != ""):
                frequency = 1
                score = int(line[0])
                words[word] = (word, frequency, score)

            elif (word in words) and (word not in stopWordsList):
                frequency = words[word][1] + 1
                score = words[word][2] + int(line[0])
                words[word] = (word, frequency, score)

            else:
                continue

    words = mediaScore(words)           
    
    file.close()
    return words

def readTestSet(testSet):
    ''' Esta funcao le o arquivo contendo o conjunto de teste
	retorna um vetor/lista de pares (escore,texto) dos
	comentarios presentes no arquivo.
    ''' 

    file = open(testSet)
    lines = file.readlines()
    reviews = list()
    for line in lines:
        reviews = reviews + [(line[0], line[2:len(line)-2])]
    file.close() 
    return reviews

def computeSentiment(review,words,stopWordsList):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario e' a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore e' 2.
        Review e' a parte textual de um comentario.
        Words e' o dicionario com as palavras e seus escores medios no conjunto
        de treinamento.
    '''

    review = list(split_on_separators(review, " '`,.\t\n"))
    score = 0.0
    palavrasAnalisadas = 0
    for word in review[1:]:
        word = clean_up(word)
        if word in words and word != "":
            score = score + words[word][2]
            palavrasAnalisadas += 1
        elif (word in stopWordsList) or (word == ""):
            continue
        else:
            score = score + 2
            palavrasAnalisadas += 1

    if palavrasAnalisadas != 0:
        sentiment = score/palavrasAnalisadas
    else:
        sentiment = 2
	
    return sentiment


def somaQuadradosLista(lista):
    quadrados=0
    for valor in lista:
        quadrados = quadrados + (valor * valor)
    return quadrados

def computeSumSquaredErrors(reviews,words,stopWordsList):
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario e' obtido com a
        funcao computeSentiment. 
        Reviews e' um vetor de pares (escore,texto)
        Words e' um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    '''
    sse = 0
    diference = list()
    for review in reviews:
        diference = diference + [int(review[0]) - computeSentiment(review[1], words, stopWordsList)]
        
    sse = somaQuadradosLista(diference)/len(reviews)
    
    return sse

def main():
    
    # Os arquivos sao passados como argumentos da linha de comando para o programa
    # Voce deve buscar mais informacoes sobre o funcionamento disso (e' parte do
    # projeto).
    
    # A ordem dos parametros e' a seguinte: o primeiro e' o nome do arquivo
    # com o conjunto de treinamento, em seguida o arquivo do conjunto de teste.
    
    if len(sys.argv) < 4:
        print ('Numero invalido de argumentos')
        print ('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste> <arq-stopWords>')
        sys.exit(0)

    stopWordsList = stopWords(sys.argv[3])

    # Lendo conjunto de treinamento e computando escore das palavras
    words = readTrainingSet(sys.argv[1], stopWordsList)
    
    # Lendo conjunto de teste
    reviews = readTestSet(sys.argv[2])
    
    # Inferindo sentimento e computando soma dos quadrados dos erros
    sse = computeSumSquaredErrors(reviews,words,stopWordsList)
    
    print ('A soma do quadrado dos erros e\': {0}'.format(sse))
            

if __name__ == '__main__':
   main()
