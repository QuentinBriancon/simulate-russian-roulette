import random
import matplotlib.pyplot as plt
from collections import defaultdict

class Player:
    def __init__(self, name):
        self.name = name
        self.deaths = 0
        self.death_turns = defaultdict(int)
        self.total_time = 0
        self.nervosity = random.uniform(0.5, 1.0)  # Valeur de nervosité de départ
        self.time_taken = 0
    
    def reset(self):
        # Réinitialiser les valeurs du joueur pour chaque époque
        self.deaths = 0
        self.death_turns.clear()
        self.total_time = 0
        self.time_taken = 0
        self.nervosity = random.uniform(0.5, 1.0)  # Réinitialiser la nervosité

    def take_turn(self, chamber, turn):
        # Calculer le temps de tir basé sur la nervosité du joueur
        time_taken = random.uniform(0.5, 1.5) * self.nervosity  # Temps de tir ajusté par nervosité
        self.time_taken += time_taken  # Ajouter le temps au total de ce joueur
        
        shot = chamber.pop(0)  # Le joueur tire
        if shot == 1:  # Si la balle est tirée, le joueur meurt
            self.deaths += 1
            self.death_turns[turn] += 1  # Enregistrer le tour de la mort
            return True  # Le joueur est mort, retourne True
        else:
            self.nervosity += 0.05  # Augmenter la nervosité après chaque tir
        return False  # Le joueur survit

    def get_stats(self, epochs):
        survival_rate = (epochs - self.deaths) / epochs * 100
        death_rate = self.deaths / epochs * 100
        avg_time = self.time_taken / (epochs - self.deaths) if epochs - self.deaths > 0 else 0  # Eviter la division par zéro
        avg_nervosity = self.nervosity / (epochs - self.deaths) if epochs - self.deaths > 0 else 0  # Moyenne de nervosité accumulée
        return {
            "Deaths": self.deaths,
            "Death Rate (%)": round(death_rate, 2),
            "Survival Rate (%)": round(survival_rate, 2),
            "Average Time per Survival (s)": round(avg_time, 2),
            "Average Nervosity": round(avg_nervosity, 2)
        }

def russian_roulette(num_players=3, epochs=100, max_chamber=6, games_per_epoch=100):
    """
    Simule plusieurs parties de roulette russe en même temps, avec accumulation du stress sur plusieurs époques.
    :param num_players: Nombre de joueurs par partie (par défaut 3).
    :param epochs: Nombre d'époques à simuler (par défaut 100).
    :param max_chamber: Nombre de chambres (par défaut 6, 1 balle et 5 vides).
    :param games_per_epoch: Nombre de parties simultanées par époque (par défaut 100).
    :return: Dictionnaire des résultats avec statistiques.
    """
    players = [Player(f"Player {i+1}") for i in range(num_players)]

    # Pour chaque époque, jouer plusieurs parties simultanément
    for epoch in range(epochs):
        # Réinitialisation des joueurs à chaque époque
        for player in players:
            player.reset()

        for game in range(games_per_epoch):
            # Préparer la chambre pour chaque partie (1 balle + chambres vides)
            chamber = [0] * (max_chamber - 1) + [1]
            random.shuffle(chamber)  # Mélange des chambres

            turn = 1
            current_players = players.copy()  # Liste des joueurs pour chaque partie
            while chamber:  # Tant qu'il reste des chambres
                if not current_players:  # Si tous les joueurs sont morts, la partie est terminée
                    break

                player_index = len(chamber) % len(current_players)  # Rotation des joueurs
                player = current_players[player_index]

                # Le joueur prend son tour
                if player.take_turn(chamber, turn):
                    # Remplacer le joueur qui est mort par un nouveau joueur
                    current_players[player_index] = Player(f"Player {len(players)+1}")
                    break  # La partie s'arrête si un joueur meurt

                turn += 1  # Passer au tour suivant

            # Ajouter du stress aux joueurs survivants après chaque partie
            for player in current_players:
                if player.deaths == 0:  # Si le joueur n'est pas mort
                    player.nervosity += 0.1  # Ajouter du stress

    # Calcul des statistiques sur les résultats
    stats = {}
    for player in players:
        stats[player.name] = player.get_stats(epochs)
    
    return stats

def plot_results(stats):
    """
    Affiche les graphiques des résultats de la simulation.
    :param stats: Dictionnaire des résultats avec statistiques.
    """
    players = list(stats.keys())
    survival_rates = [stats[player]["Survival Rate (%)"] for player in players]
    avg_times = [stats[player]["Average Time per Survival (s)"] for player in players]
    avg_nervosity = [stats[player]["Average Nervosity"] for player in players]
    
    # Configuration des sous-graphiques
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Graphique des taux de survie
    axes[0].bar(players, survival_rates, color='green', alpha=0.7, label="Taux de survie (%)")
    for i, value in enumerate(survival_rates):
        axes[0].text(i, value + 1, f"{value}%", ha='center', fontsize=10)
    axes[0].set_title("Taux de survie par joueur")
    axes[0].set_xlabel("Joueurs")
    axes[0].set_ylabel("Taux de survie (%)")

    # Graphique du temps moyen de survie
    axes[1].bar(players, avg_times, color='blue', alpha=0.7, label="Temps moyen de survie (s)")
    for i, value in enumerate(avg_times):
        axes[1].text(i, value + 0.1, f"{value}s", ha='center', fontsize=10)
    axes[1].set_title("Temps moyen par survie")
    axes[1].set_xlabel("Joueurs")
    axes[1].set_ylabel("Temps (s)")

    # Graphique de la nervosité moyenne
    axes[2].bar(players, avg_nervosity, color='red', alpha=0.7, label="Nervosité moyenne")
    for i, value in enumerate(avg_nervosity):
        axes[2].text(i, value + 0.05, f"{value:.2f}", ha='center', fontsize=10)
    axes[2].set_title("Nervosité moyenne")
    axes[2].set_xlabel("Joueurs")
    axes[2].set_ylabel("Nervosité")

    plt.tight_layout()
    plt.show()

# Paramètres de simulation
num_players = 3
epochs = 100
games_per_epoch = 100

# Simulation et affichage des résultats
stats = russian_roulette(num_players=num_players, epochs=epochs, games_per_epoch=games_per_epoch)
for player, data in stats.items():
    print(f"{player} -> {data}")
plot_results(stats)
