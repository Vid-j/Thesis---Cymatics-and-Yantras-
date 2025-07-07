import numpy as np
import matplotlib.pyplot as plt

def chladni(x, y, n=2, m=3, A=1, B=1):
    return np.sin(n * np.pi * x) * np.sin(m * np.pi * y) + A * np.sin(m * np.pi * x) * np.sin(n * np.pi * y)

# Generate grid
res = 512
x = np.linspace(0, 1, res)
y = np.linspace(0, 1, res)
X, Y = np.meshgrid(x, y)

# Calculate pattern
Z = chladni(X, Y)

# Normalize and plot
plt.imshow(Z, cmap='gray', interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
plt.savefig('chladni_texture.png', dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()
