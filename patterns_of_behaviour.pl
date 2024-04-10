% Define los hechos
% name(cambiar_ubicacion, '').
capacity_place(place1,1, 100).
capacity_place(place3,2, 300).
work(move, 1).

action(go_to_work).
% behavior_pattern(Goal).

% global_behavior(Goal, Args, Action):-
%     behavior_move(Goal, Args1, Action),
%     behavior_pattern(CurrentNode, Capacity1, Action).

behavior_move(move, Args1, move):-
    work(Go_to_work, Args), Args1 is Args .
    

behavior_pattern(CurrentNode, Id, move):-
    % Verifica la capacidad del nodo actual
    capacity_place(CurrentNode,Id1, Capacity),
    Capacity > 100,
    Id = [Id1].

:-dynamic capacity_place/3.

