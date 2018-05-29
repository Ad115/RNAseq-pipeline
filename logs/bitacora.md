Bitácora del proyecto
=====================

About the project
-----------------
We are trying to detect if there are changes in the expression of
long non-coding RNAs between the left and right hemisphere of a mouse's
brain (telencephalon). For this, 3 samples where taken and sequenced using
RNAseq. For more information about RNAseq, see: 
https://galaxyproject.org/tutorials/rb_rnaseq/

For more documentation on the scripts, look at the scripts themselves.


## Mayo

### Inicios de mayo

*Paso 1: Mapeo de datos*

- Se comenzó a trabajar sobre los datos crudos de RNAseq.

- Debido a la gran cantidad de archivos y datos, se decidió 
  realizar scripts para asegurar la reproducibilidad de cada paso.

- Se eligió realizar los scripts en Xonsh (un híbrido Bash-Python)
  por conveniencia y facilidad de uso, además de ser fácil de instalar.

- Se inició el proceso de mapeo y se dejó corriendo por dos semanas, del 
  9 al 11 de Mayo. Se encontró después que el script contenía un bug y 
  los mapeos no se hicieron.

- Debido a lo complicado que fué analizar el archivo y los procesos para
  encontrar el bug, se siguieron los consejos de Villay y se comenzó a 
  realizar una documentación exahustiva de los scripts que se utilizan.

- Se corrigió y se documentó  el script y se arrancó el proceso. Al 
  realizar los mapeos de forma secuencial, se observó que el tiempo 
  requerido para terminar  sería muy largo, por lo que se decidió matar 
  el proceso y realizar el script en SGE para lanzar múltiples procesos 
  en paralelo.

- Se realizó el script en paralelo con un Job Array de SGE y se arrancó,
  aparentemente todo bien.

- Luis Aguilar notó que los jobs que había mandado a ejecutar consumían 
  recursos de cómputo que no les correspondían y terminó los procesos.
  Posteriormente observamos que esto se debía a que el job array ejecuta
  un proceso por core, pero los procesos que había mandado requerían de 8 
  cores y eso es lo que utilizaban, así entonces el sistema de colas detectaba 
  una carga grande de trabajo y no permitía que se encolaran trabajos de otros
  usuarios.

### 29 de Mayo
- Se platicó del problema con Luis y se agregaron las lineas:
	#$ -pe openmp {CORES}
	export OMP_NUM_THREADS={CORES}
  al script que enviaba el job. Con lo que se debería resolver el problema.

- Se editó el script para verificar si el archivo de salida existe antes de 
  ejecutar el comando, para evitar duplicar trabajo.

- Se mandó a ejecutar el job array.

- El día de hoy se completó el proceso de mapeo de los datos crudos,
  pero debido a que se continuaron procesos que fueron trminados prematuramente,
  se observó que al menos 55 de 281 jobs no concluyeron satisfactoriamente y por
  lo tanto, el archivo de salida está corrupto. Por otra parte, al intentar detectar 
  qué archivos se vieron afectados, se observó que los logs del trabajo no contenían 
  información que permitiera saberlo y, por ello, no son útiles y es dificil saber cuáles
  archivos están afectados.

- Debido a lo anterior se concluyó que lo más práctico sería corregir el script, eliminar
  los archivos de salida y repetir el análisis (Lo cual es práctico ya que requiere de ~2 días 
  para terminar, que no es mucho tiempo).

- Siguiendo los consejos de Villay se creó esta bitácora para 
  tener un registro para futuras referencias y para evitar futuros errores.
  
- 13:43. Se inició el job array del proceso de mapeo desde cero (se eliminaron los archivos 
  anteriores).
  
- Se creó el script para el siguiente paso, convertir los archvos de salida de SAM a BAM.


