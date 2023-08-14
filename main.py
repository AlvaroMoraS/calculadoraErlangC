from math import factorial, exp, pow   

"""
Para usar esta calculadora, primero necesitarás tener los siguientes datos:

1) Cantidad de llamados que ingresan en un intervalo de tiempo (se recomienda cada 30 minutos; por ejemplo: 180 llamados).
2) Cantidad de segundos en los que ingresan la cantidad de llamados del punto anterior (por ejemplo: 1800 segundos, que equivalen a 30 minutos).
3) Tiempo promedio de duración de una llamada (en segundos. Por ejemplo: 180 segundos por llamada).
4) Nivel de servicio requerido (en porcentaje. Por ejemplo: 80%).
5) Segundos de respuesta objetivo (en segundos. Por ejemplo: 20 segundos).
"""


def calculaLambda(llamadasEnIntervalo:int, segundosIntervalo:int):
    lambda1 = llamadasEnIntervalo/segundosIntervalo
    return lambda1

    


def calculaIntensidadDelTrafico(llamadasEnIntervalo:int, segundosIntervalo:int, duracionLlamadaEnSegundos:int):
    lambda1 = calculaLambda(llamadasEnIntervalo, segundosIntervalo)
    intensidadDelTrafico = lambda1 * duracionLlamadaEnSegundos
    return intensidadDelTrafico



def calculaOcupacionAgente(llamadasEnIntervalo:int, segundosIntervalo:int, duracionLlamadaEnSegundos:int, numeroAgentes:int):
    intensidadDelTrafico = calculaIntensidadDelTrafico(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos)
    ocupacionAgente = intensidadDelTrafico/numeroAgentes
    return ocupacionAgente


def calculaErlangC(llamadasEnIntervalo:int, segundosIntervalo:int, duracionLlamadaEnSegundos:int, numeroAgentes:int):
    intensidadDelTrafico = calculaIntensidadDelTrafico(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos)
    ocupacionAgente = calculaOcupacionAgente(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos, numeroAgentes)

    numerador = pow(intensidadDelTrafico,numeroAgentes)/factorial(numeroAgentes)
    denominadorP1 = (1 - ocupacionAgente)

    sumatoria = 0

    for k in range(0,(numeroAgentes-1)):
        sumatoria += ((pow(intensidadDelTrafico,k)/factorial(k)))

    denominadorP2 = (sumatoria * denominadorP1) + numerador
    erlangC = numerador/denominadorP2
    return erlangC

def calculaVelocidadMediaDeRespuesta(llamadasEnIntervalo:int, segundosIntervalo:int, duracionLlamadaEnSegundos:int, numeroAgentes:int):
    erlangC = calculaErlangC(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos, numeroAgentes)
    ocupacionAgente = calculaOcupacionAgente(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos, numeroAgentes)
  
    numerador = (erlangC*duracionLlamadaEnSegundos)
    denominador = (numeroAgentes * (1-ocupacionAgente))
    velocidadMediaDeRespuesta = numerador / denominador
    return velocidadMediaDeRespuesta


def calculaNivelDeServicio(llamadasEnIntervalo:int, segundosIntervalo:int, duracionLlamadaEnSegundos:int, numeroAgentes:int, segundosObjetivo:int):

  intensidadDelTrafico = calculaIntensidadDelTrafico(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos)
  erlangC = calculaErlangC(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos, numeroAgentes)
  nivelDeServicio = 1 - (erlangC*exp((-(numeroAgentes-intensidadDelTrafico))*(segundosObjetivo/duracionLlamadaEnSegundos)))

  return nivelDeServicio


def calculaAgentesNecesarios(llamadasEnIntervalo:int, segundosIntervalo:int, duracionLlamadaEnSegundos:int, segundosObjetivo:int, nivelDeServicioObjetivo:float):
  slaAlcanzado= 0
  numAgentesCalculado=1

  while slaAlcanzado < nivelDeServicioObjetivo:
    slaAlcanzado = calculaNivelDeServicio(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos, numAgentesCalculado, segundosObjetivo)
    numAgentesCalculado += 1

  agentesNecesarios = numAgentesCalculado-1
  return agentesNecesarios


def calcularTodosLosIndicadores(llamadasEnIntervalo:int, segundosIntervalo:int, duracionLlamadaEnSegundos:int, segundosObjetivo:int, nivelDeServicioObjetivo:float):
   intensidadDelTrafico = calculaIntensidadDelTrafico(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos)
   agentesNecesarios = calculaAgentesNecesarios(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos, segundosObjetivo, nivelDeServicioObjetivo)
   ocupacionAgente = calculaOcupacionAgente(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos, agentesNecesarios)
   erlangC = calculaErlangC(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos, agentesNecesarios)
   nivelDeServicio = calculaNivelDeServicio(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos, agentesNecesarios, segundosObjetivo)
   velocidadMediaDeRespuesta = calculaVelocidadMediaDeRespuesta(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos, agentesNecesarios)

   return agentesNecesarios, nivelDeServicio, ocupacionAgente, intensidadDelTrafico, erlangC, velocidadMediaDeRespuesta



def main():
   llamadasEnIntervalo = 231
   segundosIntervalo= 1800
   duracionLlamadaEnSegundos= 243
   segundosObjetivo= 20
   nivelDeServicioObjetivo= 0.8
   
   agentesNecesarios, nivelDeServicio, ocupacionAgente, intensidadDelTrafico, erlangC, velocidadMediaDeRespuesta = calcularTodosLosIndicadores(llamadasEnIntervalo, segundosIntervalo, duracionLlamadaEnSegundos, segundosObjetivo, nivelDeServicioObjetivo)

   print('=' * 40)
   print(f'Llamadas por intervalo: {llamadasEnIntervalo}')
   print(f'Segundos del intervalo: {segundosIntervalo}')
   print(f'Duración promedio de cada llamada: {duracionLlamadaEnSegundos}')
   print(f'Segundos objetivo: {segundosObjetivo}')
   print(f'Nivel de Servicio objetivo: {nivelDeServicioObjetivo}') 
   print('=' * 15 + 'RESULTADO' + '=' * 16)
   
   print(f'Número de agentes necesarios: {agentesNecesarios}')
   print(f'Nivel de Servicio: {round(nivelDeServicio,4)*100}%')
   print(f'Ocupación agentes: {round(ocupacionAgente,4)*100}%')
   print(f'Intensidad del tráfico: {intensidadDelTrafico}')
   print(f'Probabilidad de esperar: {round(erlangC,4)*100}%')
   print(f'Velocidad de respuesta promedio: {round(velocidadMediaDeRespuesta,2)} segundos')
   

if __name__ == '__main__':
   main()

