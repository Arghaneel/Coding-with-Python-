import numpy as np
def radius_tangent_angle(a,t):
    r=a*(1-np.cos(t))
    x=r*np.cos(t)
    y=r*np.sin(t)
    dr_dt = -a*np.sin(t)
    Tx = dr_dt*np.cos(t)-r*np.sin(t)
    Ty=dr_dt*np.sin(t)+r*np.cos(t)
    dot_product = x*Tx + y*Ty
    r_magnitude=np.sqrt(x**2+y**2)
    T_magnitude=np.sqrt(Tx**2+Ty**2)
    cos_theta =dot_product/(r_magnitude*T_magnitude)
    theta_rad=np.arccos(cos_theta)
    theta_deg=np.degrees(theta_rad)
    return theta_deg

a=4
t=np.pi/2
angle=radius_tangent_angle(a,t)
print(f"THE ANGLE AT t = {t:.3f} ,IS {angle:.2f} degrees")
