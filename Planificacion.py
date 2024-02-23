import subprocess


class Planificador:
    def __init__(self, dominio_file, problema_file):
        self.dominio_file = dominio_file
        self.problema_file = problema_file

    def generar_condiciones_iniciales(self, caja):
        condiciones_iniciales = []
        condiciones_iniciales.append(f"(DESPEJADA {caja[0]})")
        condiciones_iniciales.append(f"(EN_MESA {caja[3]})")
        for i in range(len(caja) - 1):
            condiciones_iniciales.append(f"(SOBRE {caja[i]} {caja[i+1]})")
        condiciones_iniciales.append("(MANO_LIBRE)")

        return condiciones_iniciales

    def generar_estado_objetivo(self, caja):
        estado_objetivo = []
        for i in range(len(caja) - 1):
            estado_objetivo.append(f"(SOBRE {caja[i]} {caja[i+1]})")

        return estado_objetivo

    def generar_archivo_problema(self, caja, objetivo):
        # Generar las condiciones iniciales y el estado objetivo
        condiciones_iniciales = self.generar_condiciones_iniciales(caja)
        estado_objetivo = self.generar_estado_objetivo(objetivo)

        # Generar el nuevo contenido del archivo Problema.pddl
        nuevo_contenido = f"""(define 
    (problem CAJAS-4)
    (:domain CAJAS)
    (:objects arandela clavo tornillo tuerca)
    (:INIT 
        {condiciones_iniciales[0]}
        {condiciones_iniciales[1]}
        {condiciones_iniciales[2]}
        {condiciones_iniciales[3]}
        {condiciones_iniciales[4]}
        {condiciones_iniciales[5]}
    )
    (:goal (AND 
        {estado_objetivo[0]}
        {estado_objetivo[1]}
        {estado_objetivo[2]}
    ))
)"""

        # Sobreescribir el archivo Problema.pddl con el nuevo contenido
        with open(self.problema_file, 'w') as file:
            file.write(nuevo_contenido)

    def ejecutar_planificacion(self):
        comando = f'code --goto "{self.dominio_file}" && code --goto "{self.problema_file}" --wait --reuse-window'
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        print(resultado.stdout)
         # Verificar si se encontró un plan en la salida capturada
        exito = "Planner found 0 plan" not in resultado.stdout

        return exito



if __name__ == '__main__':
    # Rutas de los archivos de dominio y problema
    dominio_file = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\EXÁMEN FINAL\Dominio.pddl'
    problema_file = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\EXÁMEN FINAL\Problema.pddl'

    caja = ['arandela', 'clavo', 'tornillo', 'tuerca']
    objetivo = ['tornillo', 'tuerca', 'arandela', 'clavo']

    problema_cajas = Planificador(dominio_file, problema_file)
    problema_cajas.generar_archivo_problema(caja, objetivo)
    exito = problema_cajas.ejecutar_planificacion()
    if exito:
        print('Se encontró un plan')
    else:
            print('No se encontró un plan')

    print('Fin del programa')

