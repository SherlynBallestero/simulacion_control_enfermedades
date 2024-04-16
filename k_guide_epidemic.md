### Important Knowledge for the Epidemic Model:

#### Stage:
- **Description**: Represents the stage of the disease an agent is in. The disease progresses from lighter to more severe stages probabilistically based on symptoms and the agent's age. Movement to the recovered stage is only possible from the asymptomatic stage. The disease can either worsen or improve; initially, it can only worsen, adding new symptoms and advancing stages. However, at any point, it can start improving until the agent is recovered. Death can only occur at the terminal stage, where recovery is not possible.
- **Possible Values**:
  - asymptomatic
  - symptomatic
  - critical
  - terminal
  - recovered

#### Symptoms:
- **Description**: A list representing all the symptoms an agent has. An agent can have multiple symptoms simultaneously. Symptoms can evolve as the disease progresses. During the disease's progression phase, symptoms can only worsen or increase, while during the recovery phase, symptoms can only decrease until none are present, at which point the agent is considered asymptomatic again.
- **Example**: `[normal_fever, normal_cough, normal_short_breath, back_ache]`

#### Age Group:
- **Description**: Represents the age group of an agent. Younger agents have a better chance of recovering faster and experience periods where the disease does not change, while older agents have a higher chance of worsening.
- **Possible Values**:
  - young
  - adult
  - old

#### Symptom Notoriety:
- **Description**: Represents how noticeable each symptom is.
- **Example**:
  - `symptom_notoriety(normal_fever, 0.1)`
  - `symptom_notoriety(critical_fever, 0.25)`

#### Age Influence:
- **Description**: Represents how age influences the disease.
- **Possible Consequences**:
  - gets_better
  - gets_worse
  - nothing_happens

#### Mask Effectiveness:
- **Description**: Represents how much wearing a mask affects the contact spreading of the disease. It is not used in the calculation of disease progression but is used in the calculation of the contact rate, outside of the disease knowledge base.
- **Example**: `mask_effectiveness(0.4)`

#### Vaccination Effectiveness:
- **Description**: Represents how much the vaccine affects the evolution of the disease. It reduces the chances of worsening and increases the chances of improvement.
- **Example**: `vaccination_effectiveness(0.3)`

### Important Knowledge for the Epidemic Model Outside of the Knowledge Base:

#### Agent:
- **Description**: Represents an individual in the simulation.
- **Factors Influencing Contact and Disease Spreading**:
  - Age Group
  - Agent ID
  - Mask Usage
  - Vaccination Status
  - Previous Related Conditions (not yet implemented)

#### Map:
- **Description**: Represents the environment where agents interact.
- **Factor Influencing Contact**: Contact rate of the current node.

### Notes (To Implement Later):
- Consider adding other non-disease-related symptoms to increase the complexity of the simulation and challenge agents to differentiate between regular symptoms and those related to the disease.