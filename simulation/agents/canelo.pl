symptoms_of_disease([cough]).

% Specific control measures for symptoms
control_measure(normal_fever, mask_use).
control_measure(normal_cough, social_distancing).
control_measure(normal_short_breath, tests_and_diagnosis).
control_measure(back_ache, contact_tracing).
control_measure(stomach_ache, isolation).
control_measure(laziness, quarantine).
control_measure(sleepiness, vaccination).

% Specific control measures for critical symptoms
control_measure(critical_fever, quarantine).
control_measure(critical_cough, social_distancing).
control_measure(critical_short_breath, isolation).
control_measure(gastritis, social_distancing).

% Specific control measures for terminal symptoms
control_measure(terminal_fever, isolation).
control_measure(candela, isolation).
control_measure(que_ostine, isolation).

recommendation_control_measure(low, mask_use).
recommendation_control_measure(low, social_distancing).

recommendation_control_measure(high, tests_and_diagnosis).
recommendation_control_measure(high, contact_tracing).
recommendation_control_measure(high, vaccination).

recommendation_control_measure(terminal, isolation).
recommendation_control_measure(terminal, quarantine).

% Specific measures for certain types of places
measure_closure_place(public_place, use_mask).
measure_closure_place(public_place, social_distancing).
measure_closure_place(public_place, temporary_closure).

measure_closure_place(work, use_mask).
measure_closure_place(work, social_distancing).
measure_closure_place(work, temporary_closure).

% control_measures_based_on_symptoms(Symptoms, Measures) :-
%     findall(Measure, control_measure(Symptoms, Measure), Measures).

closure_measures_based_on_place_type(PlaceType, Measures) :-
    findall(Measure, measure_closure_place(PlaceType, Measure), Measures).

recommendation_based_on_severity(PeopleSick, Recommendation, RecomendationPlaces) :-
    (PeopleSick < 0.3 -> recommendation_control_measure(low, Recommendation));

    (PeopleSick < 0.7 -> recommendation_control_measure(high, Recommendation),
                        closure_measures_based_on_place_type(public_place, RecomendationPlaces));

    (PeopleSick < 1 -> recommendation_control_measure(terminal, Recommendation),
                        closure_measures_based_on_place_type(work, RecomendationPlaces)).


