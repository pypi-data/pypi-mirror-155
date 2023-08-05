[![PyPI version](https://badge.fury.io/py/gym-qRacing.svg)](https://pypi.org/project/gym-qRacing/)

# Deep Q-Racing

### Improving race strategy decision-making in motorsports through self-learning deep neural networks

Deep Q-Racing is a research project into the potential of using Reinforcement Learning for automating
race simulations and thus improving the comprehensiveness of results as-well as the possible amount of runs.

<br>

## 🎓 Background

<details>
<summary>View abstract</summary>
<br>
One decisive factor in the outcome of races in circuit motorsports is the race strategy.
The strategic potential of this strategy hereby stems from the timing of pit stops.
These stops become neccessary, as fuel is consumed and tires decrease in performance over the course of a race.
Deciding on a pit stop to replace these tires with a new set and refueling the car for the desired stint length contracts these affects.
Such a stop also induces drawback in form of time loss, as a speed limit is enforced when traveling through the pit lane.
Furthermore, the service conducted on the car might also increase this time loss.

Race strategy is therefore defined as balancing the benefits and costs of pit stops.
As of today, race simulations are applied in order to estimate the best possible race strategy beforehand, which reduces the required race time to a minimum.
These simulations greatly vary in granularity in prior literature and effects of probabilistic nature have to be considered.
Also, manual input of desired inlaps has to be made for each participant.

Such a simulation is implemented in this work and further adapted to the regulations of the NLS race series.
The simulation is integrated with OpenAi’s Gym framework, to serve as an environment for reinforcement learning agents to train in.
In order to automate the race simulation, an agent is implemented with the TensorFlow framework and the training is stabilized through experience replay.
Different hyper-parameter configurations, as well as observation-spaces and reward functions are evaluated.

It was found, that the agent made reasonable decisions regarding pit stop timing and refuel amount.
The learning rate and amount of episodes proved to be the most important parameters and using tire degradation in conjunction with the
current race position was found to be most fitting for policy development.

Keywords: race simulation, race strategy, Reinforcement Learning

</details>

<br>
