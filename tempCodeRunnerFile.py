    nuevo_contenido = f"""(define (problem CAJAS-4)
        (:domain CAJAS)
        (:objects arandela clavo tornillo tuerca)
        (:INIT 
            {condiciones_iniciales[0]}
            {condiciones_iniciales[1]}
            {condiciones_iniciales[2]}
            {condiciones_iniciales[3]}
            {condiciones_iniciales[4]}
        )
        (:goal (AND 
            {estado_objetivo[0]}
            {estado_objetivo[1]}
            {estado_objetivo[2]}
        ))
    )"""