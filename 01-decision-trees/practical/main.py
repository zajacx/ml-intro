import csv
import numpy as np
import matplotlib.pyplot as plt

data = []

# Wczytywanie danych
with open('drzewka-dane-1.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append({'x1': float(row['x1']), 'x2': float(row['x2']), 'y': int(row['y'])})

# Zadanie 1.: Wypisz ładnie dane

# for row in data:
#     print(f"x1: {row['x1']}\tx2: {row['x2']}\ty: {row['y']}")

x1 = []
x2 = []
y = []

for row in data:
    x1.append(row['x1'])
    x2.append(row['x2'])
    y.append(row['y'])

# matplotlib jest biblioteką do tworzenia np. ładnych wizualizacji.
# Idealnym rodzajem wykresu do przedstawienia naszych danych jest tzw. scatter plot.
# https://matplotlib.org/stable/plot_types/basic/scatter_plot.html

# Metoda plt.scatter() przyjmuje wiele argumentów, ale obowiązkowo musimy podać dwa:
# x -> lista wartości pierwszej zmiennej przyjmowanych przez wszystkie przykłady z danych
# y -> analogicznie, lista wartości drugiej zmiennej
# Opcjonalnie, jako argument 'c', można określić kolor punktów.
# Tak się składa, że każdy przykład z danych jest oznaczony przez 0 lub 1 w kolumnie y.
# Biblioteka sama dobierze kolory, a my oprócz samych punktów zobaczymy ich klasę (0/1).

# Jeżeli wszystko będzie ok, poniższy kod wyprodukuje wykres i zapisze go do pliku:
plt.xlabel('x1')
plt.ylabel('x2')
plt.scatter(x1, x2, c=y)
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.close()

# if x2<0.6 and x1<2:
#     y=0
# else:
#     if x2>0.6 and x1<2:
#         y=1
#     else: 
#         if x2>0.6 and x1>2:
#             y=0
#         else:
#             y=1

# if x1 <= 2.0:
#     if x2 <= 0.6:
#         y = 0
#     else:
#         y = 1
# else:
#     if x2 <= 0.3:
#         y = 1
#     else:
#         y = 0


def calculate_gini(y_subset):
    """
    Oblicza indeks Giniego dla podzbioru przykładów.
    Niech p_i oznacza prawdopodobieństwo przynależności punktu
    do i-tej klasy. Wtedy indeks Giniego jest równy

    1 - (p_1)^2 - (p_2)^2 - ... - (p_n)^2

    gdzie n to liczba klas.

    Argumenty:
    - y_subset: lista etykiet [0, 1, 0, 0, 1, ...]

    Zwraca:
    - indeks Giniego (float)
    """
    n = len(y_subset)
    if n == 0:
        return 0
    
    # Zadanie 3.: Zaimplementuj calculate_gini()
    # TODO {
    zeros = y_subset.count(0)
    ones = y_subset.count(1)

    p_ones = 1.0 * ones/n
    p_zeros = 1.0 * zeros/n
    
    gini = 1 - p_ones**2 - p_zeros**2
    # TODO }

    return gini


def find_best_split(x1, x2, y):
    """
    Znajduje podział danych na dwa rozłączne podzbiory,
    dla którego zysk Giniego jest największy. Definiujemy go jako:

    gini(parent) - (weight_left * gini(left) + weight_right * gini(right))

    Argumenty:
    - x1: lista wartości pierwszej cechy
    - x2: analogicznie, druga cecha
    - y: lista etykiet

    Zwraca:
    - słownik {'warunek': (cecha, prog), 'lewe': lewe_y, 'prawe': prawe_y}
    """
    best_gain = -1
    best_split = None
    n = len(y)
    current_gini = calculate_gini(y)

    # Zadanie 4.: Zaimplementuj find_best_split()
    # TODO {
    thresholds_x1 = []
    t = 0.0
    while t < 3.5:
        thresholds_x1.append(t)
        t += 0.05

    for t in thresholds_x1:
        y_left = [y[i] for i in range(n) if x1[i] <= t]
        y_right = [y[i] for i in range(n) if x1[i] > t]

        # Zabezpieczamy się na wypadek pustej listy:
        if not y_left or not y_right:
            continue

        # Obliczamy Giniego dla podziału
        gini_left = calculate_gini(y_left)
        gini_right = calculate_gini(y_right)

        # Ważony Gini:
        weighted_gini = (len(y_left)/n) * gini_left + (len(y_right)/n) * gini_right

        # Zysk Giniego:
        gain = current_gini - weighted_gini

        if gain > best_gain:
            best_gain = gain
            best_split = ('x1', t)
    
    # Analogicznie dla x2:
    thresholds_x2 = []
    t = 0.0
    while t < 1.0:
        thresholds_x2.append(t)
        t += 0.05

    for t in thresholds_x2:
        y_left = [y[i] for i in range(n) if x2[i] <= t]
        y_right = [y[i] for i in range(n) if x2[i] > t]

        if not y_left or not y_right:
            continue

        gini_left = calculate_gini(y_left)
        gini_right = calculate_gini(y_right)

        weighted_gini = (len(y_left)/n) * gini_left + (len(y_right)/n) * gini_right

        gain = current_gini - weighted_gini

        if gain > best_gain:
            best_gain = gain
            best_split = ('x2', t)
    # TODO }

    return best_split

def build_tree(x1, x2, y, depth=0):
    if not y: return {'wynik': 0}

    # Jeśli wszystkie etykiety są takie same, kończymy
    if len(set(y)) <= 1 or depth >= 3:
        return {'wynik': max(set(y), key=y.count)}

    split = find_best_split(x1, x2, y)
    if not split:
        return {'wynik': max(set(y), key=y.count)}

    feature_name, threshold = split

    # Tworzymy podzbiory list zgodnie z wybranym podziałem
    if feature_name == 'x1':
        mask = [val <= threshold for val in x1]
    else:
        mask = [val <= threshold for val in x2]

    l_x1 = [x1[i] for i in range(len(y)) if mask[i]]
    l_x2 = [x2[i] for i in range(len(y)) if mask[i]]
    l_y = [y[i] for i in range(len(y)) if mask[i]]

    p_x1 = [x1[i] for i in range(len(y)) if not mask[i]]
    p_x2 = [x2[i] for i in range(len(y)) if not mask[i]]
    p_y = [y[i] for i in range(len(y)) if not mask[i]]

    return {
        'warunek': split,
        'lewe': build_tree(l_x1, l_x2, l_y, depth + 1),
        'prawe': build_tree(p_x1, p_x2, p_y, depth + 1)
    }

tree = build_tree(x1, x2, y)

def print_tree(node, depth=0):
    indent = "  " * depth
    if 'wynik' in node:
        print(f"{indent}Decyzja: {'groźne' if node['wynik'] == 1 else 'niegroźne'}")
    else:
        cecha, prog = node['warunek']
        print(f"{indent}Czy {cecha} <= {prog}?")
        print(f"{indent}  Tak:")
        print_tree(node['lewe'], depth + 2)
        print(f"{indent}  Nie:")
        print_tree(node['prawe'], depth + 2)

print_tree(tree)

# Funkcja rekurencyjna, która "przechodzi" przez drzewo dla danego punktu
def predict(node, x1_val, x2_val):
    # Jeśli węzeł ma wynik, to go zwracamy
    if 'wynik' in node:
        return node['wynik']

    # Jeśli nie, sprawdzamy warunek (cecha, prog)
    cecha, prog = node['warunek']

    # Wybieramy wartość do porównania
    val = x1_val if cecha == 'x1' else x2_val

    if val <= prog:
        return predict(node['lewe'], x1_val, x2_val)
    else:
        return predict(node['prawe'], x1_val, x2_val)

x_range = np.linspace(min(x1) - 0.1, max(x1) + 0.1, 200)
y_range = np.linspace(min(x2) - 0.1, max(x2) + 0.1, 200)
xx, yy = np.meshgrid(x_range, y_range)
Z = np.array([predict(tree, xi, yi) for xi, yi in zip(xx.ravel(), yy.ravel())])
Z = Z.reshape(xx.shape)

plt.figure(figsize=(10, 6))
plt.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')
plt.scatter(x1, x2, c=y, edgecolors='k', cmap='coolwarm')

plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Granice decyzyjne wyuczonego drzewa')
plt.savefig('plot_with_contours.png', dpi=300, bbox_inches='tight')
plt.close()