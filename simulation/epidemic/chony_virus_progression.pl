% stage(Name, ID).
% - asymptomatic
% - symptomatic
% - critical
% - terminal
% - recovered
% symptoms(ID, Symptom-list)
% infected_agent(ID, AgeGroup)
% symptoms(none, []).
% stage(none, none).
% age_group(none, none).

symptoms(1, []).
stage(1, 'asymptomatic').
age_group(1, 'old').


possible_symptoms_symptomatic([normal_fever, normal_cough, normal_short_breath, back_ache, stomach_ache, lazyness, sleepiness]).
possible_symptoms_critical([critical_fever, critical_cough, critical_short_breath, gastritis]).
possible_symptoms_terminal([candela, que_ostine]).

advance_dissease('terminal', AgeGroup, Symptoms, NextStage):-
    random(X),
    (X < 0.5 -> NextStage = 'dead';
    NextStage = 'terminal').

advance_dissease('critical', AgeGroup, Symptoms, NextStage):-
    length(Symptoms, Length),
    random(X),
    possible_symptoms_critical(Possible_Symptoms),
    (Length < 2 -> 
        random_member(Symptom, Possible_Symptoms),
        append(Symptoms, [Symptom], NewSymptoms),
        NextStage = 'critical';
    Length >= 2 -> 
        (X < 0.5 -> NextStage = 'terminal';
        random_member(Symptom, Possible_Symptoms),
        not(member(Symptom, Symptoms)),
        append(Symptoms, [Symptom], NewSymptoms),
        NextStage = 'critical';
        NextStage = 'recovered')).

advance_dissease(symptomatic, AgeGroup, Symptoms, NextStage):-
    length(Symptoms, Length),
    random(X),
    possible_symptoms_symptomatic(Possible_Symptoms),
    (Length < 2 -> 
        random_member(Symptom, Possible_Symptoms),
        append(Symptoms, [Symptom], NewSymptoms),
        NextStage = symptomatic;
    Length >= 2 ->
        (X < 0.5 -> NextStage = critical;
        random_member(Symptom, Possible_Symptoms),
        not(member(Symptom, Symptoms)),
        append(Symptoms, [Symptom], NewSymptoms),
        NextStage = symptomatic;
        NextStage = recovered)).

advance_dissease_asymptomatic(asymptomatic, AgeGroup, NextStage):-
    random(X),
    (AgeGroup == young -> (X < 0.25 -> NextStage = recovered; NextStage = symptomatic);
    AgeGroup == adult -> (X < 0.50 -> NextStage = recovered; NextStage = symptomatic);
    AgeGroup == old -> (X < 0.80 -> NextStage = recovered; NextStage = symptomatic)).

step(ID, NextStage):-
    stage(ID, CurrentStage),
    age_group(ID, AgeGroup),
    symptoms(ID, Symptoms),
    random(X),
    (
    (CurrentStage == asymptomatic, X < 0) -> advance_dissease_asymptomatic(CurrentStage, AgeGroup, NextStage);
    (member(CurrentStage, [symptomatic, critical]), X < 1) -> advance_dissease(CurrentStage, AgeGroup, Symptoms, NextStage)
    ).

:-dynamic(symptoms/2).
:-dynamic(stage/2).
:-dynamic(age_group/2).