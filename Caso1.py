from matplotlib.pylab import *
from matplotlib import cm
from calor_de_hidratacion import Calor_de_hidratacion as q

#Geometría
a = 0.54 #Alto en m (540 cm) 
b = 0.5 #Ancho en m (500 cm) 
c = 1.04 #Profundidad en m (1040 cm)


# como todos los valores son pares dividiremos por 2 para obtener los Nx, Ny y Nz

Nx = 27 #Intervalos en X
Ny = 25 #Intervalos en Y
Nz = 52 #Intervalos en Z


dx = a / Nx #Discretizacion en X
dy = b / Ny #Discretizacion en Y
dz = c / Nz #Discretizacion en Z

if dx != dy or dx != dz or dy != dz:
    print("Error: dx, dy  y dz no son iguales")
    exit(-1)   

h = dx

#Coordenadas del punto (i,j,k)
coords = lambda i, j, k : (dx*i, dy*j, dz*k)



def imshowbien(u):
    imshow(u.T[Nx::-1,:],cmap=cm.coolwarm, interpolation='bilinear')
    cbar = colorbar(extend='both', cmap=cm.coolwarm)
    ticks = arange(0,35,5)
    ticks_Text=["{}°".format(deg) for deg in ticks]
    cbar.set_ticks(ticks)
    cbar.set_ticklabels(ticks_Text)
    clim(0, 30)
    
    xlabel('b')
    ylabel('a')
    xTicks_N = arange(0, Nx+1, 3)
    yTicks_N = arange(0, Ny+1, 3)
    xTicks =[coords(i,0)[0] for i in xTicks_N]
    yTicks =[coords(0,i)[1] for i in yTicks_N]
    xTicks_Text = ["{0:.2f}".format(tick) for tick in xTicks]
    yTicks_Text = ["{0:.2f}".format(tick) for tick in yTicks]
    xticks(xTicks_N,xTicks_Text, rotation='vertical')
    yticks(yTicks_N,yTicks_Text)
    margins(0.2)
    subplots_adjust(bottom=0.15)
    

u_k = zeros((Nx + 1, Ny + 1, Nz +1), dtype=double)
u_km1 = zeros((Nx + 1, Ny + 1, Nz + 1), dtype=double)

#Condicion de Borde Inicial
u_k[:, :, :] = 20. #Son 20 grados en todas partes

#Parámetros para el hierro
dt = 0.01 #s
K = 0.001495 
c = 1.023 
rho = 2476. 
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
Days = 1 * T #Cantidad de Dias a Simular

#Vectores con temperatura acumulada

sensor1 = zeros(int32(Days / dt))
sensor2 = zeros(int32(Days / dt))
sensor3 = zeros(int32(Days / dt))
sensor4 = zeros(int32(Days / dt))
sensor5 = zeros(int32(Days / dt))
sensor6 = zeros(int32(Days / dt))
sensor7 = zeros(int32(Days / dt))
sensor8 = zeros(int32(Days / dt))
sensor9 = zeros(int32(Days / dt))
sensor10 = zeros(int32(Days / dt))
sensor11 = zeros(int32(Days / dt))
sensor12 = zeros(int32(Days / dt))
sensor13 = zeros(int32(Days / dt))
sensor14 = zeros(int32(Days / dt))
sensor15 = zeros(int32(Days / dt))
sensor16 = zeros(int32(Days / dt))

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

    t_ambiental = 20. + 10 * sin((2 * pi / T) * t)   
    
#Condiciones de Borde Eseciales    
    u_k[0, :, :] = u_k[ -2 ,: , : ] #Cara izquierda
    u_k[-1, :, :] = u_k[ -2 ,: , : ] #Cada derecha
    u_k[:, -1, :] = t_ambiental #Cara superior
    u_k[:, 0, :] = u_k[ : ,-2 , : ]  #Cara inferior
    u_k[:, :, 0] = u_k[ : ,: , -2 ] #Cara atras
    u_k[:, :, -1] = u_k[ : ,: , -2 ] #Cara frente
    


    # Loop en el espacio desde i = 1, hasta i = n-1
    for i in range(1,Nx):
        for j in range(1,Ny):
            for k in range(1, Nz):
            
                #Algortimo de diferencias finitas en 2-D para difusion
                
                #Laplaciano
                nabla_u_k = (u_k[i-1, j,k] + u_k[i+1, j,k] + u_k[i, j-1,k] + u_k[i, j+1,k] + u_k[i, j, k-1]
                 + u_k[i, j, k+1] - 6 * u_k[i,j,k]) 
                
                #Forard Euler
                u_km1[i,j,k] = u_k[i,j,k] + alpha * nabla_u_k + q(t,DC = 360.)
                
    #Avanzar la solucion a k + 1
    u_k = u_km1
    
    #Reetablecen condiciones de Borde para asegurar cumplimiento

    u_k[0, :, :] = u_k[ -2 ,: , : ] #Cara izquierda
    u_k[-1, :, :] = u_k[ -2 ,: , : ] #Cada derecha
    u_k[:, -1, :] = t_ambiental #Cara superior
    u_k[:, 0, :] = u_k[ : ,-2 , : ]  #Cara inferior
    u_k[:, :, 0] = u_k[ : ,: , -2 ] #Cara atras
    u_k[:, :, -1] = u_k[ : ,: , -2 ] #Cara frente
    
    sensor1[k] = u_k[int(Nx / 2), int(Ny * 30 / 500), int(Nz / 2)]
    sensor2[k] = u_k[int(Nx / 2), int(Ny * 140 / 500), int(Nz / 2)]
    sensor3[k] = u_k[int(Nx / 2), int(Ny / (500/250)), int(Nz / 2)]
    sensor4[k] = u_k[int(Nx / 2), int(Ny / (500/360)), int(Nz / 2)]
    sensor5[k] = u_k[int(Nx / 2), int(Ny / (500/470)), int(Nz / 2)]
    sensor6[k] = u_k[int(Nx / (540/30)), int(Ny / 2), int(Nz / 2)]
    sensor7[k] = u_k[int(Nx / (540/510)), int(Ny / 2), int(Nz / 2)]
    sensor8[k] = u_k[int(Nx / (540/30)), int(Ny / 2), int(Nz / 2)]
    sensor9[k] = u_k[int(Nx / (540/150)), int(Ny / 2), int(Nz / 2)]
    sensor10[k] = u_k[int(Nx / (540/270)), int(Ny / 2), int(Nz / 2)]
    sensor11[k] = u_k[int(Nx / (540/390)), int(Ny / 2), int(Nz / 2)]
    sensor12[k] = u_k[int(Nx / (540/510)), int(Ny / 2), int(Nz / 2)]
    sensor13[k] = u_k[int(Nx / 2), int(Ny / 2), int(Nz / (1040/30))]
    sensor14[k] = u_k[int(Nx / 2), int(Ny / 2), int(Nz / (1040/275))]
    sensor15[k] = u_k[int(Nx / 2), int(Ny / 2), int(Nz / (1040/765))]
    sensor16[k] = u_k[int(Nx / 2), int(Ny / 2), int(Nz / (1040/1010))]

    #Graicando en d_next
    #if t >= next_t:
     #   figure(1)
      #  imshowbien(u_k)
       # title(titulo)
        #savefig("Caso1/frame_{0:04.0f}.png".format(framenum))
        #framenum += 1
        #next_t += dnext_t
        #close(1)
        
        
#Ploteo puntos interesantes
figure(1)
plot(range(int32(Days / dt)), sensor1, label='Sensor1')
plot(range(int32(Days / dt)), sensor2, label='Sensor2')
plot(range(int32(Days / dt)), sensor3, label='Sensor3')
plot(range(int32(Days / dt)), sensor4, label='Sensor4')
plot(range(int32(Days / dt)), sensor5, label='Sensor5')
plot(range(int32(Days / dt)), sensor6, label='Sensor6')
plot(range(int32(Days / dt)), sensor7, label='Sensor7')
plot(range(int32(Days / dt)), sensor8, label='Sensor8')
plot(range(int32(Days / dt)), sensor9, label='Sensor9')
plot(range(int32(Days / dt)), sensor10, label='Sensor10')
plot(range(int32(Days / dt)), sensor11, label='Sensor11')
plot(range(int32(Days / dt)), sensor12, label='Sensor12')
plot(range(int32(Days / dt)), sensor13, label='Sensor13')
plot(range(int32(Days / dt)), sensor14, label='Sensor14')
plot(range(int32(Days / dt)), sensor15, label='Sensor15')
plot(range(int32(Days / dt)), sensor16, label='Sensor16')
title("Evolución de temperatura")
legend()
savefig("Caso_1.png", dpi=320)
show()

