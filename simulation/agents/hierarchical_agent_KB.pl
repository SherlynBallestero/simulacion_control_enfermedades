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
% sleeping(true).

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

% hospitl, block, public_space, work_space, buss
% Perception and body related knowledge predicates
initialize_k():-
    assert(too_sick(false)).

add_node_info(Id, Address, CapacityStatus, NodeType):-%TODO: see if this is necesary and if it works
    retractall(node(Id, _, _, _)),
    retractall(),
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

work_is_open(WorkId):-
    week_day(WeekDay),
    write("Day of the week:"),writeln(WeekDay),
    not(week_day(saturday)),
    not(week_day(sunday)),
    hour(H),
    write("Hour:"), writeln(H),
    write("WorkId:"), writeln(WorkId),
    open_hours_place(WorkId,I,F),
    write("Opening Hour:"), writeln(I),
    write("Closing Hour:"), writeln(F),
    write("Is Open:"), writeln(open_place(WorkId, true)),
    open_place(WorkId, true),
    H >= I,
    H =< F.
%---------------------------- Patterns of Behaviour -----------------------------------------------

check_goals():-
    (goal(move, Id), location(Id) ->
        retractall(goal(move, Id)));
    (goal(wear_mask), wearing_mask(true) ->
        retractall(goal(wear_mask)));
    (goal(remove_mask), wearing_mask(false) ->
        retractall(goal(remove_mask)));
    true.

move(NodeId, Action, Arguments):-
    Action = move,
    Arguments = [NodeId].

work(Action, Arguments):-
    Action = work,
    Arguments = [].

sleep(Action, Arguments):-
    Action = sleep,
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

% move(move, Node):-
%     retractall(goal(move, Node)),
%     open_place(Node, true),
%     (take_bus(Node, _, _); walk(_, Node)).
    

% sleep(sleep):-
%     hour(Hour),
%     Hour == 22,
%     retractall(sleeping(_)),
%     assert(sleeping(true)).

% sleep_now(sleep):-
%     retractall(sleeping(_)),
%     assert(sleeping(true)).

% wake_up(wake_up):-
%     hour(Hour),
%     Hour == 7,
%     retractall(sleeping(_)),
%     assert(sleeping(false)).

% take_bus(NodeIdDest, move, Id):-
%     public_transportation_working(Id, true),
%     public_transportation_schedule(Id, AddrList),
%     member(NodeIdDest, AddrList).


% walk(move, _).

% wear_mask(use_mask, Node):-
%     not(use_personal_mask(true)),
%     mask_requirement(Node,true),
%     mask_necessity(true),
%     retractall(use_personal_mask(false)),
%     assert(use_personal_mask(true)).

% remove_mask(remove_mask, Node):-
%     not(use_personal_mask(false)),
%     mask_requirement(Node,false),
%     mask_necessity(false),
%     retractall(use_personal_mask(_)),
%     assert(use_personal_mask(false)).
    
% search_medical_attention(FunctionName, Id):-
%     FunctionName = move,
%     hospital(Id, _),
%     hospital_acepting_patients(Id, true).

% detect_symptoms(FunctionName, Args) :-
%     my_symptoms(Symptoms),
%     disease_symptoms(DiseaseSymptoms),
%     intersection(Symptoms, DiseaseSymptoms, CommonSymptoms),
%     CommonSymptoms \= [],
%     search_medical_attention(FunctionName, Args).


% step( Action, Arguments):-
%     Action = move,
%     Arguments = 1.
    % check_goals(),
    % (wear_mask(Action, Arguments); remove_mask(Action, Arguments));
    % (goal(move, NodeIdDest),move(_, NodeIdDest)).
    % go_home_after_work(Action, Arguments);
    % (goal(go_home_after_work, F),hour(H), H == F, go_home_after_work(Action, Arguments));
    % (goal(go_home, F),hour(H), H == F, go_home_after_recreation(Action, Arguments));
    % (wake_up(Action); sleep(Action));
    % (sleeping(true), Action = sleeping).
    % detect_symptoms(Action, Arguments).
    
behavioral_step(Action, Arguments):-
    % scheduling
    check_schedule(),
    
    % check archieved goals
    check_goals(),

    % (preconditions) - (actions)
    (goal(move, NodeId), not(location(NodeId))->
        move(NodeId, Action, Arguments));
    (goal(sleeping), home(HomeId), location(HomeId)->
        sleep(Action, Arguments));
    (goal(work), work_place(WorkId, _), location(WorkId)->
        work(Action, Arguments));
    (goal(wear_mask), mask_necessity(true), location(NodeId), mask_requirement(NodeId, true), wearing_mask(false)->
        wear_mask(Action, Arguments));
    (goal(remove_mask), wearing_mask(true)->
        remove_mask(Action, Arguments)).

behavioral_feedback(Location, WearingMask):-
    (not(location(Location))->
        update_location(Location));
    (not(wearing_mask(WearingMask))->
        update_wearing_mask(WearingMask)).
    % check archieved goals
    
%---------------------------- Local Plans --------------------------------------------------------

% Rules

goal_move(TagetNode):-
    retractall(goal(move, _)),
    assert(goal(move, TagetNode)).

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
    % print("Remove Task: "),%TODO: Remove After Testing
    % print(GoalType),
    % print(H),
    % print(M),
    % print("Already Scheduled"),
    retractall(schedule(remove, _, H, M)),
    assert(schedule(remove, GoalType, H, M)).

get_to_work(WorkId):-
    goal_move(WorkId),
    location(WorkId).

work():-
    not(goal(work)),
    assert(goal(work)).

go_home(HomeId):-
    goal_move(HomeId).

work_day_routine(WorkId, HomeId):-
    get_to_work(WorkId),
    work(),
    go_home(HomeId).

free_day_routine():-
    true.

sleep_time():-
    hour(H),
    H >= 20,
    H =< 6.

planification_step():-
    remove_goals(),
    home(HomeId),
    work_place(WorkId, _),
    write("HomeId:"), writeln(HomeId),
    write("WorkId:"), writeln(WorkId),
    too_sick(Boolean), write("Is To Sick:"), writeln(Boolean),
    (work_is_open(WorkId), too_sick(false) ->
        work_day_routine(WorkId, HomeId);
        (
            writeln("Entering on else"), 
            free_day_routine())).
    % (sleep_time() ->
    %     assert(goal(sleeping)), remove_schedule(sleeping, 6, 0)).%TODO: change this to sleep at home

% Facts for testing purposes:
% hour(16).
% min(0).
% week_day(monday).
% home(55).
% too_sick(false).
% work_place(66).
% open_hours_place(66, 8, 18).
% open_place(66, true).
% hospital(5, 77).
% open_hours_place(5, 8, 20).
% open_place(5, true).
% public_space(77, 44).


%---------------------------- Cooperation Knowledge -----------------------------------------------

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
:-dynamic(sleeping/1).

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