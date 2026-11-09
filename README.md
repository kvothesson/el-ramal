# El Ramal

Un tren fantasma en un ramal cerrado en 1993. El tren no se enteró.

Roguelite de pixel art y horror que se juega en el navegador: **[jugalo en kvothesson.com/el-ramal](https://kvothesson.com/el-ramal/)**. Armás un tren vagón por vagón, reabrís los pueblos muertos del ramal y en cada vuelta tenés que entregar una cuota. Si no llegás, el ramal cierra.

## Cómo se juega

- El tren recorre los 8 lugares del ramal y frena donde hay un pueblo. Ahí sus vagones se activan de izquierda a derecha.
- Unos vagones suben **carga** (cajones) y otros levantan la **presión** de la caldera. En cada parada entregás carga × presión.
- Si al terminar la vuelta no llenaste la cuota, el ramal cierra.
- En el taller comprás vagones, los ordenás y reabrís un pueblo por vuelta. El orden importa: muchos vagones combinan con el de al lado.
- Cada 4 vueltas sube un inspector con una regla nueva. En el taller ves cuál viene.
- La meta es la vuelta 16, el Fin de la vía. Después podés seguir sin fin.
- Los pueblos que reabrís quedan abiertos para siempre y traen vagones nuevos. Llegar lejos desbloquea otros trenes de arranque.

## Controles

- Mouse: todo. Señalá cualquier cosa y la caja de abajo explica qué hace.
- Esc: pausa (y saltear cinemáticas).
- F: pantalla completa.
- La partida se guarda sola.

## Cómo está hecho

Todo con código: los sprites salen de un motor (`arte/sprites.py` los regenera) de pixel art con luz por normales, rampas de color y contorno selectivo (`arte/`); el sonido es síntesis en vivo con Web Audio; el juego es un solo `index.html` sin dependencias.

Para jugarlo local: abrí `abrir.cmd`, o servilo con cualquier servidor estático (`python -m http.server`) y entrá a la carpeta.

Un juego de [Kvothesson](https://kvothesson.com/).
