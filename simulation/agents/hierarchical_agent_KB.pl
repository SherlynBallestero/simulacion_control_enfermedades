%---------------------------- Knowledge -----------------------------------------------

% week_day(WeekDay).
% month_day(MonthDay).
% hour(Hour).
% min(Min).
% home(Id).
% work_place(Id).
% open_place(Id, Bool).
% open_hours_place(ID, OH, CH).
% disease_symptoms(SymptomList).
% my_symptoms(SymptomList).
% is_medical_personal(Bool).
% mask_necessity(Bool).
% mask_requirement(PlaceID, Bool).
% goal(Goal1).
% goal(Goal2).
% public_space(Id, Address).
% space_capacity_state(Id, CapacityState).
% hospital(Id, Address).
% hospital_overrun(Id, OverrunBool).
% public_transportation_working(Id, Bool).
% public_transportation_schedule(Id, AddrList).
% hospital_acepting_patients(Id, Bool).

% goal(move, 1).
% hour(16).
% position(5).

% my_symptoms([tos]).
% use_personal_mask(false).
% open_place(_, true).
% mask_requirement(_,true).
% mask_necessity(true).
% public_transportation_working(_, true).
% public_transportation_schedule(2, [1,6,4,7,5,8,78,9,37]).
% hospital_acepting_patients(_, true).
% disease_symptoms([tos]).
% hospital(5,_).
% public_space(77, _).
% public_space(44, _).
% isolation_center(45, _).
% work_place(66).
% home(55).

initialize_k():-
    assert(too_sick(false)),
    assert(wearing_mask(false)),
    assert(social_distancing(false)).

add_node_info(Id, Address, CapacityStatus, NodeType):-%TODO: see if this is necesary and if it works
    retractall(node(Id, _, _, _)),
    assert(node(Id, Address, CapacityStatus, NodeType)),
    (not(NodeType), open_place(Id, true)).

add_map_node(Id, Address, CapacityStatus, NodeType):-
    (NodeType = hospital, 
        add_hospital(Id, Address), retractall(place_status(Id, _)), assert(place_status(Id, CapacityStatus)));
    (NodeType = public_space, 
        add_public_space(Id, Address), retractall(place_status(Id, _)), assert(place_status(Id, CapacityStatus)));
    (NodeType = block, 
        add_block_info(Id, Address), retractall(place_status(Id, _)), assert(place_status(Id, CapacityStatus))).

add_block_info(Id, Address):-
    retractall(block(Id, _)),
    assert(block(Id, Address)).

add_public_space(Id, Address):-
    retractall(public_space(Id, _)),
    retractall(open_place(Id, true)),
    assert(open_place(Id, true)),
    assert(public_space(Id, Address)).

add_home(Node):-
    retractall(home(_)),
    assert(home(Node)).

add_work_place(Node, Address):-
    retractall(work_place(_, _)),
    retractall(open_place(Node, true)),
    assert(open_place(Node, true)),
    assert(work_place(Node, Address)).

add_open_place(Node, Bool):-
    retractall(open_place(Node,_)),
    assert(open_place(Node, Bool)).

add_open_hours_place(Node, Initial, Final):-
    retractall(open_hours_place(Node, _, _)),
    assert(open_hours_place(Node,Initial,Final)).

add_date(WeekDayK, MonthDayK, HourK, MinK):-
    retractall(week_day(_)),
    retractall(month_day(_)),
    retractall(min(_)),
    retractall(hour(_)),
    assert(week_day(WeekDayK)),
    assert(month_day(MonthDayK)),
    assert(hour(HourK)),
    assert(min(MinK)).

add_symptom(Symptom):-
    my_symptoms(S),
    not(member(Symptom, S)),
    Symptom_list_result = [Symptom| S],
    retractall(my_symptoms(_)),
    asserta(my_symptoms(Symptom_list_result)).
    
add_hospital(HospitalId, Address):-
    retractall(hospital(HospitalId, _)),
    asserta(hospital(HospitalId, Address)).
    
add_disease_symptoms(S):-
    retractall(disease_symptoms(_)),
    assert(disease_symptoms(S)).

add_if_is_medical_personal(Bool):-
    retractall(is_medical_personal(_)),
    assert(is_medical_personal(Bool)).

add_mask_necessity(Bool):-
    retractall(mask_knowledge(_)),
    assert(mask_knowledge(Bool)).

add_place_to_use_mask(Place, Bool):-
    retractall(mask_requirement(Place,_)),
    assert(mask_requirement(Place, Bool)).

add_location(Node):-
    retractall(location(_)),
    assert(location(Node)).

add_quarantine(Bool):-
    retractall(quarantine(_)),
    assert(quarantine(Bool)).

add_social_distancing(Bool):-
    retractall(social_distancing(_)),
    assert(social_distancing(Bool)).

add_tests_and_diagnosis(Bool):-
    retractall(tests_and_diagnosis(_)),
    assert(tests_and_diagnosis(Bool)).

add_contact_tracing(Bool):-
    retractall(contact_tracing(_)),
    assert(contact_tracing(Bool)).

add_isolation(Bool):-
    retractall(isolation(_)),
    assert(isolation(Bool)).

work_is_open(WorkId):-
    not(week_day(saturday)),
    not(week_day(sunday)),
    hour(H),
    open_hours_place(WorkId,I,F),
    open_place(WorkId, true),
    H >= I,
    H =< F.

%---------------------------- Patterns of Behaviour -----------------------------------------------

check_goals():-
    ((location(Id), goal(move, Id)) ->
        (retractall(goal(move, Id)))
    );
    ((goal(work), hour(H), work_place(WorkId, _), open_hours_place(WorkId,_,F), H >= F) ->
        retractall(goal(work)));

    (goal(wear_mask), wearing_mask(true) ->
        retractall(goal(wear_mask)));

    ((goal(medical_check), location(Id), open_hours_place(Id,_,C), hour(H), C == H) ->
        retractall(goal(medical_check)));

    ((goal(have_fun),  location(Id), open_hours_place(Id,_,C), hour(H), C == H)  ->
        retractall(goal(wear_mask)));

    (goal(remove_mask), wearing_mask(false) ->
        retractall(goal(remove_mask)));
    true.

move(NodeId, Action, Arguments):-
    social_distancing(SocialDistancing),
    Action = move,
    Arguments = [NodeId, SocialDistancing].

work(Action, Arguments):-
    Action = work,
    Arguments = [].

wear_mask(Action, Arguments):-
    Action = wear_mask,
    Arguments = [].

remove_mask(Action, Arguments):-
    Action = remove_mask,
    Arguments = [].

update_location(Location):-
    retractall(location(_)),
    retractall(goal(move, Location)),
    assert(location(Location)).

update_wearing_mask(WearingMask):-
    retractall(wearing_mask(_)),
    WearingMask -> retractall(goal(wear_mask)); retractall(goal(remove_mask)).
    
behavioral_step(Action, Arguments):-
    % scheduling
    check_schedule(),
    
    % check archieved goals
    check_goals(),
    % (preconditions) - (actions)

    (goal(work), work_place(WorkId, _), location(WorkId)->
    work(Action, Arguments));

    (goal(medical_check)-> Action = medical_check);

    (goal(move, NodeId), not(location(NodeId))->
    (move(NodeId, Action, Arguments)));

    (goal(wear_mask), mask_necessity(true), location(NodeId), mask_requirement(NodeId, true), wearing_mask(false)->
        wear_mask(Action, Arguments));

    (goal(remove_mask), wearing_mask(true)->
        remove_mask(Action, Arguments)).


feedback(Location, WearingMask):-
    (not(location(Location))->
        update_location(Location));
    (not(wearing_mask(WearingMask))->
        update_wearing_mask(WearingMask)).
    % check archieved goals
    
%---------------------------- Local Plans --------------------------------------------------------

% Rules


remove_goals():-
    retractall(goal(_)),
    retractall(goal(_, _)).

check_schedule():-
    hour(H),
    min(M),
    (schedule(remove, GoalType, H, M) ->
        retractall(goal(GoalType)), retractall(schedule(remove, GoalType, H, M))),
    (schedule(add, GoalType, H, M) ->
        assert(goal(GoalType)), retractall(schedule(add, GoalType, H, M)));
    (schedule(add, GoalType, Param, H, M) ->
        assert(goal(GoalType, Param)), retractall(schedule(add, GoalType, H, M)));
    true.

remove_schedule(GoalType, H, M):-
    schedule(remove, GoalType, H, M),
    retractall(schedule(remove, _, H, M)),
    assert(schedule(remove, GoalType, H, M)).

goal_move(TagetNode):-
    retractall(goal(move, _)),
    assert(goal(move, TagetNode)).
    

get_to_work(WorkId):-
    goal_move(WorkId),
    location(WorkId).

get_to_public_place(Id):-
    goal_move(Id),
    location(Id).

get_to_hospital(Hospital):-
    goal_move(Hospital),
    location(Hospital).

work(WorkId):-
    hour(H),
    open_hours_place(WorkId, _, C),
    (not(goal(work))->
        assert(goal(work)); true),
    H >= C.

medical_check(HospitalId):-
    hour(H),
    open_hours_place(HospitalId, _, C),
    (not(goal(medical_check))->
        assert(goal(medical_check)); true),
    H >= C.

have_fun(Id):-
    hour(H),
    open_hours_place(Id, _, C),
    (not(goal(have_fun))->
        assert(goal(have_fun)); true),
    H >= C.


go_home(HomeId):-
    goal_move(HomeId).

work_day_routine(WorkId, HomeId):-
    get_to_work(WorkId),
    work(WorkId),
    go_home(HomeId).

hospital_rutine(HospitalId, HomeId):-
    get_to_hospital(HospitalId),
    medical_check(HospitalId),
    go_home(HomeId).

go_public_place_rutine(Id, HomeId):-
    get_to_public_place(Id),
    have_fun(Id),
    go_home(HomeId).

hospital_overrun(_, false).

planification_step():-
    remove_goals(),
    home(HomeId),
    work_place(WorkId, _),
    (work_is_open(WorkId), too_sick(false) -> work_day_routine(WorkId, HomeId));
    ((too_sick(true), hospital(Id,_), open_place(Id, true), hospital_overrun(Id, false))-> hospital_rutine(Id, HomeId));
    ((public_space(Id, _),open_place(Id, true)) -> go_public_place_rutine(Id, HomeId)).


% Facts for testing purposes:
% hour(16).
% min(0).
% week_day(monday).
% home(55).
% too_sick(false).
% work_place(66, -1).
% open_hours_place(66, 8, 18).
% open_place(66, true).
% hospital(5, -1).
% open_hours_place(5, 8, 20).


%---------------------------- Cooperation Knowledge -----------------------------------------------

% % Enviar un mensaje
% recibe_message(SenderId, ReceiverId, Message) :-
%     retractall(message(SenderId, Message)),
%     assert(message(SenderId, Message)).

% % Coordinar acciones
% coordinate_action(AgentId, OtherAgentId, PlanId) :-
%     send_message(AgentId, OtherAgentId, coordinate_action),
%     receive_message(AgentId, OtherAgentId, coordinate_action).

cooperation_step().


%--------------------------- Auxiliary Methods -----------------------------------------


:-dynamic(maintain_distancing/1).
:-dynamic(mask_knowledge/1).
:-dynamic(need_isolation/1).
:-dynamic(use_protection_equipment/1).
:-dynamic(stay_at_home/1).
:-dynamic(my_symptoms/1).
:-dynamic(month_day/1).
:-dynamic(use_personal_mask/1).
:-dynamic(hospital/2).
:-dynamic(open_place/2).
:-dynamic(public_space/2).
:-dynamic(open_hours_place/3).

:-dynamic(goal/2).
:-dynamic(goal/1).
:-dynamic(wearing_mask/1).
:-dynamic(mask_requirement/2).
:-dynamic(mask_necessity/1).
:-dynamic(location/1).
:-dynamic(home/1).
:-dynamic(work_place/2).
:-dynamic(week_day/1).
:-dynamic(quarantined/1).
:-dynamic(too_sick/1).
:-dynamic(schedule/4).
:-dynamic(schedule/5).
:-dynamic(min/1).
:-dynamic(hour/1).