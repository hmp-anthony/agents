import collections
import collections.abc
import numbers
import random


class Thing:
    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))

    def is_alive(self):
        return hasattr(self, 'alive') and self.alive

    def show_state(self):
        print("I don't know how to show_state.")


class Agent(Thing):
    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program is None or not isinstance(program, collections.abc.Callable):
            print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

            def program(percept):
                return eval(input('Percept={}; action? '.format(percept)))

        self.program = program

    def can_grab(self, thing):
        """Return True if this agent can grab this thing.
        Override for appropriate subclasses of Agent and Thing."""
        return False

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
    
    return Agent(program)


class Environment:
    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self  ):
        return []  # List of classes that can go into environment

    def percept(self, agent):
        """Return the percept that the agent sees at this point. (Implement this.)"""
        raise NotImplementedError

    def execute_action(self, agent, action):
        """Change the world to reflect this action. (Implement this.)"""
        raise NotImplementedError

    def default_location(self, thing):
        """Default location to place a new thing with unspecified location."""
        return None

    def is_done(self):
        """By default, we're done when we can't find a live agent."""
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)

    def add_thing(self, thing, location=None):
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        if thing in self.things:
            print("Can't add the same thing twice")
        else:
            thing.location = location if location is not None else self.default_location(thing)
            self.things.append(thing)
            if isinstance(thing, Agent):
                thing.performance = 0
                self.agents.append(thing)


class Dirt(Thing):
    pass


class TrivialVacuumEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.status = {loc_A: random.choice(['Clean', 'Dirty']),
                       loc_B: random.choice(['Clean', 'Dirty'])}

    def percept(self, agent):
        return agent.location, self.status[agent.location]

    def execute_action(self, agent, action):
        if(action == 'Right'):
            agent.location = (1, 0)
        if(action == 'Left'):
            agent.location = (0, 0)
        if(action == 'Suck'):
            self.status[agent.location] = 'Clean'

    def show_status(self):
        print(self.status)

    def thing_classes(self):
        return [Dirt, ReflexVacuumAgent]




# instantiate trivial environment 
env = TrivialVacuumEnvironment()
# instantiate trivial agent
agnt = ReflexVacuumAgent()
# add agent to environment
env.add_thing(agnt, location=loc_A)
env.show_status()
print(agnt.location)
# step forward
env.step() 
env.show_status()
print(agnt.location)

