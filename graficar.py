from numpy import *
from matplotlib import pyplot
import datetime as dt

time_format = "%d-%m-%y %H:%M:%S"

fname = 'caso_1_camara_de_curado.csv' #Caso 1: Camara de curado
#fname = 'caso_2_intemperie.csv'       #Caso 2: Intemperie


archivo = open(fname) 

sensores=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

tiempo = []
primer_paso = True
for linea in archivo:
    lin = linea.split(',')
    sens = 0
    dia = lin[0]
    hora = lin[1]

    if primer_paso:
        t1 = dt.datetime.strptime(dia+" "+hora,time_format)
        primer_paso = False
    t2 = dt.datetime.strptime(dia+" "+hora,time_format)
    t = (t2 - t1).total_seconds()

    print(f"{dia} {hora} -->  t1 = {t1} t2 = {t2} dt = {t}")

    tiempo.append(t)

    for i in [3,5,7,9,11,13,15,17,19,21,23,25,27,29,31]:
        if i ==31:
            sensores[sens].append(float(lin[i][:-1]))
            sens+=1
        else:
            sensores[sens].append(float(lin[i]))
            sens+=1
#print (sensores[-1])
pyplot.title(fname)
pyplot.xlabel("Tiempo (Dias)")
pyplot.ylabel("Temperatura (Celcius)")

for i in range(15):
    pyplot.plot(array(tiempo)/(24*3600),sensores[i],label=f'Sensor{i+1}')
    pyplot.legend(loc='upper right')
pyplot.savefig(fname.replace(".csv",".png"))
pyplot.show()