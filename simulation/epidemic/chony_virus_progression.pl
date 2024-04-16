% Agent's facts format
% stage(ID, Stage)
% symptoms(ID, [Symptom1, Symptom2, ..., SymptomN])
% age_group(ID, AgeGroup)
% mask_usage(ID, MaskUsage)
% vaccination_status(ID, VaccinationStatus)

% Facts

infection_stages([asymptomatic, symptomatic, critical, terminal, recovered]).
mask_effectiveness(0.4).

% Vaccination effects

vaccination_effect(gets_better, 2).
vaccination_effect(gets_worse, 0.5).
vaccination_effect(nothing_happens, 1.0).

% Symptom notoriety

symptom_notoriety(normal_short_breath, 0.15).
symptom_notoriety(normal_cough, 0.15).
symptom_notoriety(normal_fever, 0.2).
symptom_notoriety(back_ache, 0.1).
symptom_notoriety(stomach_ache, 0.1).
symptom_notoriety(lazyness, 0.05).
symptom_notoriety(sleepiness, 0.1).

symptom_notoriety(critical_short_breath, 0.2).
symptom_notoriety(critical_cough, 0.2).
symptom_notoriety(critical_fever, 0.25).
symptom_notoriety(gastritis, 0.15).

symptom_notoriety(candela, 0.2).
symptom_notoriety(que_ostine, 0.15).
symptom_notoriety(terminal_fever, 0.25).

% Possible Symptoms/Stage

possible_symptoms_symptomatic([normal_fever, normal_cough, normal_short_breath, back_ache, stomach_ache, lazyness, sleepiness]).
possible_symptoms_critical([critical_fever, critical_cough, critical_short_breath, gastritis]).
possible_symptoms_terminal([terminal_fever, candela, que_ostine]).
possible_symptoms_recovered([]).

% Age Influence on the disease

age_influence(young, gets_better, 0.25).
age_influence(young, gets_worse, 0.15).
age_influence(young, nothing_happens, 0.6).

age_influence(adult, gets_better, 0.25).
age_influence(adult, gets_worse, 0.25).
age_influence(adult, nothing_happens, 0.5).

age_influence(old, gets_better, 0.15).
age_influence(old, gets_worse, 0.45).
age_influence(old, nothing_happens, 0.4).

% Symptoms Progression

symptom_progression(normal_fever, critical_fever).
symptom_progression(normal_cough, critical_cough).
symptom_progression(normal_short_breath, critical_short_breath).
symptom_progression(stomach_ache, gastritis).

symptom_progression(critical_fever, terminal_fever).

% Rules

% Symptom Progression
symptom_progression(Person, CurrentSymptom, NextSymptom) :-
    symptom_progression(CurrentSymptom, NextSymptom),
    symptoms(Person, Symptoms),
    member(CurrentSymptom, Symptoms).

% Add new symptoms for a person
add_symptoms(Person, NewSymptoms) :-
    retract(symptoms(Person, OldSymptoms)),
    append(OldSymptoms, NewSymptoms, AllSymptoms),
    assertz(symptoms(Person, AllSymptoms)).

% Remove symptoms for a person
remove_symptoms(Person, SymptomsToRemove) :-
    symptoms(Person, OldSymptoms),
    subtract(OldSymptoms, SymptomsToRemove, RemainingSymptoms),
    retract(symptoms(Person, _)),
    assertz(symptoms(Person, RemainingSymptoms)).

% Update person's stage
update_stage(Person, NewStage) :-
    retract(stage(Person, _)),
    assertz(stage(Person, NewStage)).


% Infection Progression
infection_gets_worse(Person, NextStage) :-
    stage(Person, CurrentStage),
    (
        (CurrentStage == symptomatic, count_symptomatic_symptoms(Person, Count), Count >= 4, NextStage = critical);
        (CurrentStage == critical, count_critical_symptoms(Person, Count), Count >= 2, NextStage = terminal);
        (CurrentStage == terminal, count_terminal_symptoms(Person, Count), Count >= 1, NextStage = dead);
        NextStage = CurrentStage
    ).

infection_gets_better(Person, NextStage) :-
    stage(Person, CurrentStage),
    (
        (CurrentStage == symptomatic, count_symptomatic_symptoms(Person, Count), Count == 0, NextStage = symptomatic);
        (CurrentStage == critical, count_critical_symptoms(Person, Count), Count == 0, NextStage = critical);
        (CurrentStage == terminal, count_terminal_symptoms(Person, Count), Count == 0, NextStage = terminal);
        NextStage = CurrentStage
    ).

% Count symptomatic symptoms
count_symptomatic_symptoms(Person, Count) :-
    symptoms(Person, Symptoms),
    intersection(Symptoms, [normal_fever, normal_cough, normal_short_breath, back_ache, stomach_ache, lazyness, sleepiness], SymptomaticSymptoms),
    length(SymptomaticSymptoms, Count).

% Count critical symptoms
count_critical_symptoms(Person, Count) :-
    symptoms(Person, Symptoms),
    intersection(Symptoms, [critical_fever, critical_cough, critical_short_breath, gastritis], CriticalSymptoms),
    length(CriticalSymptoms, Count).

% Count terminal symptoms
count_terminal_symptoms(Person, Count) :-
    symptoms(Person, Symptoms),
    intersection(Symptoms, [terminal_fever, candela, que_ostine], TerminalSymptoms),
    length(TerminalSymptoms, Count).

% Main function to simulate the progression of the disease
step(Person, NextStage, NewSymptoms, RemovedSymptoms) :-
    % Get the necessary information for the current agent
    vaccination_status(Person, VaccinationStatus),
    stage(Person, CurrentStage),
    age_group(Person, AgeGroup),
    symptoms(Person, CurrentSymptoms),

    % Determine if the infection will get worse, better or remain the same
    step_type(AgeGroup, VaccinationStatus, StepType),
    
    % Determine if there are any new symptoms to add
    available_symptoms(CurrentStage, CurrentSymptoms, PossibleSymptoms),
    
    % Changing the stage of the person if possible
    (
        (StepType == gets_better, infection_gets_better(Person, NextStage));
        (StepType == gets_worse, infection_gets_worse(Person, NextStage));
        (NextStage = CurrentStage)
    ).

% Calculating if a person gets better, worse or stays the same:
step_type(AgeGroup, VaccinationStatus, StepType):-
    once(step_type_gen(AgeGroup, VaccinationStatus, StepType)).

step_type_gen(AgeGroup, VaccinationStatus, StepType):-
    (
        (VaccinationStatus, vaccination_effect(gets_better, VaccinationEffectBetter));
        VaccinationEffectBetter = 1.0
    ),
    (
        (VaccinationStatus, vaccination_effect(gets_worse, VaccinationEffectWorse));
        VaccinationEffectWorse = 1.0
    ),
    (
        (VaccinationStatus, vaccination_effect(nothing_happens, VaccinationEffectNothing));
        VaccinationEffectNothing = 1.0
    ),
    age_influence(AgeGroup, gets_better, AgeInfluenceBetter),
    age_influence(AgeGroup, gets_worse, AgeInfluenceWorse),
    age_influence(AgeGroup, nothing_happens, AgeInfluenceNothing),
    Better is VaccinationEffectBetter * AgeInfluenceBetter,
    Worse is VaccinationEffectWorse * AgeInfluenceWorse,
    Nothing is VaccinationEffectNothing * AgeInfluenceNothing,
    random(0.0, 1.0, Random),
    (
        (Random < Better, StepType = gets_better);
        (Random < Better + Worse, StepType = gets_worse);
        (StepType = nothing_happens)
    ).

% Symptom Evolution
available_symptoms(Stage, Symptoms, StageSymptoms) :-
    once(available_symptoms_gen(Stage, Symptoms, StageSymptoms)).
%TODO: This method is returning several results.
available_symptoms_gen(Stage, Symptoms, StageSymptoms) :-
    ((member(Stage, [symptomatic, critical, terminal]),
        possible_symptoms_symptomatic(SympSymptoms), 
        get_new_evol(Symptoms, SympSymptoms, ValidSymptoms1)); ValidSymptoms1 = []),
    ((member(Stage, [critical, terminal]), 
        possible_symptoms_critical(CritSymptoms), 
        get_new_evol(Symptoms, CritSymptoms, ValidSymptoms2)); ValidSymptoms2 = []),
    ((member(Stage, [terminal]), 
        possible_symptoms_terminal(TerSymptoms), 
        get_new_evol(Symptoms, TerSymptoms, ValidSymptoms3)); ValidSymptoms3 = []),
    append(ValidSymptoms1, ValidSymptoms2, ValidSymptoms12),
    append(ValidSymptoms12, ValidSymptoms3, StageSymptoms).

get_new_evol(Symptoms, StageSymptoms, SymptomList) :-
    findall(NewSymptom, (
        (member(NewSymptom, StageSymptoms), \+ member(NewSymptom, Symptoms)),
    \+ (symptom_progression(OldSymptom, NewSymptom), \+ member(OldSymptom, Symptoms))
    ), NewSymptoms),
    SymptomList = NewSymptoms.

% Testing utility

adding_test_agents(1) :-
    retractall(stage(1, _)),
    retractall(age_group(1, _)),
    retractall(symptoms(1, _)),
    retractall(mask_usage(1, _)),
    retractall(vaccination_status(1, _)),
    assertz(stage(1, symptomatic)),
    assertz(age_group(1, adult)),
    assertz(symptoms(1, [normal_fever, normal_cough])),
    assertz(mask_usage(1, true)),
    assertz(vaccination_status(1, false)).

adding_test_agents(2) :-
    retractall(stage(2, _)),
    retractall(age_group(2, _)),
    retractall(symptoms(2, _)),
    retractall(mask_usage(2, _)),
    retractall(vaccination_status(2, _)),
    assertz(stage(2, critical)),
    assertz(age_group(2, old)),
    assertz(symptoms(2, [critical_fever, critical_cough, critical_short_breath, gastritis])),
    assertz(mask_usage(2, false)),
    assertz(vaccination_status(2, true)).

adding_test_agents(1).
adding_test_agents(2).

% Test Case 1: Progression from Symptomatic to Critical Stage
test_case_1 :-
    adding_test_agents(1),
    step(1, NextStage, NewSymptoms, RemovedSymptoms),
    NextStage = critical,
    NewSymptoms = [critical_short_breath, gastritis],
    RemovedSymptoms = [].

% Test Case 2: Progression from Critical to Terminal Stage
test_case_2 :-
    adding_test_agents(2),
    step(2, NextStage, NewSymptoms, RemovedSymptoms),
    NextStage = terminal,
    NewSymptoms = [terminal_fever],
    RemovedSymptoms = [].

% Test Case 3: Progression from Terminal to Dead Stage
test_case_3 :-
    retractall(stage(3, _)),
    retractall(symptoms(3, _)),
    assertz(stage(3, terminal)),
    assertz(age_group(3, young)),
    assertz(symptoms(3, [terminal_fever, candela, que_ostine])),
    assertz(mask_usage(3, true)),
    assertz(vaccination_status(3, false)),
    step(3, NextStage, NewSymptoms, RemovedSymptoms),
    NextStage = dead,
    NewSymptoms = [],
    RemovedSymptoms = [].
% Test Case 4: Progression from Asymptomatic to Symptomatic Stage
test_case_4 :-
    retractall(stage(4, _)),
    retractall(symptoms(4, _)),
    assertz(stage(4, asymptomatic)),
    assertz(age_group(4, adult)),
    assertz(symptoms(4, [])),
    assertz(mask_usage(4, true)),
    assertz(vaccination_status(4, false)),
    step(4, NextStage, NewSymptoms, RemovedSymptoms),
    NextStage = symptomatic,
    member(normal_fever, NewSymptoms),
    RemovedSymptoms = [].

% Test Case 5: Progression from Symptomatic to Recovered Stage
test_case_5 :-
    retractall(stage(5, _)),
    retractall(symptoms(5, _)),
    assertz(stage(5, symptomatic)),
    assertz(age_group(5, old)),
    assertz(symptoms(5, [normal_fever, normal_cough])),
    assertz(mask_usage(5, true)),
    assertz(vaccination_status(5, false)),
    step(5, NextStage, NewSymptoms, RemovedSymptoms),
    NextStage = recovered,
    NewSymptoms = [],
    RemovedSymptoms = [normal_fever, normal_cough].

% Test Case 6: Progression from Asymptomatic to Recovered Stage
test_case_6 :-
    retractall(stage(6, _)),
    retractall(symptoms(6, _)),
    assertz(stage(6, asymptomatic)),
    assertz(age_group(6, young)),
    assertz(symptoms(6, [])),
    assertz(mask_usage(6, false)),
    assertz(vaccination_status(6, true)),
    step(6, NextStage, NewSymptoms, RemovedSymptoms),
    NextStage = recovered,
    NewSymptoms = [],
    RemovedSymptoms = [].

% Test Case 7: Progression from Asymptomatic to Dead Stage
test_case_7 :-
    retractall(stage(7, _)),
    retractall(symptoms(7, _)),
    assertz(stage(7, asymptomatic)),
    assertz(age_group(7, adult)),
    assertz(symptoms(7, [])),
    assertz(mask_usage(7, false)),
    assertz(vaccination_status(7, false)),
    step(7, NextStage, NewSymptoms, RemovedSymptoms),
    NextStage = dead,
    NewSymptoms = [],
    RemovedSymptoms = [].
