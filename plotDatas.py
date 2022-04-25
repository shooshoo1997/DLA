import matplotlib.pyplot as plt
import numpy as np

step_11 = np.array([10, 50, 100, 300, 500])
moy_11 = np.array([2.8,4.14,4.19,4.19,4.19])
std_11 = np.array([1.46,1.57,1.55,1.56,1.56])

step_31 = np.array([10, 50, 100, 300, 500, 700, 900])
moy_31 = np.array([2.8,6.26,8.61,11.46,11.81,11.85,11.85])
std_31 = np.array([1.47, 3.24, 4.15, 4.65, 4.41, 4.42, 4.42])

step_51 = np.array([10, 100, 300, 500, 700, 900, 1100, 1300, 1500])
moy_51 = np.array([2.8,8.86,14.73,17.22,18.55,19.02,19.25,19.4,19.45])
std_51 = np.array([1.47,4.61,6.99,7.36,7.33,7.3,7.27,7.28,7.25])

step_71 = np.array([10, 100, 300, 500, 700, 900, 1100, 1300, 1500, 1700, 2000])
moy_71 = np.array([2.79,8.84,15.3,19.33,21.92,23.71,24.83,25.64,26.1,26.42,26.73])
std_71 = np.array([1.46,4.61,7.9,9.39,10,10.18,10.25,10.21,10.2,10.19,10.12])

step_101 = np.array([100, 300, 500, 700, 900, 1100, 1300, 1500, 1700, 2000, 2300, 2500, 2700, 2900, 3100])
moy_101 = np.array([8.91,15.36,19.87,23.27,26.93,28.38,30.3,31.77,33.05,34.54,35.53,36.11,36.51,36.91,37.2])
std_101 = np.array([4.63,8.02,10.36,11.86,12.93,13.61,14.09,14.34,14.44,14.53,14.58,14.56,14.55,14.54,14.55])

x = np.linspace(0, 3000, 3000)
sig = np.sqrt(x/2)
moy_theo = sig*np.sqrt(np.pi/2)
sigm_theo = np.sqrt(((4 - np.pi)/2) * sig**2)

plt.figure(1)
plt.plot(step_11, moy_11, 'o-', color='green', label='L = 11')
plt.plot(step_31, moy_31, 'o-', color='blue', label='L = 31')
plt.plot(step_51, moy_51, 'o-', color='red', label='L = 51')
plt.plot(step_71, moy_71, 'o-', color='black', label='L = 71')
plt.plot(step_101, moy_101, 'o-', color='orange', label='L = 101')
plt.plot(x, moy_theo, color='purple', label='Théorie')
plt.xlabel('Number of steps')
plt.ylabel('Average of displacement distribution')
plt.legend()
plt.show()

plt.figure(2)
plt.plot(step_11, std_11, 'o-', color='green', label='L = 11')
plt.plot(step_31, std_31, 'o-', color='blue', label='L = 31')
plt.plot(step_51,  std_51, 'o-', color='red', label='L = 51')
plt.plot(step_71,  std_71, 'o-', color='black', label='L = 71')
plt.plot(step_101,  std_101, 'o-', color='orange', label='L = 101')
plt.plot(x, sigm_theo, color='purple', label='Théorie')
plt.xlabel('Number of steps')
plt.ylabel('STD of displacement distribution')
plt.legend()
plt.show()