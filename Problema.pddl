(define 
    (problem CAJAS-4)
    (:domain CAJAS)
    (:objects arandela clavo tornillo tuerca)
    (:INIT 
        (DESPEJADA tuerca)
        (EN_MESA clavo)
        (SOBRE tuerca arandela)
        (SOBRE arandela tornillo)
        (SOBRE tornillo clavo)
        (MANO_LIBRE)
    )
    (:goal (AND 
        (SOBRE tuerca tornillo)
        (SOBRE tornillo arandela)
        (SOBRE arandela clavo)
    ))
)