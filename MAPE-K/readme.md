# MAPE-K: Cómputo Autónomo  
![image](https://github.com/user-attachments/assets/e2851249-8f92-46e3-9bec-997fe9972e65)

## Descripción  

Este sistema implementa el modelo **MAPE-K** para el monitoreo y control de la temperatura y humedad mediante un Arduino con un sensor **DHT11**. Su propósito es analizar las lecturas obtenidas, clasificarlas según reglas predefinidas y tomar decisiones en función de los resultados.  

## Esquemático  

![image](https://github.com/user-attachments/assets/7d74d473-66d2-4a3c-bd99-fc86920e1fcb)

## Funcionamiento  

### 1. Monitoreo  
- El sistema recibe datos a través del puerto serial desde un **Arduino** con un sensor **DHT11**.  
- Un módulo de **monitor** lee estas lecturas mediante un método específico del puerto serial.  

### 2. Análisis  
- Una clase de **análisis** procesa los datos obtenidos y los compara con reglas predefinidas en una base de conocimiento (**Knowledge**).  
- Estas reglas fueron inicialmente categorizadas en un archivo **Excel**, diferenciando datos normales y anormales.  
- Posteriormente, la información se importó a la herramienta de IA **Weka**, donde se aplicó el algoritmo **Naive Bayes**. Se eligió este método debido a la correlación entre temperatura y humedad, evitando la exclusión de variables que ocurre con algoritmos como **J48**.  

### 3. Planificación  
- El módulo de **planeación** consulta el analizador en busca de alertas basadas en el monitoreo y la base de conocimiento.  
- Si se detecta una anomalía, se envían los datos al **ejecutor**.  

### 4. Ejecución  
- El ejecutor realiza una consulta a **OpenAPI** para obtener recomendaciones sobre cómo mantener la temperatura en un rango óptimo.  
- Un caso hipotético sería la conservación de vacunas en condiciones ideales.  



## Instrucciones para Clasificación de Datos en Weka

### 1. Registro de Datos
Se almacenan los valores obtenidos de los sensores para su posterior clasificación:

- **Normal - Temperatura**
- **Anormal - Temperatura**
- **Normal - Humedad**
- **Anormal - Humedad**

![image](https://github.com/user-attachments/assets/b284def0-41b4-4c13-b788-9b0ec9ba1b37)

### 2. Importación de Datos en Weka
Se importa el archivo de datos en Weka.

![image](https://github.com/user-attachments/assets/037987a4-b77c-41ac-af3f-c9ae4107a429)

### 3. Apertura del Archivo
- Utiliza la opción **OpenFile**.
- Asegúrate de seleccionar el formato correcto, en este caso **.csv**.

![image](https://github.com/user-attachments/assets/a0539c85-df19-4da1-92c0-f830d1568f54)

### 4. Verificación de Datos
- Asegúrate de que los datos estén bien cargados y en el formato adecuado.

![image](https://github.com/user-attachments/assets/442e2577-39fb-4681-99f7-b3d56ad2fa6d)

### 5. Selección del Clasificador
- Ve a la pestaña de **Clasificador**.

![image](https://github.com/user-attachments/assets/83f23267-de84-4834-8dcf-277388df7881)

### 6. Elección del Tipo de Clasificador
- Selecciona el algoritmo de clasificación que deseas utilizar.

![image](https://github.com/user-attachments/assets/90a4649d-f45d-4f3e-9c73-65ffab18f5a2)

### 7. Ejecución del Análisis
- Presiona **Start** para iniciar el proceso de clasificación.
- Se generará un modelo basado en los datos proporcionados.

![image](https://github.com/user-attachments/assets/96aec125-cc4d-45fb-aa7d-b2edd41e0ab2)

### 8. Análisis de Resultados
- Analiza los límites establecidos para cada variable (temperatura y humedad).
- Define un **umbral de tolerancia** para determinar si se debe activar una alerta.

![image](https://github.com/user-attachments/assets/c7807ed6-3a12-4191-ae06-08b818af9eff)

### 9. Código de Arduino
Este es el código de Arduino para imprimir el valor del sensor en el puerto serial:

![image](https://github.com/user-attachments/assets/65360efe-dd43-470b-bc8d-dd293168a292)

## 10. Respuesta Open API al generarse una alerta

![image](https://github.com/user-attachments/assets/01b70107-0bbd-4876-9cf4-d2f45233688a)


```python
    python planeador.py
```


### 11. Trabajo pendiente automatización mediante simulación fisica  con https://wokwi.com/ para le obtención de datos
![image](https://github.com/user-attachments/assets/1499ae65-6e73-4b97-a9ab-5a76a082e8a7)
![Recording 2025-03-22 at 10 05 12](https://github.com/user-attachments/assets/bef5522c-1df0-4d3b-ad8a-627cfbbd4f01)

```robot
    robot test.robot
```

### 12. Evidencias

![WhatsApp Image 2025-03-21 at 09 50 00](https://github.com/user-attachments/assets/aceeace7-2b1c-4703-be3f-ac479c7dbacb)


![WhatsApp Image 2025-03-21 at 09 51 07](https://github.com/user-attachments/assets/ba65dd1d-afcd-4a75-8518-23c756b0342d)


![Recording 2025-03-21 at 10 03 40](https://github.com/user-attachments/assets/29b3ae2c-bf16-41fa-a6ff-af9c0d5d0a1e)








