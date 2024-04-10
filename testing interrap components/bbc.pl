% behavior_patterns.pl

% Behavior patterns for healthy citizens
healthy_citizen_behavior(social_distancing).
healthy_citizen_behavior(wearing_mask).

% Behavior patterns for infected citizens
infected_citizen_behavior(isolation).
infected_citizen_behavior(seeking_medical_help).

% Behavior patterns for citizens in quarantine
quarantined_citizen_behavior(stay_home).
quarantined_citizen_behavior(wearing_mask).

% Rule to determine behavior based on health status
behavior(Citizen, Behavior) :-
    healthy(Citizen),
    healthy_citizen_behavior(Behavior).

behavior(Citizen, Behavior) :-
    infected(Citizen),
    infected_citizen_behavior(Behavior).

behavior(Citizen, Behavior) :-
    quarantined(Citizen),
    quarantined_citizen_behavior(Behavior).
