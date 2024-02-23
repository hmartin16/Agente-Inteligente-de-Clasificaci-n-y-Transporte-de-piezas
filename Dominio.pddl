(define (domain CAJAS)
  (:requirements :strips)
  (:predicates (sobre ?x ?y)
           (en_mesa ?x)
           (despejada ?x)
           (mano_libre)
           (sosteniendo ?x)
           )

  (:action tomar
         :parameters (?x)
         :precondition (and (despejada ?x) (en_mesa ?x) (mano_libre))
         :effect
         (and (not (en_mesa ?x))
           (not (despejada ?x))
           (not (mano_libre))
           (sosteniendo ?x)))

  (:action soltar
         :parameters (?x)
         :precondition (sosteniendo ?x)
         :effect
         (and (not (sosteniendo ?x))
           (despejada ?x)
           (mano_libre)
           (en_mesa ?x)))
  (:action apilar
         :parameters (?x ?y)
         :precondition (and (sosteniendo ?x) (despejada ?y))
         :effect
         (and (not (sosteniendo ?x))
           (not (despejada ?y))
           (despejada ?x)
           (mano_libre)
           (sobre ?x ?y)))
  (:action desapilar
         :parameters (?x ?y)
         :precondition (and (sobre ?x ?y) (despejada ?x) (mano_libre))
         :effect
         (and (sosteniendo ?x)
           (despejada ?y)
           (not (despejada ?x))
           (not (mano_libre))
           (not (sobre ?x ?y)))))