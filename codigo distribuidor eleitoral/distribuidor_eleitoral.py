from csv import reader
from numpy import array
from matplotlib import pyplot as plt 
from pandas import read_csv

def teto(x):
    """Retorna o valor de um numero arredondado para cima"""
    if x%1!=0:
        return int(x//1 + 1)
    return int(x)

def Euclidean_Distance(x0, y0, x1, y1):
    """Distancia euclidiana entre 2 pontos"""
    return (((x0 - x1)**2) + ((y0 - y1)**2))**0.5

def get_Data_From(arq):
    """Le o arquivo e retorna os valores"""
    values = list(reader(open(arq), delimiter=","))
    values = array(values).astype("float")
    return values

def main():
    def mudar_Entrada():
        """Realiza alterações nos dados dos eleitores e urnas"""
        manter = ""
        while manter!=True and manter!=False:
            manter = input("\n-> Manter dados atuais - Pressione(s | n)\n-> Sair - Pressione(e)\n")
            if manter == "s":
                manter = True
            elif manter =="n":
                manter = False
            elif manter == "e":
                return False
        if not manter:
            from random import uniform
            eleitores = 0
            while eleitores>100000 or eleitores<1:
                eleitores = int(input("Escolha o número de eleitores[1-100.000]: "))
            urnas = 0
            while urnas>10 or urnas<1:
                urnas = int(input("Escolha o número de urnas[1-10]: "))
            arq = open("eleitores.csv","w")
            for i in range(eleitores):
                arq.write(str(uniform(1,100)) + "," + str(uniform(1,100)) + "\n")
            arq.close()
            arq = open("urnas.csv","w")
            for i in range(urnas):
                arq.write(str(uniform(1,100)) + "," + str(uniform(1,100)) + "\n")
            arq.close()   
        return True       
    def mudar_Tolerancia():
        """altera % máximo de eleitores em cada urna"""
        tolerancia = 0
        minimo = 100//(len(get_Data_From("urnas.csv")))
        while tolerancia>100 or tolerancia<minimo: #0 a 1, percentual maximo de pessoa por urna, minimo sera o numero de 100 / n urnas
            tolerancia = int(input("Escolha o percentual máximo de pessoas por urna["+str(minimo)+"-100]%: "))
        return tolerancia/100
    def iteracoes_Distancia_Eleitor_Urna():
        """Retorna lista com as iteracoes de distancia entre as urnas e os eleitores"""
        nonlocal eleitores, urnas
        distancias = []
        print("\nCalculando distancias de eleitor<--->urna ...")
        finalizado = 0
        for i in range(len(eleitores)):
            for j in range(len(urnas)):
                #[[[cordX,cordY],[cordX,cordY],distance, indiceUrna]]
                distancias.append([(eleitores[i][0], eleitores[i][1]), (urnas[j][0], urnas[j][1]), Euclidean_Distance(eleitores[i][0], eleitores[i][1], urnas[j][0], urnas[j][1]), j])      
                finalizado += 1
                try:
                    if finalizado%int(len(eleitores)*len(urnas)/6) == 0:
                        print(teto(finalizado*100/(len(eleitores)*len(urnas))), "%")
                except:
                    pass
        print("")
        distancias.sort(key = lambda x: x[2])
        return distancias
    def seleciona_Eleitores_De_Cada_Urna():
        """Retorna dicionario com o eleitor e a urna que ele deve votar,
        a relacao de vagas restante em cada urna, e o maximo de vagas por urna"""
        nonlocal tolerancia, eleitores, urnas, maxEleitores, distancias
        lotacaoUrnas = [int(maxEleitores)]*(len(urnas))
        if len(eleitores)*tolerancia > maxEleitores: #Percentual maximo de eleitores por urna
            lotacaoUrnas = [int(len(eleitores)*tolerancia)]*(len(urnas))
        lotacaoMaxima = lotacaoUrnas[0]
        resultado = dict()
        finalizado = 0
        print("Selecionando eleitores de cada urna...")
        for i in distancias:
            finalizado+=1
            try:
                if finalizado%int(len(distancias)/6)==0:
                    print(teto(finalizado*100/len(distancias)),"%")
            except:
                pass
            if lotacaoUrnas[i[3]]>0:
                temp = len(resultado)
                resultado.setdefault(i[0], i[3])
                if (len(resultado)!= temp):
                    lotacaoUrnas[i[3]] -= 1
        print("")
        return resultado, lotacaoUrnas, lotacaoMaxima
    def salva_Eleitores_De_Cada_Urna():
        """Faz um backup das selecoes realizadas em 2 arquivos,
        e retorna a legenda a ser inserida no grafico"""
        nonlocal eleitores, vagasPorUrna, maxVagas
        arq = open("eleitoresResultado.csv","w")
        arq.write("x,y,urna\n")
        for i in eleitores:
            arq.write(str(i[0]) + "," + str(i[1]) + "," + str(resultado.get((i[0], i[1])) + 1) + "\n")
        arq.close()
        arq2 = open("urnasResultado.csv","w")
        arq2.write("x,y,urna\n")
        legenda = []
        for index,i in enumerate(urnas):
            arq2.write(str(i[0]) + "," + str(i[1]) + "," + str(index+1) + "\n")
            legenda.append(str(maxVagas - vagasPorUrna[index]) + " (" + str(round((maxVagas - vagasPorUrna[index])*100/len(eleitores))) + "%)") 
        arq2.close()
        return legenda
    def mostrar_Resultados():
        """Mostra tudo que foi calculado de forma gráfica"""
        nonlocal legenda
        plt.figure(figsize=(6, 6))
        plt.subplot(1, 1, 1)
        plt.axis("equal")
        data1 = read_csv("eleitoresResultado.csv") #Gerar arquivo com dados finais
        data2 = read_csv("urnasResultado.csv")
        from itertools import cycle
        color = ["blue", "orange", "green","red", "purple", "brown", "pink", "gray", "olive", "cyan"]
        colors = cycle(["blue", "orange", "green","red", "purple", "brown", "pink", "gray", "olive", "cyan"])
        for name, group in data1.groupby("urna"):
            plt.scatter(group["x"], group["y"], marker="^", color=color[name-1]) #ms = marker size
        colors = cycle(["blue", "orange", "green","red", "purple", "brown", "pink", "gray", "olive", "cyan"])
        for name, group in data2.groupby("urna"):
            plt.plot(group["x"], group["y"], marker="X", linestyle="", label=name, ms=12, color=next(colors), markerfacecolor='black') #ms = marker size
        plt.grid(True)
        plt.legend(legenda, loc="center right", bbox_to_anchor=(1.12, 0.5))
        plt.title("Eleições")
        plt.show()
        # plt.savefig("eleicoes.svg")

    sair = mudar_Entrada()
    if not sair:
        return sair
    tolerancia = mudar_Tolerancia()
    eleitores = get_Data_From("eleitores.csv")
    urnas = get_Data_From("urnas.csv")
    maxEleitores = teto(len(eleitores)/len(urnas))
    distancias = iteracoes_Distancia_Eleitor_Urna()
    resultado, vagasPorUrna, maxVagas = seleciona_Eleitores_De_Cada_Urna()
    legenda = salva_Eleitores_De_Cada_Urna()
    mostrar_Resultados()
    return sair
    
sair = True
while sair:
    sair = main()