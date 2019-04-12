#!/bin/sh

function test_ambermini(){
    reduce -Version
    antechamber -h
    tleap -h
    sqm -h
    # acdoctor -h
    # charmmgen -h
    # match_atomname -h
    am1bcc -h
    atomtype -h
    bondtype -h
    espgen -h
    parmchk2 -h
    prepgen -h
    residuegen -h
    respgen -h
}

test_ambermini
