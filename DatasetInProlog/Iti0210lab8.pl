
man(marcus).
man(jaan).
man(francesco).

pompej_civilian(francesco).
pompej_civilian(marcus).

birth_date(enrico, 1999).
birth_date(marcus, 40).
birth_date(jaan, 1977).
birth_date(francesco, 1989).

mortal(man).

eradication(pompej_civilian, 79).
lifetime(mortal, 150).

is_mortal(Name) :- man(Name), mortal(man).

alive(Year, Human) :- not(is_mortal(Human)), birth_date(Human, Birth), Year >= Birth. % is immortal

alive(Year, Human) :- is_mortal(Human), mortal(man), lifetime(mortal, Mortality), birth_date(Human, Birth), Year - Birth =< Mortality, Year >= Birth,
                      (
                            (pompej_civilian(Human), eradication(pompej_civilian, Eradication_year),
                                (
                                    (Birth =< Eradication_year, Eradication_year > Year)
                                        ;
                                    (Birth >  Eradication_year)
                                )
                                    ;
                                (not(pompej_civilian(Human)))
                            )
                      ).

%   ?- alive(2019, marcus).
%   false. # eradication event and too old
%
%   ?- alive(79, marcus).
%   false. # eradication event
%
%   ?- alive(78, marcus).
%   true .
%
%   ?- alive(40, marcus).
%   true .
%
%   ?- alive(39, marcus).
%   false. # not born yet
%
%   ?- alive(2019, jaan).
%   true.
%
%   ?- alive(1977, jaan).
%   true.
%
%   ?- alive(1976, jaan).
%   false. # not born yet
%
%   ?- alive(2019, francesco).
%   true .
%
%   ?- alive(1989, francesco).
%   true
%
%   ?- alive(1988, francesco).
%   false. # not born yet
%
%   ?- alive(3019, enrico).
%   true . # I'm not mortal
%
%   ?- alive(2019, enrico).
%   true .
%
%   ?- alive(1999, enrico).
%   true
%
%   ?- alive(1998, enrico).
%   false. # not born yet
