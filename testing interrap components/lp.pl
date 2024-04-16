
% infected(Id, perception).
% infected(Id, comunication).
% trust([Id]).
% work_place(Id, status).
% working_hours(start, end).
% home(id).
% curfew(True).
% curfew(False).
% curfew_hours(start, end).
% social_distancing(True).
% social_distancing(False).
% public_transport_available([Id]).
% public_transport_unavailable([Id]).
% status(susceptible).
% status(infected).
% status(recovered).

healthy(none).
quarantined(none).
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



:-dynamic(infected/1).















% % Facts representing the current state of the world
% at(robot, location1).
% at(object1, location2).
% at(object2, location3).

% % Goals
% goal(at(object1, location1)).
% goal(at(object2, location1)).

% % Actions and their preconditions
% action(move(X, Y), [at(X, Z)], [at(X, Y)]).

% % Rule to plan actions
% plan(Goal) :-
%     goal(Goal),
%     plan(Goal, []).

% plan(Goal, _) :-
%     goal(Goal).

% plan(Goal, Plan) :-
%     action(Action, Preconditions, Effects),
%     not(member(Action, Plan)),
%     all_true(Preconditions),
%     append(Plan, [Action], NewPlan),
%     plan(Goal, NewPlan).

% % Helper predicates
% all_true([]).
% all_true([H|T]) :-
%     call(H),
%     all_true(T).

% member(X, [X|_]).
% member(X, [_|T]) :-
%     member(X, T).
