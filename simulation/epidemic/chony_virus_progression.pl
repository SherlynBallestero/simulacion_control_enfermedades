% Agent's facts format
% stage(ID, Stage)
% symptoms(ID, [Symptom1, Symptom2, ..., SymptomN])
% age_group(ID, AgeGroup)
% mask_usage(ID, MaskUsage)
% vaccination_status(ID, VaccinationStatus)

% Facts

infection_stages([asymptomatic, symptomatic, critical, terminal]).
base_transmition_rate(1.0).
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

age_influence(young, gets_better, 0.005).
age_influence(young, gets_worse, 0.003).
age_influence(young, nothing_happens, 0.992).

age_influence(adult, gets_better, 0.005).
age_influence(adult, gets_worse, 0.005).
age_influence(adult, nothing_happens, 0.990).

age_influence(old, gets_better, 0.005).
age_influence(old, gets_worse, 0.015).
age_influence(old, nothing_happens, 0.980).

% Symptoms Progression

symptom_progression(normal_fever, critical_fever).
symptom_progression(normal_cough, critical_cough).
symptom_progression(normal_short_breath, critical_short_breath).
symptom_progression(stomach_ache, gastritis).

symptom_progression(critical_fever, terminal_fever).

% Rules
% Add person's data
add_agent(Person, VaccinationStatus, AgeGroup):-
    assertz(vaccination_status(Person, VaccinationStatus)),
    assertz(age_group(Person, AgeGroup)),
    assertz(stage(Person, asymptomatic)),
    assertz(symptoms(Person, [])).

% Remove person's data
remove_agent(Person) :-
    retractall(stage(Person, _)),
    retractall(vaccination_status(Person, _)),
    retractall(age_group(Person, _)),
    retractall(symptoms(Person, _)).

% Update person's data
update_agent(Person, NewStage, NewSymptoms, NewVaccinationStatus, NewAgeGroup) :-
    update_stage(Person, NewStage),
    update_symptoms(Person, NewSymptoms),
    update_vaccination_status(Person, NewVaccinationStatus),
    update_age_group(Person, NewAgeGroup).

update_stage(Person, NewStage) :-
    retract(stage(Person, _)),
    assertz(stage(Person, NewStage)).

update_symptoms(Person, NewSymptoms) :-
    retract(symptoms(Person, _)),
    assertz(symptoms(Person, NewSymptoms)).

update_vaccination_status(Person, NewVaccinationStatus) :-
    retract(vaccination_status(Person, _)),
    assertz(vaccination_status(Person, NewVaccinationStatus)).

update_age_group(Person, NewAgeGroup) :-
    retract(age_group(Person, _)),
    assertz(age_group(Person, NewAgeGroup)).

% Main function to simulate the progression of the disease
step(Person, NextStage, NewSymptoms, StepType) :-
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
    once(
    (StepType == gets_better, 
        once(infection_gets_better(CurrentSymptoms, CurrentStage, NextStage, NewSymptoms)));
    (StepType == gets_worse,
        once(infection_gets_worse(CurrentSymptoms, CurrentStage, PossibleSymptoms, NextStage, NewSymptoms)));
    (NextStage = CurrentStage, NewSymptoms = CurrentSymptoms)
    ),

    % Updating agent information
    once(
        (member(NextStage, [recovered, dead]), remove_agent(Person));
        (update_stage(Person, NextStage),update_symptoms(Person, NewSymptoms))
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
    % (
    %     (VaccinationStatus, vaccination_effect(nothing_happens, VaccinationEffectNothing));
    %     VaccinationEffectNothing = 1.0
    % ),
    age_influence(AgeGroup, gets_better, AgeInfluenceBetter),
    age_influence(AgeGroup, gets_worse, AgeInfluenceWorse),
    % age_influence(AgeGroup, nothing_happens, AgeInfluenceNothing),
    Better is VaccinationEffectBetter * AgeInfluenceBetter,
    Worse is VaccinationEffectWorse * AgeInfluenceWorse,
    % Nothing is VaccinationEffectNothing * AgeInfluenceNothing,
    random(0.0, 1.0, Random),
    (
        (Random < Better, StepType = gets_better);
        (Random < Better + Worse, StepType = gets_worse);
        (StepType = nothing_happens)
    ).

% Symptom Evolution
available_symptoms(Stage, Symptoms, StageSymptoms) :-
    once(available_symptoms_gen(Stage, Symptoms, StageSymptoms)).

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

% Infection Progression
infection_gets_worse(Symptoms, CurrentStage, PossibleSymptoms, NextStage, NextSymptoms) :-
    % Add or evolve symptoms
    ((\+ length(PossibleSymptoms, 0), once(random_member(Symptom, PossibleSymptoms)), add_symptom(Symptom, Symptoms, NextSymptoms));
    NextSymptoms = []),
    
    % Change Stage if possible
    ((CurrentStage == asymptomatic,
        NextStage = symptomatic);
    (CurrentStage == symptomatic, 
        count_symptomatic_symptoms(Symptoms, Count1), Count1 >= 4, 
        NextStage = critical);
    (CurrentStage == critical, 
        count_critical_symptoms(Symptoms, Count2), Count2 >= 2, 
        NextStage = terminal);
    (CurrentStage == terminal, 
        count_terminal_symptoms(Symptoms, Count3), Count3 >= 1, 
        NextStage = dead);
    NextStage = CurrentStage).

add_symptom(Symptom, Symptoms, NextSymptoms) :-
    (symptom_progression(PreviousSymptom, Symptom),
    select(PreviousSymptom, Symptoms, CleanSymptomsList),
    append(CleanSymptomsList, [Symptom], NextSymptoms));
    (append(Symptoms, [Symptom], NextSymptoms)).

infection_gets_better(Symptoms, CurrentStage, NextStage, NextSymptoms) :-
    % Remove or devolve symptoms
    ((\+ length(Symptoms, 0), once(random_member(Symptom, Symptoms)), remove_symptom(Symptom, Symptoms, NextSymptoms));
    NextSymptoms = []),
    
    % Change Stage if possible
    (
    (CurrentStage == asymptomatic,
        NextStage = recovered);
    (CurrentStage == symptomatic, 
        count_symptomatic_symptoms(Symptoms, 0), 
        NextStage = asymptomatic);
    (CurrentStage == critical, 
        count_critical_symptoms(Symptoms, 0), 
        NextStage = symptomatic);
    (CurrentStage == terminal, 
        count_terminal_symptoms(Symptoms, 0), 
        NextStage = critical);
    NextStage = CurrentStage).

remove_symptom(Symptom, Symptoms, NextSymptoms) :-
    (symptom_progression(PreviousSymptom, Symptom),
    select(Symptom, Symptoms, CleanSymptomsList),
    append(CleanSymptomsList, [PreviousSymptom], NextSymptoms));
    (select(Symptom, Symptoms, NextSymptoms)).

% Count symptomatic symptoms
count_symptomatic_symptoms(Symptoms, Count) :-
    intersection(Symptoms, [normal_fever, normal_cough, normal_short_breath, back_ache, stomach_ache, lazyness, sleepiness], SymptomaticSymptoms),
    length(SymptomaticSymptoms, Count).

% Count critical symptoms
count_critical_symptoms(Symptoms, Count) :-
    intersection(Symptoms, [critical_fever, critical_cough, critical_short_breath, gastritis], CriticalSymptoms),
    length(CriticalSymptoms, Count).

% Count terminal symptoms
count_terminal_symptoms(Symptoms, Count) :-
    intersection(Symptoms, [terminal_fever, candela, que_ostine], TerminalSymptoms),
    length(TerminalSymptoms, Count).

% Testing utility

% adding_test_agents(1) :-
%     retractall(stage(1, _)),
%     retractall(age_group(1, _)),
%     retractall(symptoms(1, _)),
%     retractall(mask_usage(1, _)),
%     retractall(vaccination_status(1, _)),
%     assertz(stage(1, symptomatic)),
%     assertz(age_group(1, adult)),
%     assertz(symptoms(1, [normal_fever, normal_cough])),
%     assertz(mask_usage(1, true)),
%     assertz(vaccination_status(1, false)).

% adding_test_agents(2) :-
%     retractall(stage(2, _)),
%     retractall(age_group(2, _)),
%     retractall(symptoms(2, _)),
%     retractall(mask_usage(2, _)),
%     retractall(vaccination_status(2, _)),
%     assertz(stage(2, critical)),
%     assertz(age_group(2, old)),
%     assertz(symptoms(2, [critical_fever, critical_cough, critical_short_breath, gastritis])),
%     assertz(mask_usage(2, false)),
%     assertz(vaccination_status(2, true)).
