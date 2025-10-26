import math

def entropie(probabilites):
    """Calcule H(X) = -Σ P(xi) * log2(P(xi))"""
    h = 0
    for p in probabilites:
        if p > 0:
            h -= p * math.log2(p)
    return h

def entropie_conjointe(probs_conjointes):
    """
    Calcule H(X,Y) = -Σ Σ P(xi,yj) * log2(P(xi,yj))
    
    probs_conjointes: matrice des probabilités conjointes P(X,Y)
    """
    h = 0
    for ligne in probs_conjointes:
        for p in ligne:
            if p > 0:
                h -= p * math.log2(p)
    return h

def entropie_conditionnelle(probs_conjointes, probs_y):
    """
    Calcule H(X|Y) = H(X,Y) - H(Y)
    
    probs_conjointes: matrice P(X,Y)
    probs_y: probabilités marginales de Y
    """
    h_xy = entropie_conjointe(probs_conjointes)
    h_y = entropie(probs_y)
    return h_xy - h_y

def information_mutuelle(probs_conjointes, probs_x, probs_y):
    """
    Calcule I(X;Y) = H(X) + H(Y) - H(X,Y)
    
    probs_conjointes: matrice P(X,Y)
    probs_x: probabilités marginales de X
    probs_y: probabilités marginales de Y
  """
    h_x = entropie(probs_x)
    h_y = entropie(probs_y)
    h_xy = entropie_conjointe(probs_conjointes)
    return h_x + h_y - h_xy

def calculer_marginales(probs_conjointes):
    """
    Calcule les probabilités marginales à partir de la matrice conjointe
    
    Returns: (probs_x, probs_y)
    """
    # P(X) = Σ_y P(X,Y)
    probs_x = [sum(ligne) for ligne in probs_conjointes]
    
    # P(Y) = Σ_x P(X,Y)
    n_cols = len(probs_conjointes[0])
    probs_y = [sum(probs_conjointes[i][j] for i in range(len(probs_conjointes))) 
               for j in range(n_cols)]
    
    return probs_x, probs_y

def afficher_matrice(matrice, titre="Matrice"):
    """Affiche une matrice de manière formatée"""
    print(f"\n{titre}:")
    for ligne in matrice:
        print("  ", [f"{p:.3f}" for p in ligne])

def analyser_sources(probs_conjointes):
    """Analyse complète de deux sources"""
    print("="*60)
    print("ANALYSE DE DEUX SOURCES")
    print("="*60)
    
    # Afficher la matrice conjointe
    afficher_matrice(probs_conjointes, "Probabilités Conjointes P(X,Y)")
    
    # Calculer les marginales
    probs_x, probs_y = calculer_marginales(probs_conjointes)
    print(f"\nProbabilités marginales X: {[f'{p:.3f}' for p in probs_x]}")
    print(f"Probabilités marginales Y: {[f'{p:.3f}' for p in probs_y]}")
    
    # Calculer les entropies
    h_x = entropie(probs_x)
    h_y = entropie(probs_y)
    h_xy = entropie_conjointe(probs_conjointes)
    h_x_given_y = entropie_conditionnelle(probs_conjointes, probs_y)
    h_y_given_x = entropie_conditionnelle(probs_conjointes, probs_x)
    i_xy = information_mutuelle(probs_conjointes, probs_x, probs_y)
    
    print("\n" + "-"*60)
    print("RÉSULTATS:")
    print("-"*60)
    print(f"H(X)         = {h_x:.4f} bits    (Entropie de X)")
    print(f"H(Y)         = {h_y:.4f} bits    (Entropie de Y)")
    print(f"H(X,Y)       = {h_xy:.4f} bits    (Entropie conjointe)")
    print(f"H(X|Y)       = {h_x_given_y:.4f} bits    (Entropie conditionnelle de X sachant Y)")
    print(f"H(Y|X)       = {h_y_given_x:.4f} bits    (Entropie conditionnelle de Y sachant X)")
    print(f"I(X;Y)       = {i_xy:.4f} bits    (Information mutuelle)")
    
    # Vérifications
    print("\n" + "-"*60)
    print("VÉRIFICATIONS:")
    print("-"*60)
    print(f"H(X,Y) = H(X) + H(Y|X) : {h_xy:.4f} = {h_x + h_y_given_x:.4f} ✓")
    print(f"H(X,Y) = H(Y) + H(X|Y) : {h_xy:.4f} = {h_y + h_x_given_y:.4f} ✓")
    print(f"I(X;Y) = H(X) - H(X|Y) : {i_xy:.4f} = {h_x - h_x_given_y:.4f} ✓")
    print("="*60 + "\n")


# ===== EXEMPLES D'UTILISATION =====

# Exemple 1: Sources indépendantes
print("\n### EXEMPLE 1: Sources INDÉPENDANTES ###")
# Si X et Y sont indépendants: P(X,Y) = P(X)*P(Y)
probs1 = [
    [0.25, 0.25],  # P(X=0,Y=0)=0.25, P(X=0,Y=1)=0.25
    [0.25, 0.25]   # P(X=1,Y=0)=0.25, P(X=1,Y=1)=0.25
]
analyser_sources(probs1)

# Exemple 2: Sources totalement dépendantes
print("\n### EXEMPLE 2: Sources TOTALEMENT DÉPENDANTES ###")
# Y = X (information mutuelle maximale)
probs2 = [
    [0.5, 0.0],   # Si X=0 alors Y=0
    [0.0, 0.5]    # Si X=1 alors Y=1
]
analyser_sources(probs2)

# Exemple 3: Sources partiellement dépendantes
print("\n### EXEMPLE 3: Sources PARTIELLEMENT DÉPENDANTES ###")
probs3 = [
    [0.4, 0.1],   # X=0 favorise Y=0
    [0.1, 0.4]    # X=1 favorise Y=1
]
analyser_sources(probs3)

# Exemple 4: Source 3x3
print("\n### EXEMPLE 4: Sources avec 3 valeurs chacune ###")
probs4 = [
    [0.2, 0.1, 0.0],
    [0.1, 0.3, 0.1],
    [0.0, 0.1, 0.2]
]
analyser_sources(probs4)

