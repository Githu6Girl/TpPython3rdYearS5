import math

def quantite_information(probabilite):
    """Calcule I(x) = -log2(P(x))"""
    if probabilite == 0:
        return float('inf')
    return -math.log2(probabilite)

def entropie(probabilites):
    """Calcule H(X) = -Σ P(xi) * log2(P(xi))"""
    h = 0
    for p in probabilites:
        if p > 0:
            h -= p * math.log2(p)
    return h

# ===== EXEMPLES D'UTILISATION =====

# Exemple 1: Pile ou Face équilibré
print("Exemple 1: Pile ou Face")
probs1 = [0.5, 0.5]
print(f"Probabilités: {probs1}")
print(f"Entropie: {entropie(probs1):.4f} bits\n")

# Exemple 2: Dé à 6 faces
print("Exemple 2: Dé à 6 faces")
probs2 = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]
print(f"Probabilités: {[round(p, 3) for p in probs2]}")
print(f"Entropie: {entropie(probs2):.4f} bits\n")

# Exemple 3: Source non équilibrée
print("Exemple 3: Source non équilibrée")
probs3 = [0.8, 0.2]
print(f"Probabilités: {probs3}")
print(f"Quantité info symbole 1: {quantite_information(0.8):.4f} bits")
print(f"Quantité info symbole 2: {quantite_information(0.2):.4f} bits")
print(f"Entropie: {entropie(probs3):.4f} bits\n")

# Exemple 4: À partir de données
print("Exemple 4: Calculer à partir de données")
donnees = "AAABBC"
total = len(donnees)
compte = {}
for symbole in donnees:
    compte[symbole] = compte.get(symbole, 0) + 1

probs4 = [count/total for count in compte.values()]
print(f"Données: {donnees}")
print(f"Probabilités: {[round(p, 3) for p in probs4]}")
print(f"Entropie: {entropie(probs4):.4f} bits")

