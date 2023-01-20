import environment as e

import random

loc_A, loc_B = (0, 0), (1, 0)

def ReflexVacuumAgent():
    def program(percept):
        location, status = percept
        if status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Left'

    return e.Agent(program)


class TrivialVacuumEnvironment(e.Environment):
    def __init__(self):
        super().__init__()
        self.status = {loc_A: random.choice(['Clean', 'Dirty']),
                       loc_B: random.choice(['Clean', 'Dirty'])}
        self.score = 0

    """ perceptions from percepts. """
    def percept(self, agent):
        return agent.location, self.status[agent.location]

    """ actions from actuators.  """
    def execute_action(self, agent, action):
        # score a point for each clean square
        if self.status[loc_A] == 'Clean':
            self.score += 1
        if self.status[loc_B] == 'Clean':
            self.score += 1

        # lose a point for moving
        if (action == 'Right'):
            agent.location = (1, 0)
            self.score -= 1
        if (action == 'Left'):
            agent.location = (0, 0)
            self.score -= 1
        if (action == 'Suck'):
            self.status[agent.location] = 'Clean'

    def show_status(self):
        print(self.status)

    def thing_classes(self):
        return [ReflexVacuumAgent]


# instantiate trivial environment
env = TrivialVacuumEnvironment()
# instantiate trivial agent
agnt = ReflexVacuumAgent()
# add agent to environment
env.add_thing(agnt, location=loc_A)
env.show_status()
print(agnt.location)
# step forward and show status
env.step()
env.show_status()
print(agnt.location)
# ...and again
env.step()
env.show_status()
print(agnt.location)
# ...and again
env.step()
env.show_status()
print(agnt.location)
