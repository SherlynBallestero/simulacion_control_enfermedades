class InteRRaPAgent:
    def __init__(self, name):
        self.name = name
        self.reactive_component = None
        self.local_planning_component = None
        self.cooperative_component = None

    def set_reactive_component(self, component):
        self.reactive_component = component

    def set_local_planning_component(self, component):
        self.local_planning_component = component

    def set_cooperative_component(self, component):
        self.cooperative_component = component

    def act(self, agent_state):
        # Example: Use the components to determine the agent's action
        reactive_action = self.reactive_component(agent_state)
        planning_action = self.local_planning_component(agent_state)
        cooperative_action = self.cooperative_component(agent_state)

        # Combine actions as needed (this is a simplified example)
        return f"{reactive_action}, {planning_action}, {cooperative_action}"

def reactive_component(agent_state):
    # Example: React to the environment based on the agent's state
    if agent_state['infected']:
        return 'isolate'
    else:
        return 'socialize'

def local_planning_component(agent_state):
    # Example: Plan actions based on the agent's state
    if agent_state['infected']:
        return 'seek_medical_help'
    else:
        return 'maintain_social_distance'

def cooperative_component(agent_state):
    # Example: Cooperate with other agents based on the agent's state
    if agent_state['infected']:
        return 'inform_others'
    else:
        return 'share_information'
agent = InteRRaPAgent("Agent1")
agent.set_reactive_component(reactive_component)
agent.set_local_planning_component(local_planning_component)
agent.set_cooperative_component(cooperative_component)


def main():
    # Example agent state
    agent_state = {
        'infected': False,
        'social_distance': True,
        'medical_help_available': True
    }

    # Agent acts based on its state
    action = agent.act(agent_state)
    print(f"Agent action: {action}")