import random
import matplotlib.pyplot as plt

def russian_roulette(num_players=3, epochs=1000):
    """
    Simule une roulette russe où les joueurs continuent à tirer tant qu'il reste des chambres.
    :param num_players: Nombre de joueurs (par défaut 3).
    :param epochs: Nombre d'itérations (par défaut 1000).
    :return: Dictionnaire des résultats par joueur.
    """
    results = {f"Player {i+1}": 0 for i in range(num_players)}
    
    for _ in range(epochs):
        # Préparation d'une nouvelle partie
        chamber = [0] * 5 + [1]  # 5 chambres vides et 1 balle
        random.shuffle(chamber)  # Mélange des chambres
        
        player_index = 0
        while chamber:  # Tant qu'il reste des chambres
            shot = chamber.pop(0)  # Le joueur tire
            if shot == 1:  # Si la balle est tirée
                results[f"Player {player_index+1}"] += 1  # Comptabilise pour ce joueur
            player_index = (player_index + 1) % num_players  # Passer au joueur suivant
    
    # Calcul des statistiques (morts et survie)
    stats = {}
    total_shots = epochs * 6  # Chaque partie utilise 6 tirs (6 chambres)
    for player, deaths in results.items():
        survival_rate = (epochs - deaths) / epochs * 100
        death_rate = deaths / epochs * 100
        stats[player] = {
            "Deaths": deaths,
            "Death Rate (%)": round(death_rate, 2),
            "Survival Rate (%)": round(survival_rate, 2)
        }
    
    return stats

def plot_results(stats):
    """
    Affiche un graphique des résultats de la simulation.
    :param stats: Dictionnaire des résultats avec statistiques.
    """
    players = list(stats.keys())
    deaths = [stats[player]["Deaths"] for player in players]
    survival_rates = [stats[player]["Survival Rate (%)"] for player in players]
    
    # Graphique des morts
    plt.figure(figsize=(10, 5))
    plt.bar(players, deaths, color='red', alpha=0.7, label="Éliminations")
    for i, value in enumerate(deaths):
        plt.text(i, value + 1, str(value), ha='center', fontsize=10)
    plt.title("Éliminations par joueur")
    plt.xlabel("Joueurs")
    plt.ylabel("Nombre d'éliminations")
    plt.legend()
    plt.show()

    # Graphique des taux de survie
    plt.figure(figsize=(10, 5))
    plt.bar(players, survival_rates, color='green', alpha=0.7, label="Taux de survie (%)")
    for i, value in enumerate(survival_rates):
        plt.text(i, value + 1, f"{value}%", ha='center', fontsize=10)
    plt.title("Taux de survie par joueur")
    plt.xlabel("Joueurs")
    plt.ylabel("Taux de survie (%)")
    plt.legend()
    plt.show()

# Paramètres de simulation
num_players = 3
epochs = 100000

# Simulation et affichage des résultats
stats = russian_roulette(num_players=num_players, epochs=epochs)
for player, data in stats.items():
    print(f"{player} -> {data}")
plot_results(stats)
