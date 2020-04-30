import gym
import numpy as np
import math
from collections import deque
import matplotlib.pyplot as plt


class QCartPoleSolver:
    def __init__(self, buckets=(1, 1, 6, 12), n_episodes=200, min_alpha=0.1, min_epsilon=0.1, gamma=1.0, ada_div=25):
        self.buckets = buckets  # Diskreetsete võimalike väärtuste arv (1 -> tähtsusetu ehk viskan minema)
        self.n_episodes = n_episodes  # Treeningepisoodide arv
        self.min_alpha = min_alpha  # Õppimise kiirus
        self.min_epsilon = min_epsilon  # avastamise faktor
        self.gamma = gamma
        self.ada_divisor = ada_div  # konstant parema alpha ja epsiloni arvutamiseks

        self.scores_mean = [0]  # Vahevastused
        self.scores_all = []  # -||-

        self.env = gym.make('CartPole-v0')

        self.Q = np.zeros(self.buckets + (self.env.action_space.n,))  # Q-tabel

    def discretize(self, obs):  # Tagastab vahemiku kuhu ta protsentuaalselt jääb
        upper_bounds = [self.env.observation_space.high[0], 0.5, self.env.observation_space.high[2], math.radians(50)]
        lower_bounds = [self.env.observation_space.low[0], -0.5, self.env.observation_space.low[2], -math.radians(50)]
        ratios = [(obs[i] + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i]) for i in range(len(obs))]
        new_obs = [int(round((self.buckets[i] - 1) * ratios[i])) for i in range(len(obs))]
        new_obs = [min(self.buckets[i] - 1, max(0, new_obs[i])) for i in range(len(obs))]
        return tuple(new_obs)

    def choose_action(self, state, epsilon):  # tagastab kas suvalise või parima käigu tabelist vastavalt epsilonile
        return self.env.action_space.sample() if (np.random.random() <= epsilon) else np.argmax(self.Q[state])

    def update_q(self, state_old, action, reward, state_new, alpha):  # http://lambda.ee/wiki/Iti0210lab142
        self.Q[state_old][action] += alpha * (reward + self.gamma * max(self.Q[state_new]) - self.Q[state_old][action])

    def get_epsilon(self, t):
        return max(self.min_epsilon, min(1, 1.0 - math.log10((t + 1) / self.ada_divisor)))

    def get_alpha(self, t):
        return max(self.min_alpha, min(1.0, 1.0 - math.log10((t + 1) / self.ada_divisor)))

    def run(self):
        buffer = 20
        scores = deque(maxlen=buffer)

        for e in range(1, self.n_episodes + 1):
            self.env.render()
            current_state = self.discretize(self.env.reset())

            alpha = self.get_alpha(e)
            epsilon = self.get_epsilon(e)
            done = False
            i = 0

            while not done:
                action = self.choose_action(current_state, epsilon)
                obs, reward, done, _ = self.env.step(action)
                new_state = self.discretize(obs)
                self.update_q(current_state, action, reward, new_state, alpha)
                current_state = new_state
                i += 1

            scores.append(i)
            if e % buffer == 0:
                mean_score = np.mean(scores)
                print('[Episode {}] - Mean survival time over last {} episodes was {} ticks.'.format(e, buffer, mean_score))
                self.scores_mean.append(mean_score)
            self.scores_all.append(i)

        plt.plot([x + 1 for x in range(self.n_episodes)], self.scores_all, 'ro')
        plt.plot([x * buffer for x in range(len(self.scores_mean))], self.scores_mean, 'k')

        plt.ylabel('episoodi pikkus')
        plt.xlabel('iteratsioonide arv')
        plt.show()

        self.env.close()


if __name__ == "__main__":
    solver = QCartPoleSolver()
    solver.run()
