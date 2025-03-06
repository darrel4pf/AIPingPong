import pygame
from pingpong.game import PongMatch
import neat
import os
import pickle


class AIPongTrainer:
    """
    A class to manage the training and evaluation of AI agents for the Pong game.
    """

    def __init__(self, window, width, height):
        """
        Initialize the Pong game environment for AI training.

        :param window: The Pygame window surface.
        :param width: The width of the game window.
        :param height: The height of the game window.
        """
        self.match = PongMatch(window, width, height)
        self.left_player = self.match.left_player
        self.right_player = self.match.right_player
        self.ball = self.match.ball

    def evaluate_ai(self, genome, config):
        """
        Evaluate the performance of a single AI genome by playing a game.

        :param genome: The NEAT genome to evaluate.
        :param config: The NEAT configuration object.
        """
        neural_net = neat.nn.FeedForwardNetwork.create(genome, config)

        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            # Handle player input for the left paddle
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.match.move_player(left=True, up=True)
            if keys[pygame.K_s]:
                self.match.move_player(left=True, up=False)

            # Get the AI's decision based on the current game state
            output = neural_net.activate(
                (self.right_player.y, self.ball.y, abs(self.right_player.x - self.ball.x)))
            decision = output.index(max(output))

            # Move the right paddle based on the AI's decision
            if decision == 0:
                pass  # No movement
            elif decision == 1:
                self.match.move_player(left=False, up=True)
            else:
                self.match.move_player(left=False, up=False)

            # Update the game state and render the game
            match_info = self.match.update()
            self.match.render(draw_score=True, draw_hits=False)
            pygame.display.update()

        pygame.quit()

    def train_ai_models(self, genome1, genome2, config):
        """
        Train two AI genomes by having them compete against each other.

        :param genome1: The first NEAT genome.
        :param genome2: The second NEAT genome.
        :param config: The NEAT configuration object.
        """
        neural_net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        neural_net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # Get the decision for the left paddle (controlled by neural_net1)
            output1 = neural_net1.activate(
                (self.left_player.y, self.ball.y, abs(self.left_player.x - self.ball.x)))
            decision1 = output1.index(max(output1))

            if decision1 == 0:
                pass  # No movement
            elif decision1 == 1:
                self.match.move_player(left=True, up=True)
            else:
                self.match.move_player(left=True, up=False)

            # Get the decision for the right paddle (controlled by neural_net2)
            output2 = neural_net2.activate(
                (self.right_player.y, self.ball.y, abs(self.right_player.x - self.ball.x)))
            decision2 = output2.index(max(output2))

            if decision2 == 0:
                pass  # No movement
            elif decision2 == 1:
                self.match.move_player(left=False, up=True)
            else:
                self.match.move_player(left=False, up=False)

            # Update the game state
            match_info = self.match.update()

            # Render the game without the score but with hit counts
            self.match.render(draw_score=False, draw_hits=True)
            pygame.display.update()

            # End the game if a score condition is met
            if match_info.left_score >= 1 or match_info.right_score >= 1 or match_info.left_hits > 50:
                self.update_fitness(genome1, genome2, match_info)
                break

    def update_fitness(self, genome1, genome2, match_info):
        """
        Update the fitness scores of the genomes based on their performance.

        :param genome1: The first NEAT genome.
        :param genome2: The second NEAT genome.
        :param match_info: The game information containing scores and hits.
        """
        genome1.fitness += match_info.left_hits
        genome2.fitness += match_info.right_hits


def evaluate_population(genomes, config):
    """
    Evaluate the entire population of genomes by having them compete against each other.

    :param genomes: A list of genomes to evaluate.
    :param config: The NEAT configuration object.
    """
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            trainer = AIPongTrainer(window, width, height)
            trainer.train_ai_models(genome1, genome2, config)


def start_neat_training(config):
    """
    Start the NEAT training process.

    :param config: The NEAT configuration object.
    """
    # Uncomment the following line to restore from a checkpoint
    # population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-7')
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(1))

    # Run the NEAT algorithm for a specified number of generations
    champion = population.run(evaluate_population, 50)
    with open("top.pickle", "wb") as f:
        pickle.dump(champion, f)


def evaluate_champion(config):
    """
    Evaluate the best-performing genome (champion) by playing a game.

    :param config: The NEAT configuration object.
    """
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))

    # Load the champion genome from the saved file
    with open("top.pickle", "rb") as f:
        champion = pickle.load(f)

    # Evaluate the champion genome
    trainer = AIPongTrainer(window, width, height)
    trainer.evaluate_ai(champion, config)


if __name__ == "__main__":
    # Set up the NEAT configuration
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    
    #start_neat_training(config) #Uncomment this to train AI and create checkpoints
    evaluate_champion(config)