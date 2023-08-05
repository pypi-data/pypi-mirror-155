import matplotlib
import numpy as np
import matplotlib.pyplot as plt

sin = np.sin
cos = np.cos
pi = np.pi

def Q(f):
    return [{'matrix': np.array([[1,0], [-1/f,1]]), 'length': 0}]

# The quadrupole as a sequence of a single tuple
Q3 = lambda f: [{'matrix': np.array([[1, 0, 0],[-1/f, 1,0],[0,0,1]]), 'length':0 }]

# The quadrupole as a sequence of a single tuple
Q5 = lambda f: [{'matrix': np.array([[1, 0, 0, 0, 0],[-1/f, 1, 0, 0, 0],[0, 0, 1, 0, 0],[0, 0, 1/f, 1,0], [0, 0, 0, 0,1]]), 'length': 0}]

def Qthick3(k1, l):
    '''Returns a thick quadrupole element (3x3 case)'''
    if k1>0:
        matrix = np.array([[np.cos(np.sqrt(k1)*l), 1/np.sqrt(k1)*np.sin(np.sqrt(k1)*l), 0],\
                         [-np.sqrt(k1)*np.sin(np.sqrt(k1)*l), np.cos(np.sqrt(k1)*l), 0],\
                        [0,0,1]])
    else:
        k1 = -k1;
        matrix = np.array([[np.cosh(np.sqrt(k1)*l), 1/np.sqrt(k1)*np.sinh(np.sqrt(k1)*l), 0],\
                         [np.sqrt(k1)*np.sinh(np.sqrt(k1)*l), np.cosh(np.sqrt(k1)*l), 0],\
                        [0,0,1]])
    return [{'matrix': matrix, 'length': l}]
    
def Qthick5(k1, l):
    '''Returns a thick quadrupole element (5x5 case)'''
    if k1>0:
        matrix = np.array([[np.cos(np.sqrt(k1)*l), 1/np.sqrt(k1)*np.sin(np.sqrt(k1)*l), 0],\
                         [-np.sqrt(k1)*np.sin(np.sqrt(k1)*l), np.cos(np.sqrt(k1)*l), 0],\
                        [np.cosh(np.sqrt(k1)*l), 1/np.sqrt(k1)*np.sinh(np.sqrt(k1)*l), 0],\
                         [np.sqrt(k1)*np.sinh(np.sqrt(k1)*l), np.cosh(np.sqrt(k1)*l), 0],\
                        [0,0,1]])
    else:
        k1 = -k1;
        matrix = np.array([[np.cosh(np.sqrt(k1)*l), 1/np.sqrt(k1)*np.sinh(np.sqrt(k1)*l), 0],\
                         [np.sqrt(k1)*np.sinh(np.sqrt(k1)*l), np.cosh(np.sqrt(k1)*l), 0],\
                        [np.cos(np.sqrt(k1)*l), 1/np.sqrt(k1)*np.sin(np.sqrt(k1)*l), 0],\
                         [-np.sqrt(k1)*np.sin(np.sqrt(k1)*l), np.cos(np.sqrt(k1)*l), 0],\
                        [0,0,1]])
    return [{'matrix': matrix, 'length': l}]

# The drift as a sequence of a single tuple 2D
def D(L):
    return [{'matrix': np.array([[1,L], [0,1]]), 'length': L}]
    
# The drift as a sequence of a single tuple 3D
D3 = lambda L: [{'matrix': np.array([[1, L, 0],[0, 1, 0], [0, 0, 1]]), 'length':L}]

# The drift as a sequence of a single tuple 4D
D4 = lambda L: [{'matrix': np.array([[1, L, 0, 0],[0, 1, 0, 0], [0, 0, 1, L], [0, 0, 0, 1]]), 'length': L}]
# The drift as a sequence of a single tuple 5D
D5 = lambda L: [{'matrix': np.array([[1, L, 0, 0,0],[0, 1, 0, 0,0], [0, 0, 1, L,0], [0, 0, 0, 1,0], [0, 0, 0, 0,1]]), 'length': L}]


#Sector banding magnets
B3 = lambda phi, l: [{'matrix': np.array([[cos(phi),l/phi*sin(phi), l/phi*(1-cos(phi))],\
                              [-sin(phi)/l*phi, cos(phi), sin(phi)],
                             [0,0,1]]), 'length': l}]
B4 = lambda phi, l: [{'matrix': np.array([[cos(phi),l/phi*sin(phi), 0, 0],\
                               [-sin(phi)/l*phi, cos(phi), 0, 0],\
                               [0, 0, 1, l],
                               [0, 0, 0, 1]]),'length': l}]
B5 = lambda phi, l: [{'matrix': np.array([[cos(phi),l/phi*sin(phi), 0, 0, l/phi*(1-cos(phi))],\
                               [-sin(phi)/l*phi, cos(phi), 0, 0, sin(phi)],\
                               [0, 0, 1, l, 0],
                               [0, 0, 0, 1 , 0], [0, 0, 0, 0, 1]]),'length': l}]

def lattice(beamline):
    M = np.eye(beamline[0]['matrix'].shape[0])
    L = 0
    for elements in beamline[-1::-1]:
        M = M @ elements['matrix']
        L = L + elements['length']
    return [{'matrix': M, 'length':L}]

def twiss(beamline):
    '''Returns the Q, and the Twiss parameters beta, alpha, gamma of the beamline'''
    # 2x2 case
    OTM = lattice(beamline)
    R = OTM[0]['matrix']
    
    if np.shape(R)[0]<4:
        mu = np.arccos(0.5*(R[0,0]+R[1,1]))
        if (R[0,1]<0):
            mu = 2*np.pi-mu;
        Q = mu/(2*np.pi)
        beta = R[0,1]/np.sin(mu)
        alpha = (0.5*(R[0,0]-R[1,1]))/np.sin(mu)
        gamma = (1+alpha**2)/beta
        return Q, beta, alpha, gamma

    
    # 4x4 case, we assume uncoupled motion!!!
    if np.shape(R)[0]>=4:
        Rx = R[:2,:2]
        mux = np.arccos(0.5*(Rx[0,0]+Rx[1,1]))
        if (Rx[0,1]<0):
            mux = 2*np.pi-mux;
        Qx = mux/(2*np.pi)
        betax = Rx[0,1]/np.sin(mux)
        alphax = (0.5*(Rx[0,0]-Rx[1,1]))/np.sin(mux)
        gammax = (1+alphax**2)/betax
        
        Ry = R[2:,2:]
        muy = np.arccos(0.5*(Ry[0,0]+Ry[1,1]))
        if (Ry[0,1]<0):
            muy = 2*np.pi-muy;
        Qy = muy/(2*np.pi)
        betay = Ry[0,1]/np.sin(muy)
        alphay = (0.5*(Ry[0,0]-Ry[1,1]))/np.sin(muy)
        gammay = (1+alphay**2)/betay
        
        return (Qx, betax, alphax, gammax, Qy, betay, alphay, gammay)

def transportSigma2(sigma, beamline):
    coords = [sigma]
    s = [0]
    for elements in beamline:
        sigmaN = elements['matrix'] @ coords[-1] @ elements['matrix'].transpose()
        coords.append(sigmaN)
        s.append(s[-1]+elements['length'])
    coords = np.array(coords).transpose()
    return { 'sigma11': coords[0][0],
            'sigma22': coords[1][1],
            'sigma12': coords[0][1],
            'sigma21': coords[1][0],
            's' : np.array(s),
            'coords': coords,}
        
def transportSigma3(sigma, beamline):
    coords = [sigma]
    s = [0]
    for elements in beamline:
        sigmaN = elements['matrix'] @ coords[-1] @ elements['matrix'].transpose()
        coords.append(sigmaN)
        s.append(s[-1]+elements['length'])
    coords = np.array(coords).transpose()
    return { 'sigma11': coords[0][0],
            'sigma22': coords[1][1],
            'sigma12': coords[0][1],
            'sigma21': coords[1][0],
            'sigmap': coords[2][2],
            's' : np.array(s),
            'coords': coords,}

def transportSigma5(sigma, beamline):
    coords = [sigma]
    s = [0]
    for elements in beamline:
        sigmaN = elements['matrix'] @ coords[-1] @ elements['matrix'].transpose()
        coords.append(sigmaN)
        s.append(s[-1]+elements['length'])
    coords = np.array(coords).transpose()
    return { 'sigma11': coords[0][0],
            'sigma22': coords[1][1],
            'sigma12': coords[0][1],
            'sigma21': coords[1][0],
            'sigma33': coords[2][2],
            'sigma34': coords[2][3],
            'sigma44': coords[3][3],
            'sigmap': coords[4][4],
            's' : np.array(s),
            'coords': coords,}
            
def transportSigma(sigma, beamline):
    R = sigma
    if np.shape(R)[0]==2:
        return transportSigma2(sigma, beamline)
    if np.shape(R)[0]==3:
        return transportSigma3(sigma, beamline)
    if np.shape(R)[0]==5:
        return transportSigma5(sigma, beamline)

def Track(x,beamline):
    coords = [x]
    s = [0]
    for elements in (beamline):
        coords.append(elements['matrix'] @ coords[-1])
        s.append(s[-1] + elements['length'])
    coords = np.array(coords).transpose()
    return { 'x': coords[:,0,:],
             'px': coords[:,1,:],
            'y': coords[:,2,:],
             'py': coords[:,3,:],
             's' : np.array(s),
             'coords': coords,
            }

#Plot tune diagram
def Tune(order, color, von, bis):
    Qx = np.arange(von, bis+3*0.1, 0.1)
    list = np.arange(-order, order+1, 1)
    p = list
    m = list
    n = list
    for i in range(len(list)):
        for j in range(len(list)):
            for k in range(len(list)):
                if n[k] != 0 and abs(n[k]) + abs(m[j]) == order :
                    Qy = (p[i] - m[j]*Qx)*(1/n[k])
                    plt.plot(Qx, Qy, color, lw=0.35)
                    plt.plot(Qy, Qx, color, lw=0.35)


#________LINAC_Dynamics_____________________________________
from scipy import constants
import scipy.constants as sciCont
#constants
from scipy.constants import speed_of_light
from scipy.constants import e
from scipy import optimize
from scipy.optimize import fsolve
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
#muon mass in eV
m_mu = 105.65837555*1e6
#pi
pi = np.pi
#speed of light in [m/s]
c = constants.speed_of_light
#unitary charge
e = constants.e
def dpsi_n1(dpsi_n0, dW_n0, W_kin, w_RF, L):
    W = W_kin + m_mu
    beta = np.sqrt(1 - (m_mu*m_mu)/(W*W))
    gamma = W/m_mu
    return dpsi_n0 - w_RF * dW_n0 * L / (m_mu*c * (beta*gamma)**3)
def dW_n1_acc(dW_n0, RF_field, dpsi_n1, psi_stable, W_kin, w_RF, L):
    W = W_kin + m_mu
    beta = np.sqrt(1 - (m_mu*m_mu)/(W*W))
    lambda_RF = 2 * pi * c / w_RF
    T_trans = np.sin(pi*L/(beta * lambda_RF)) / (pi*L / (beta* lambda_RF))
    return dW_n0 + L * T_trans * RF_field * (np.sin(dpsi_n1) - sin(psi_stable))
def Tracker(dpsi, dW, cell_number, W_kin, w_RF, RF_field, psi_stable, L_gap, L_drift):
    W = W_kin + m_mu
    gamma = W / m_mu
    lambda_RF = 2 * pi * c / w_RF
    for j in range(0,cell_number):
        dpsi = dpsi_n1(dpsi, dW, W_kin, w_RF, L_gap)
        dW_final = dW_n1_acc(dW, RF_field, dpsi, psi_stable, W_kin, w_RF, L_gap)
        dpsi_final = dpsi_n1(dpsi, dW_final, W_kin, w_RF, L_drift)
        dpsi = dpsi_final
        dW = dW_final
        #Update W_kin____________
        W = W_kin + m_mu
        beta = np.sqrt(1 - (m_mu*m_mu)/(W*W))
        gamma = W / m_mu
        T_trans = np.sin(pi*L_gap/(beta * lambda_RF)) / (pi*L_gap / (beta* lambda_RF))
        W_kin = W_kin + T_trans*L_gap*RF_field * np.sin(psi_stable)
        #________________________
    return dpsi, dW, W_kin
def Separatrix(W_kin, RF_field, w_RF, psi_stable, L_gap, L_drift):
    sign = lambda a: 1 if a>0 else -1 if a<0 else 0
    code = 0
    #____________________
    W = W_kin + m_mu
    gamma = W / m_mu
    dpsi_i = np.linspace(np.pi - psi_stable - 0.001, np.pi - psi_stable - 0.001, 1)
    dW_i = np.linspace(0, 0, 1)
    coordinates = []
    for i in range(0, len(dpsi_i)):
        dpsis = []
        dWs = []
        dpsi = dpsi_i[i]
        dW = dW_i[i]
        dWs.append(dW ) #in MeV
        dpsis.append(dpsi)
        #________________________
        number = 100000
        for j in range(0,number):
            if j == 2:
                beginn = sign(dpsis[1] - dpsis[2])
            dpsi = dpsi_n1(dpsi, dW, W_kin, w_RF, L_gap)
            dW_final = dW_n1_acc(dW, RF_field, dpsi, psi_stable, W_kin, w_RF, L_gap)
            dpsi_final = dpsi_n1(dpsi, dW_final, W_kin, w_RF, L_drift)
            dpsis.append(dpsi_final)
            dWs.append(dW_final )
            dpsi = dpsi_final
            dW = dW_final
            if j > 2:
                if sign(dpsis[j] - dpsis[j+1]) != beginn:
                    code = code + 1
                    beginn = - beginn
            if code == 2:
                break
        dpsis.pop()
        dWs.pop()
        coordinates.append([dpsis, dWs])
    return np.array(coordinates[0])
def hamilton_phi(phi_1, phi_stab):
    if phi_stab == 0:
        return -phi_1
    else:
        def opt_phi(y):
            x = np.cos(phi_1) + phi_1*np.sin(phi_stab) - np.cos(y) - y*np.sin(phi_stab)
            return x
        phi_2 = optimize.fsolve(opt_phi, phi_stab)
        return phi_2[0]
def hamilton_dW(psi, W_kin, w_RF, V_RF, psi_stable, L_gap, L_drift):
    lambda_RF = 2 * pi * c / w_RF
    W = W_kin + m_mu
    beta = np.sqrt(1 - (m_mu*m_mu)/(W*W))
    gamma = W / m_mu
    T_trans = np.sin(pi*L_gap/(beta * lambda_RF)) / (pi*L_gap / (beta* lambda_RF))
    H1 = T_trans * V_RF * (-2*np.cos(psi_stable) + (np.pi - 2*psi_stable)*sin(psi_stable))
    fact = 2 * (L_gap/(L_gap + L_drift)) * beta**3 * gamma**2 * c * W / w_RF
    dE =  fact * ( T_trans * V_RF * (np.cos(psi) - np.cos(psi_stable) + (psi - psi_stable)*np.sin(psi_stable)) - H1 )
    return np.sqrt(abs(dE))
def hamilton_dW_mid(psi, psi_mid, W_kin, w_RF, V_RF, psi_stable, L_gap, L_drift):
    lambda_RF = 2 * pi * c / w_RF
    W = W_kin + m_mu
    beta = np.sqrt(1 - (m_mu*m_mu)/(W*W))
    gamma = W / m_mu
    T_trans = np.sin(pi*L_gap/(beta * lambda_RF)) / (pi*L_gap / (beta* lambda_RF))
    H1 = T_trans * V_RF * ( np.cos(psi) - np.cos(psi_stable) + (psi - psi_stable)*np.sin(psi_stable) )
    fact = 2 * (L_gap/(L_gap + L_drift)) * beta**3 * gamma**2 * c * W / w_RF
    dE =  fact * ( T_trans * V_RF * (np.cos(psi_mid) - np.cos(psi_stable) + (psi_mid - psi_stable)*np.sin(psi_stable)) - H1 )
    return np.sqrt(abs(dE))
def Particle_generator(sigma_psi, W_kin, w_RF, psi_stable, L_gap, L_drift, RF_field, Number):
    psi_1 = psi_stable + sigma_psi
    psi_2 = hamilton_phi(psi_1, psi_stable)
    mean_psi = (psi_1 + psi_2)*0.5
    mean_DeltaE = 0
    #matched beam
    sig_DeltaE = hamilton_dW_mid(psi_1, mean_psi, W_kin, w_RF, RF_field, psi_stable, L_gap, L_drift )
    beam = np.random.randn(2,Number)
    beam[0,:] = psi_stable + sigma_psi*beam[0,:]
    beam[1,:] = mean_DeltaE + sig_DeltaE*beam[1,:]
    return beam, mean_psi, mean_DeltaE, sig_DeltaE
def Separatrix_Sort(W_kin, RF_field, w_RF, psi_stable, L_gap, L_drift, phi_coord, dE_coord):
    x = np.array ( Separatrix(W_kin, RF_field, w_RF, psi_stable, L_gap, L_drift) )
    dphi_spx =  x[0]
    dW_spx = x[1]
    point_list = Polygon(zip( dphi_spx, dW_spx ) )
    #Sorting_algorithm__________________________________________________________________________
    SEPARATRIX = Polygon(point_list)
    points = list(zip( phi_coord, dE_coord ) )
    #___________________________________________________________________________________________
    uebrig = 0
    j = 0
    for i in range(len(points)):
        point = Point(points[i])
        if SEPARATRIX.contains(point) == True:
            uebrig = uebrig + 1
    for i in range(len(points)):
        point = Point(points[j])
        if SEPARATRIX.contains(point) == False:
            phi_coord = np.delete(phi_coord, j)
            dE_coord = np.delete(dE_coord, j)
            points.remove(points[j])
        else: j = j + 1
    return dphi_spx, dW_spx, uebrig, phi_coord, dE_coord
def long_phaspace(dpsi, dW):
    #longitudinal phase space in rad x eV
    mean_psi = np.mean(dpsi)
    mean_dW = np.mean(dW)
    var_dpsi = np.std(dpsi - mean_psi) ** 2
    var_dW = np.std(dW - mean_dW) ** 2
    sigma_dpsi_dW = np.mean((dpsi - mean_psi)*(dW - mean_dW))
    A = np.sqrt ( var_dpsi*var_dW - sigma_dpsi_dW**2 )
    return A
def long_emit_norm_eVs(dpsi, dW, w_RF):
    area = long_phaspace(dpsi, dW)
    return area / w_RF
def long_emit_norm_m(dpsi, dW, w_RF):
    area = long_phaspace(dpsi, dW)
    return area / w_RF * c / m_mu
def long_emit_norm_eVm(dpsi, dW, w_RF):
    area = long_phaspace(dpsi, dW)
    return area / w_RF * c
def acceptance(W_kin_1, RF_field, w_RF, psi_stable, L_gap, L_drift):
    x = np.array ( Separatrix(W_kin_1, RF_field, w_RF, psi_stable, L_gap, L_drift) )
    dphi_spx =  x[0]
    dW_spx = x[1]
    point_list = Polygon(zip( dphi_spx, dW_spx ) )
    emittance = point_list.area
    return emittance
#----------------------------------------------------------------------------------------#
#_____________WINDOWS____________________________________________________________________#
#---------Parameters for Windows---------------------------------------------------------#
e0 = 1.602176634e-19        #Elementary charge [C = As]
eps0 = 8.8541878128e-12     #vacuum permittivity [(As)/(Vm)]
m_e = 9.1093837015e-31      #mass of electron [kg]
c = 299792458               #Speed of light [v/s]
NA = 6.02214076e23          #Avogadro [1/mol]
E_mu = m_mu * 1e-6 #Energy of rest muon [MeV]
E_e = (m_e*c**2/e0)*10**-6  #Energy of rest electron [MeV]
r_e = e0**2/(4*np.pi*eps0*m_e*c**2)#electron radius
K = (4*np.pi*NA*r_e**2*m_e*c**2)/e0 *10**-2
#----------------------------------------------------------------------------------------#
#Beryllium
#material densities in g/cm**3
rho_Be = 1.848      # Beryllium
#mean ionization energy in MeV
I_Be = 63.7e-6      #Beryllium
#Relation between Z and A
j_Be = 0.44
#Charge number of atoms
Z_Be = 4
#Mass number of atoms
A_Be = 9.0121831
#Radiation length in cm
L_Be = 35.28        #Beryllium
#specific heat capcity in J/( kg K )
c_Be = 1825.4448
def Be(Ekin): #enter kinetic energy in eV
    E_kin = Ekin * 1e-6
    x = Ekin+E_mu #Total energy
    beta = np.sqrt(1-(E_mu**2/x**2))    #Lorentz beta
    gamma = 1/np.sqrt(1-beta**2)        #Lorentz gamma
    D_Be = np.log((4*E_e**2*beta**4*gamma**4)/((1+2*gamma*(E_e/E_mu)+(E_e/E_mu)**2)*I_Be**2))
    y_Be = K/(beta**2)*j_Be*(0.5*D_Be-beta**2) * rho_Be #Energy loss [MeV/cm]
    return y_Be #Energy loss [MeV/cm]
#----------------------------------------------------------------------------------------#
def Deposition(Func, E_init, thickness, step):
    #energy deposition of a single muon
    #Func is Be(E_init), E_init in eV, thickness in cm!
    E_init = E_init * 1e-6
    thickness = thickness * 1e2
    step = step * 1e2 #
    depos = []
    window_L = np.arange(0, thickness + step, step)
    for i in range(0, len(window_L)):
       if E_init > 0:
            loss = Func(E_init) * step
            E_init = E_init - loss
            depos.append(loss * 1e6) # save deposited energy in [eV]
       else: depos.append(0)
    return np.array(depos)
