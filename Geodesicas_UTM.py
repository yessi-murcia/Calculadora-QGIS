# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 13:50:17 2021

@author: josea
"""

import math

#Variables para ambas transformaciones

#Factor de Escala
K0 = 0.9996

#Excentricidades
E = 0.00669438
E2 = E * E
E3 = E2 * E
E_P2 = E / (1 - E)

#Segundas Excentricidades
SQRT_E = math.sqrt(1 - E)
_E = (1 - SQRT_E) / (1 + SQRT_E)
_E2 = _E * _E
_E3 = _E2 * _E
_E4 = _E3 * _E
_E5 = _E4 * _E

#Ecuaciones de la conversion a UTM
M1 = (1 - E / 4 - 3 * E2 / 64 - 5 * E3 / 256)
M2 = (3 * E / 8 + 3 * E2 / 32 + 45 * E3 / 1024)
M3 = (15 * E2 / 256 + 45 * E3 / 1024)
M4 = (35 * E3 / 3072)

#Ecuaciones de la conversion a Lat Lon
P2 = (3 / 2 * _E - 27 / 32 * _E3 + 269 / 512 * _E5)
P3 = (21 / 16 * _E2 - 55 / 32 * _E4)
P4 = (151 / 96 * _E3 - 417 / 128 * _E5)
P5 = (1097 / 512 * _E4)

#Semieje del Elipsoide (WHS84)
R = 6378137

#Bandas UTM
ZONE_LETTERS = "CDEFGHJKLMNPQRSTUVWXX"

NORTH_LETTERS = "NPQRSTUVWXX"

SOUTH_LETTERS = "CDEFGHJKLM"


def to_LatLon():
    """
    Esta funcion solicita al usuario los Inputs:
        Coordenada X > float
        Coordenada Y > float
        Numero de la Zona > int de 1 - 60
        Letra de la Banda > str 
        
    Calcula:
        Latitud > float. grados decimales
        Longitud > float. grados decimales

    Returns
    -------
    Una tupla de los valores de Latitud y Longitud
    (Latitud, Longitud)

    """
    
    easting = float(input("Ingrese la coordenada X > "))
    northing = float(input("Ingrese la coordenada Y > "))
    zone_number = int(input("Ingrese el numero de la zona > "))
    zone_letter = input("Ingrese la letra de la Zona > ").upper()
    
    if not 100000 <= easting <= 1000000:
        print('ERROR:\nLa coordenada X debe estar entre 100,000 y 999,999 metros')
        print("\nIntroduce nuevamente los valores")
        to_LatLon()
    
    if not 0 <= northing <= 10000000:
        print('ERROR:\nLa coordenada Y debe estar entre 0 y 10,000,000 metros')
        print("\nIntroduce nuevamente los valores")
        to_LatLon()
        
    if not 1 <= zone_number <= 60:
        print("ERROR:\nEl numero de la zona debe estar entre 1 y 60")
        print("\nIntroduce nuevamente los valores")
        to_LatLon()
    
    if zone_letter not in ZONE_LETTERS:
        print("ERROR:\nLa letra de la Zona debe estar entre 'C' y 'X'")
        print("Introduce nuevamente los valores")
        to_LatLon()
        
    x = easting - 500000
    
    if zone_letter in NORTH_LETTERS:
        y = northing
        
    else:
        y = northing - 10000000
        
    m = y/K0
    
    mu = m / (R * M1)
    
    p_rad = (mu +
             P2 * math.sin(2 * mu) +
             P3 * math.sin(4 * mu) +
             P4 * math.sin(6 * mu) +
             P5 * math.sin(8 * mu))
    
    p_sin = math.sin(p_rad)
    p_sin2 = p_sin * p_sin
    
    p_cos = math.cos(p_rad)
    
    p_tan = p_sin / p_cos
    p_tan2 = p_tan**2
    p_tan4 = p_tan2**2
    
    ep_sin = 1 - E * p_sin2
    ep_sin_sqrt = math.sqrt(1 - E * p_sin2)
    
    n = R / ep_sin_sqrt
    r = (1 - E) / ep_sin
    
    c = E_P2 * p_cos**2
    c2 = c * c
    
    d = x / (n * K0)
    d2 = d * d
    d3 = d2 * d
    d4 = d3 * d
    d5 = d4 * d
    d6 = d5 * d
    
    latitude = (p_rad - (p_tan / r) *
               (d2 / 2 -
                d4 / 24 * (5 + 3 * p_tan2 + 10 * c - 4 * c2 - 9 * E_P2)) +
                d6 / 720 * (61 + 90 * p_tan2 + 298 * c + 45 * p_tan4 - 252 * E_P2 - 3 * c2))
    
    cenMer = 6 * (zone_number - 1) - 177
    
    long = (d -
            d3 / 6 * (1 + 2 * p_tan2 + c) +
            d5 / 120 * (5 - 2 * c + 28 * p_tan2 - 3 * c2 + 8 * E_P2 + 24 * p_tan4)) / p_cos
    
    #longitud = check_angle(long + math.radians(cenMer))
    longitud =(((long + math.radians(cenMer)) + math.pi) % (2 * math.pi) - math.pi)
    
    latDegrees = math.degrees(latitude)
    lonDegrees = math.degrees(longitud)
    
    print(f"Latitud = {round(latDegrees,5)}")
    print(f"Longitud = {round(lonDegrees,5)}")
    
    return (latDegrees, lonDegrees)

def to_UTM():
    """
    Esta funcion solicita al usuario los Inputs:
        Latitud > float. grados decimales
        Longitud > float. grados decimales
        
    Calcula:
        El numero de la Zona > int. huso
        El meridiano central de la zona > int. cenMer
        Banda de la zona > str. zona
        Coordenada X > float
        Coordenada Y > float

    Returns
    -------
    Una tupla de los valores de X, Y, Zona, Banda, Meridiano Central)
    (X, Y, huso, zona, cenMer)

    """

    phi = float(input("Ingrese la Latitud en grados decimales > "))
    
    phiRad = math.radians(phi)
    
    lamb = float(input("Ingrese la longitud en grados decimales > "))
    
    lambRad = math.radians(lamb)
    
    #Huso
    huso = int((lamb/6) + 31)
    
    print(f"Huso = {huso}")
    
    #Meridiano central de la zona
    cenMer = 6 * (huso - 1) - 177
    print(f"Meridiano Central = {cenMer}")
    cenMer_rad = math.radians(cenMer)
    
    #Letra de Zona
    if -80 <= phi <= 84:
        zona = ZONE_LETTERS[int(phi + 80) >> 3]
        
    print(f"Zona = {zona}")
        
    cosRad= math.cos(phiRad)
    
    tanRad = math.tan(phiRad)
    
    sinRad = math.sin(phiRad)
    
    tanRad2 = tanRad**2
    
    tanRad4 = tanRad2**2
    
    #Calcula el valor de N 
    n = R / math.sqrt(1 - E * sinRad**2)
    
    c = E_P2 * cosRad**2
    
    #Ecuaciones de la proyección
    a = cosRad * (((lambRad - cenMer_rad) + math.pi) % (2 * math.pi) - math.pi)
    a2 = a * a
    a3 = a2 * a
    a4 = a3 * a
    a5 = a4 * a
    a6 = a5 * a
    
    m = R * (M1 * phiRad -
             M2 * math.sin(2 * phiRad) +
             M3 * math.sin(4 * phiRad) -
             M4 * math.sin(6 * phiRad))
    
    
    X = K0 * n * (a +
                  a3 / 6 * (1 - tanRad2 + c) +
                  a5 / 120 * (5 - 18 * tanRad2 + tanRad4 + 72 * c - 58 * E_P2)) + 500000
    
    y = K0 * (m + n * tanRad * (a2 / 2 +
              a4 / 24 * (5 - tanRad2 + 9 * c + 4 * c**2) +
              a6 / 720 * (61 - 58 * tanRad2 + tanRad4 + 600 * c - 330 * E_P2)))

    if phi >= 0:
        Y = y
    else:
        Y = 10000000 + y
        
    print(f"X = {round(X,3)}")
    
    print(f"Y = {round(Y,3)}") 
    
    return (X, Y, huso, zona, cenMer)
