import sympy as sp

# Definicja zmiennych
x1, x2, x3, lambda1, lambda2 = sp.symbols('x1 x2 x3 lambda1 lambda2')

# Funkcja celu
f = x1**2 + 2*x2**2 + 3*x3**2

# Ograniczenia
h1 = x1 + x2 + x3 - 2
h2 = x1 - x2 + 2*x3 - 3

# Funkcja Lagrange'a
L = f - lambda1 * h1 - lambda2 * h2

# Pochodne cząstkowe
dL_dx1 = sp.diff(L, x1)
dL_dx2 = sp.diff(L, x2)
dL_dx3 = sp.diff(L, x3)
dL_dlambda1 = sp.diff(L, lambda1)
dL_dlambda2 = sp.diff(L, lambda2)

# Rozwiązanie układu równań
solution = sp.solve([
    dL_dx1, 
    dL_dx2, 
    dL_dx3, 
    dL_dlambda1, 
    dL_dlambda2
], (x1, x2, x3, lambda1, lambda2))

# Wyświetlenie rozwiązania
print("Znalezione rozwiązanie:")
print(f"x1 = {solution[x1]}")
print(f"x2 = {solution[x2]}")
print(f"x3 = {solution[x3]}")
print(f"lambda1 = {solution[lambda1]}")
print(f"lambda2 = {solution[lambda2]}")

# Obliczenie wartości funkcji celu w punkcie optymalnym
optimal_value = f.subs({
    x1: solution[x1],
    x2: solution[x2],
    x3: solution[x3]
})

print("\nMinimalna wartość funkcji celu:")
print(f"f(x1, x2, x3) = {optimal_value}")
print(f"Uproszczona postać: {sp.simplify(optimal_value)}")