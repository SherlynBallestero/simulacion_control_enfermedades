from pyswip import Prolog
import random
class WorldModel:
    def __init__(self, environment, perception,action):
        self.world_model = environment
        self.perception_module = perception
        self.action_module = action

    def perceive(self):
        # Implement perception logic here
        pass

    def act(self, action):
        # Implement action logic here
        pass
class BehaviorLayer:
    def __init__(self, world_model, knowledge):
        self.world_model = world_model
        self.prolog = Prolog()
        self.prolog.consult('hierarchical_agent_KB.pl')

    def react(self, queryString):
        query = f"{queryString}"
        action = []
        for result in self.prolog.query(query):
            action.append(result['FunctionName'])
            action.append(result['Args'])
            
        # if not actions:
        #     action = self.chose_action(actions)
        
        try:
            return action[0], action[1]
        except:
            return None, None
    

class LocalPlanningLayer:
    def __init__(self, behavior_layer_based):
        self.behavior_layer_based = behavior_layer_based
        self.plans = {} # Dictionary of plans

    def plan(self, goal):
        # Implement planning logic here
        pass

class CooperativeLayer:
    def __init__(self, local_planning_layer):
        self.local_planning_layer = local_planning_layer

    def cooperate(self, goal):
        # Implement cooperative planning logic here
        pass

def main():
    world_interface = WorldModel()
    behavior_layer_based = BehaviorLayer(world_interface)
    local_planning_layer = LocalPlanningLayer(behavior_layer_based)
    cooperative_layer = CooperativeLayer(local_planning_layer)

    # Example of use
    situation = "example_situation"
    goal = "example_goal"
    cooperative_layer.cooperate(goal)

if __name__ == "__main__":
    main()