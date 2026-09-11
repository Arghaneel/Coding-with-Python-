import numpy as np
import matplotlib.pyplot as plt
x=np.arange(-10,10,0.001)
y1=np.sin(x)
y2=np.cos(x)
plt.plot(x,y1,x,y2)
plt.title("SINE AND COS CURVES")
plt.xlabel("VALUES OF x")
plt.ylabel("VALUES OF sin(x) AND cos(x)")
plt.grid()
plt.show()