from matplotlib.pylab import *
from matplotlib import cm


#Geometría
a = 0.5 #Alto
b = 1.04 #Ancho
Nx = 52 #Intervalos en X
Ny = 25 #Intervalos en Y

dx = b / Nx #Discretizacion en X
dy = a / Ny #Discretizacion en Y


if dx != dy:
    print("Error: dx y dy no son iguales")
    exit(-1)   

h = dx

#Coordenadas del punto (i,j)
def coords(i, j): return (dx * i, dy * j)


x, y = coords(4, 2)

print("x: ",x)
print("y: ",y)

import numpy as np
from scipy.interpolate import interp1d

#Curva de calor de hidratacion en el tiempo (ingresar t en segundos), entrega el calor de 
#hidratacion en kJ/m^3*s considerando una dosificacion DC en kg de cemento por m^3 
#DC por default se considera 360 kg/m^3
def Calor_de_hidratacion(t,DC = 360.):      #[tiempo, Dosificacion cemento en kg/m^3]
    #datos registrados por ensayo semi-adiabatico de Langavant

    x = [0, 130, 250, 400, 540, 720, 900, 1100, 1300, 1500, 1800, 3600, 5400, 7200,
        9000, 10800, 14400, 18000, 21500, 25200, 28000, 32400, 36000, 39600, 43200, 46800,
        50000, 54000, 61200, 72000, 79200, 86400, 100800, 111600, 122400, 133200, 144000, 180000,
        216000, 234000, 259200, 288000, 324000, 360000, 432000, 468000, 504000, 540000, 604800, 
        648000, 684000, 720000, 756000, 792000, 828000, 864000, 900000, 936000, 972000, 1008000, 1044000,
        1080000, 1116000, 1152000, 1188000, 1224000]

    y = [0.0, 0.019230769, 0.016666667, 0.013333333, 0.010714286, 0.009444444, 0.007222222,
        0.006, 0.005150000, 0.00385, 0.003, 0.001444444, 0.001055556, 0.000722222, 0.000833333, 
        0.001111111, 0.002166667, 0.003472222, 0.005285714, 0.006756757, 0.007142857, 0.007272727, 
        0.006944444, 0.006250000, 0.005277778, 0.004027778, 0.003281250, 0.0025, 0.001875, 0.001111111, 
        0.000833333, 0.000694444, 0.000416667, 0.000296296, 0.000194444, 0.000111111, 0.000064815, 0.000027778, 
        0.000013889, 0.000027778, 0.000031746, 0.000031250, 0.000038889, 0.000061111, 0.000076389, 0.000072222, 
        0.000066667, 0.000055556, 0.000046296, 0.000023148, 0.000019444, 0.000030556, 0.000033333, 0.000041667, 
        0.000033333, 0.000030556, 0.000033333, 0.000041667, 0.000033333, 0.000030556, 0.000033333, 0.000041667, 
        0.000033333, 0.000030556, 0.000033333, 0.000041667]
    
    q = interp1d(x,y)


    return q(t)*DC








def imshowbien(u):
    imshow(u.T[Nx::-1, :], cmap=cm.coolwarm, interpolation = "bilinear")
    cbar = colorbar(extend="both", cmap=cm.coolwarm)
    ticks = arange(0, 65, 5)
    ticks_Text = ["{}".format(deg) for deg in ticks]
    cbar.set_ticks(ticks)
    cbar.set_ticklabels(ticks_Text)
    clim(0, 60)
    
    xlabel("b")
    ylabel("a")
    xTicks_N = arange(0, Nx + 1, 3)
    yTicks_N = arange(0, Ny + 1, 3)
    xTicks = [coords(i, 0)[0] for i in xTicks_N]
    yTicks = [coords(0, i)[1] for i in yTicks_N]
    xTicks_Text = ["{0:.2f}".format(tick) for tick in xTicks]
    yTicks_Text = ["{0:.2f}".format(tick) for tick in yTicks]
    xticks(xTicks_N, xTicks_Text, rotation="vertical")
    yticks(yTicks_N, yTicks_Text)
    margins(0.2)
    subplots_adjust(bottom = 0.15)
    

u_k = zeros((Nx + 1, Ny + 1), dtype=double)
u_km1 = zeros((Nx + 1, Ny + 1), dtype=double)

#Condicion de Borde Inicial
u_k[:, :] = 20. #Son 20 grados en todas partes

#Parámetros para el hormigon
dt = 0.01 #s
K = 1.495 #m^2/s
c = 1023. #J/Kg*C
rho = 2476. #Kg/m^3
alpha = K * dt / (c * rho * dx**2)

#Informacion interesante
print(f"dt = {dt}")
print(f"dx = {dx}")
print(f"K = {K}")
print(f"c = {c}")
print(f"rho = {rho}")
print(f"alpha = {alpha}")

#Loop en el tiempo
minuto = 60.
hora = 3600.
dia = 24 * 3600.

dt = 1 * minuto
dnext_t = 0.5 * hora

next_t = 0
framenum = 0

T = 1 * dia
Days = 2 * T #Cantidad de Dias a Simular

q = Calor_de_hidratacion(Days)

#Vectores con temperatura acumulada
u_0 = zeros(int32(Days / dt))
u_N4 = zeros(int32(Days / dt))
u_2N4 = zeros(int32(Days / dt))
u_3N4 = zeros(int32(Days / dt))

P1 = zeros(int32(Days / dt))
P2 = zeros(int32(Days / dt))
P3 = zeros(int32(Days / dt))

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n* multiplier) / multiplier


for k in range(int32(Days/dt)):
    t = dt * (k + 1)
    dias = truncate(t / dia, 0)
    horas = truncate((t - dias *dia) / hora, 0)
    minutos = truncate((t - dias * dia -horas * hora) / minuto, 0)
    titulo = "k = {0:05.0f}".format(k) + " t = {0:02.0f}d {1:02.0f}h {2:02.0f}m ".format(dias, horas, minutos)
    print(titulo)
    
    Tambiental = 20. + 10.*sin((2*pi/T)*t)
    
#Condiciones de Borde Eseciales    
    u_k[0, :] = u_k[1, :] - 0. * dx #Borde Izquierdo
    u_k[:, 0] = u_k[:, 1] - 0. * dy #Borde Inferior
    u_k[:, -1] = Tambiental #Borde Superior
    u_k[-1, :] = u_k[-2, :] + 0. * dx #Borde Derecho
    


    # Loop en el espacio desde i = 1, hasta i = n-1
    for i in range(1,Nx):
        for j in range(1,Ny):
            
            #Algortimo de diferencias finitas en 2-D para difusion
            
            #Laplaciano
            nabla_u_k = (u_k[i-1, j] + u_k[i+1, j] + u_k[i, j-1] + u_k[i, j+1] - 4 * u_k[i,j]) / h**2
            
            #Forard Euler
            u_km1[i,j] = u_k[i,j] + alpha * nabla_u_k + q
            
    #Avanzar la solucion a k + 1
    u_k = u_km1
    
    #Reetablecen condiciones de Borde para asegurar cumplimiento
    u_k[0, :] = u_k[1, :] - 0. * dx #Borde Izquierdo
    u_k[:, 0] = u_k[:, 1] - 0. * dy #Borde Inferior
    u_k[:, -1] = Tambiental #Borde Superior
    u_k[-1, :] = u_k[-2, :] + 0. * dx #Borde Derecho
    
    u_0[k] = u_k[int(Nx / 2), -1]
    u_N4[k] = u_k[int(Nx / 2), int(Ny / 4)]
    u_2N4[k] = u_k[int(Nx / 2), int(2 * Ny / 4)]
    u_3N4[k] = u_k[int(Nx / 2), int(3 * Ny / 4)]

    P1[k] = u_k[int(Nx / 2), int(Ny / 4)]
    P2[k] = u_k[int(Nx / 2), int(3* Ny / 4)]
    P3[k] = u_k[int(3*Nx / 4), int(3 * Ny / 4)]
    
    #Graicando en d_next
    if t >= next_t:
        figure(1)
        imshowbien(u_k)
        title(titulo)
        savefig("Caso_xz/frame_{0:04.0f}.png".format(framenum))
        framenum += 1
        next_t += dnext_t
        close(1)
        
        
