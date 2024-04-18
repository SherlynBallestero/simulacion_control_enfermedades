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
sleeping(true).

% goal(move, 1).
% hour(16).
position(5).

my_symptoms([tos]).
use_personal_mask(false).
open_hours_place(_,7, 16).
open_place(_, true).
mask_requirement(_,true).
mask_necessity(true).
public_transportation_working(_, true).
public_transportation_schedule(2, [1,6,4,7,5,8,78,9,37]).
hospital_acepting_patients(_, true).
disease_symptoms([tos]).
hospital(5,_).
public_space(77, _).
public_space(44, _).
isolation_center(45, _).
% work_place(66).
% home(55).

% hospitl, block, public_space, work_space, buss
add_map_node(Id, Address, CapacityStatus, NodeType):-
    (NodeType = hospital, add_hospital(Id, Address), retractall(place_status(Id, _)), assert(place_status(Id, CapacityStatus)));
    (NodeType = public_space, add_public_space(Id, Address), retractall(place_status(Id, _)), assert(place_status(Id, CapacityStatus)));
    (NodeType = block, add_public_space(Id, Address), retractall(place_status(Id, _)), assert(place_status(Id, CapacityStatus))).

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

add_work_place(Node):-
    retractall(work_place(_)),
    retractall(open_place(Node, true)),
    assert(open_place(Node, true)),
    assert(work_place(Node)).

add_open_place(Node, Bool):-
    retractall(open_place(Node,_)),
    assert(open_place(Node, Bool)).


add_open_hours_place(Node, Initial, Final):-
    retractall(open_hours_place(Node, Initial, Final)),
    assert(open_hours_place(Node,Initial,Final)).

add_date(WeekDayK, MonthDayK, HourK, MinK):-
    retractall(week_day(_)),
    retractall(month_day(_)),
    retractall(min(_)),
    retractall(hour(_)),
    asserta(week_day(WeekDayK)),
    asserta(month_day(MonthDayK)),
    assert(hour(HourK)),
    asserta(min(MinK)).

add_symptom(Symptom):-
    my_symptoms(S),
    Symptom_list_result = [Symptom| S],
    retractall(my_symptoms(_)),
    asserta(my_symptoms(Symptom_list_result)).
    
add_hospital(HospitalId, Address):-
    retractall(hospital(HospitalId, _)),
    asserta(hospital(HospitalId, Address)).
    
add_disease_symptoms(S):-
    assert(disease_symptoms(S)).

add_if_is_medical_personal(Bool):-
    assert(is_medical_personal(_)),
    assert(is_medical_personal(Bool)).

add_mask_necessity(Bool):-
    retractall(mask_knowledge(_)),
    assert(mask_knowledge(Bool)).

add_place_to_use_mask(Place, Bool):-
    retractall(mask_requirement(Place,_)),
    assert(mask_requirement(Place, Bool)).


%---------------------------- Patterns of Behaviour -----------------------------------------------

move(move, Node):-
    retractall(goal(move, Node)),
    open_place(Node, true),
    (take_bus(Node, _, _); walk(_, Node)).
    

sleep(sleep):-
    hour(Hour),
    Hour == 22,
    retractall(sleeping(_)),
    assert(sleeping(true)).

sleep_now(sleep):-
    retractall(sleeping(_)),
    assert(sleeping(true)).

wake_up(wake_up):-
    hour(Hour),
    Hour == 7,
    retractall(sleeping(_)),
    assert(sleeping(false)).

take_bus(NodeIdDest, move, Id):-
    public_transportation_working(Id, true),
    public_transportation_schedule(Id, AddrList),
    member(NodeIdDest, AddrList).


walk(move, _).

wear_mask(use_mask, Node):-
    not(use_personal_mask(true)),
    mask_requirement(Node,true),
    mask_necessity(true),
    retractall(use_personal_mask(false)),
    assert(use_personal_mask(true)).

remove_mask(remove_mask, Node):-
    not(use_personal_mask(false)),
    mask_requirement(Node,false),
    mask_necessity(false),
    retractall(use_personal_mask(_)),
    assert(use_personal_mask(false)).
    
search_medical_attention(FunctionName, Id):-
    FunctionName = move,
    hospital(Id, _),
    hospital_acepting_patients(Id, true).

detect_symptoms(FunctionName, Args) :-
    my_symptoms(Symptoms),
    disease_symptoms(DiseaseSymptoms),
    intersection(Symptoms, DiseaseSymptoms, CommonSymptoms),
    CommonSymptoms \= [],
    search_medical_attention(FunctionName, Args).


step( Action, Arguments):-
    (wear_mask(Action, Arguments); remove_mask(Action, Arguments));
    (goal(move, NodeIdDest),move(_, NodeIdDest));
    % go_home_after_work(Action, Arguments);
    (goal(go_home_after_work, F),hour(H), H == F, go_home_after_work(Action, Arguments));
    (goal(go_home, F),hour(H), H == F, go_home_after_recreation(Action, Arguments));
    (wake_up(Action); sleep(Action));
    (sleeping(true), Action = sleeping).

    % (goal(move, NodeIdDest),take_bus(NodeIdDest, Action, Arguments), retractall(goal(move, NodeIdDest)));
    % (goal(go_home_after_work, F),hour(H), H == F, go_home_after_work(Action, Arguments), retractall(goal(go_home_after_work, F)));

    % detect_symptoms(Action, Arguments).
    

    
%---------------------------- Local Plans --------------------------------------------------------

% Facts
use_protection_equipment(false).
stay_at_home(false).
maintain_distancing(false).
need_isolation(false).

% Rules
step_rutine():-
    (work_rutine();non_working_day_routine());
    quarantine_routine().

go_to_work(move, X):-
    work_place(X),
    open_place(X, true),
    hour(H),
    open_hours_place(X,I,_),
    H == I.

go_home_after_work(move, Y):-
    home(Y),
    work_place(X),
    open_place(X, true),
    hour(H),
    open_hours_place(X,_,F),
    H == F,
    retractall(goal(go_home_after_work, Y)).

go_home_after_recreation(move, Y):-
    home(Y),
    position(X),
    open_place(X, true),
    hour(H),
    open_hours_place(X,_,F),
    H == F,
    retractall(goal(go_home, Y)).


work_rutine():-
    go_to_work(Action, NodeWork),
    (take_bus(NodeWork, Action, _); walk(Action, NodeWork)),
    open_hours_place(NodeWork,_,F),
    asserta(goal(go_home_after_work, F)).

non_working_day_routine():-
    open_place(Id, true),
    public_space(Id, _),
    open_hours_place(Id, _, F),
    % asserta(goal(move, Id)),
    asserta(goal(go_home, F)).
    
quarantine_routine():-
    use_mask_k(),
    detect_symptoms(_,_),
    isolation_center(Id,_),
    asserta(goal(move, Id)).


% schedule_manager():-
%     hour(H),
%     min(M),
%     schedule(NewGoal, H, M),
%     assert(goal(NewGoal)).

use_mask_k():-
    retractall(mask_necessity(_)),
    asserta(mask_necessity(true)).

remove_mask_k():-
    retractall(mask_necessity(_)),
    asserta(mask_necessity(false)).

establish_need_isolation():-
    retractall(need_isolation(_)),
    asserta(need_isolation(true)).

remove_need_isolation():-
    retractall(need_isolation(_)),
    asserta(need_isolation(false)).

establish_use_protection_equipment():-
    retractall(use_protection_equipment(_)),
    asserta(use_protection_equipment(true)).

establish_stay_at_home():-
    retractall(stay_at_home(_)),
    asserta(stay_at_home(true)).

leave_home():-
    retractall(stay_at_home(_)),
    asserta(stay_at_home(false)).

establish_distancing():-
    retractall(maintain_distancing(_)),
    asserta(maintain_distancing(true)).

remove_distancing():-
    retractall(maintain_distancing(_)),
    asserta(maintain_distancing(false)).

implement_isolation_measures() :-
    establish_need_isolation(),
    establish_use_protection_equipment(),
    establish_stay_at_home().

%---------------------------- Cooperation Knowledge -----------------------------------------------

risk_contacts_detected( [_]).
send_info(_, _).

inform_contacts(_, []).
inform_contacts(Info, [A|[Contacts]]):-
    send_info(Info, A),
    inform_contacts(Info, Contacts).

track_risk_contacts() :-
    risk_contacts_detected(Contacts),
    inform_contacts(infected_agent, Contacts).

%--------------------------- Auxiliary Methods -----------------------------------------

intersection([], _, []).
intersection([H|T], L, [H|R]) :-
    member(H, L),
    intersection(T, L, R).
intersection([H|T], L, R) :-
    \+ member(H, L),
    intersection(T, L, R).

:-dynamic(maintain_distancing/1).
:-dynamic(mask_knowledge/1).
:-dynamic(need_isolation/1).
:-dynamic(use_protection_equipment/1).
:-dynamic(stay_at_home/1).
:-dynamic(my_symptoms/1).
:-dynamic(hour/1).
:-dynamic(week_day/1).
:-dynamic(month_day/1).
:-dynamic(min/1).
:-dynamic(use_personal_mask/1).
:-dynamic(home/1).
:-dynamic(work_place/1).
:-dynamic(goal/2).
:-dynamic(hospital/2).
:-dynamic(open_place/2).
:-dynamic(mask_necessity/1).
:-dynamic(public_space/2).
:-dynamic(open_hours_place/3).
:-dynamic(sleeping/1).