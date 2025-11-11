# microservicio que reciba un número por URL y devuelva una respuesta JSON

Este microservicio expone un endpoint que recibe un número por URL y devuelve un JSON con:
- `numero`: el valor recibido
- `factorial`: el factorial de `numero` (para `n >= 0`)
- `etiqueta`: `"par"` o `"impar"` según el número

## Análisis: ¿Cómo lo modificaría para registrar historial en otro servicio?

El objetivo es que este servicio (A) calcule y devuelva la respuesta sin bloquearse, y envíe el resultado a un servicio externo de historial (B) que lo guarda en una base de datos.

1. **Separación de responsabilidades**
   - **Servicio A (este repo):** cálculo y respuesta JSON.  
   - **Servicio B (historial):** persistencia (expone `POST /history` y escribe en la BD).

2. **Comunicación**
   - En A, enviar un `POST` a B en background para no retrasar la respuesta al cliente.  
   - URL de B por variable de entorno `HISTORY_API_URL` (evita acoplar la dirección).

3. **Resiliencia**  
   - Si B falla, A responde igual (no rompemos la experiencia del usuario).

4. **Escalabilidad**
   - Si la carga crece, pasar de HTTP directo a mensajería (podria ser SQS).  
     - A publica evento `calculo_realizado`.  
     - B consume y persiste. Esto desacopla los servicios y absorbe picos de carga.

---

### Reglas/validaciones
- `n >= 0` (si es negativo → `400 Bad Request`)
- Límite práctico `n <= 2000` para evitar bloqueos por factoriales enormes (ajustable).

## Correr local

pip install -r requirements.txt
uvicorn app.main:app --reload


Probar: http://127.0.0.1:8000/calc/7
DocsSwagger: http://127.0.0.1:8000/docs

## Docker

docker build -t servicio-factorial .
docker run --rm -p 8000:8000 servicio-factorial

```bash