const nivelActual = parseInt(document.getElementById('nivel-actual').dataset.nivel);
const totalNiveles = parseInt(document.getElementById('nivel-actual').dataset.total);
let vidas = 3;

document.getElementById('btn-submit').addEventListener('click', async () => {
    const respuesta = document.getElementById('answer-input').value.trim();

    if (!respuesta) {
        Swal.fire('Espera', 'Escribe una respuesta primero', 'warning');
        return;
    }

    const response = await fetch('/api/answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ level_number: nivelActual, answer: respuesta })
    });
    const data = await response.json();

    if (data.success) {
        if (nivelActual < totalNiveles) {
            await Swal.fire('¡Correcto!', '¡Avanzas al siguiente nivel!', 'success');
            window.location.href = `/game/${nivelActual + 1}`;
        } else {
            await Swal.fire('¡Ganaste!', '¡Completaste todos los niveles!', 'success');
            window.location.href = '/';
        }
    } else {
        vidas--;
        document.getElementById('lives-count').textContent = vidas;
        document.getElementById('answer-input').value = '';

        if (vidas <= 0) {
            await Swal.fire('¡Perdiste!', 'Se acabaron los intentos', 'error');
            window.location.href = '/game/1';
        } else {
            Swal.fire('Incorrecto', `Te quedan ${vidas} intentos`, 'error');
        }
    }
});

document.getElementById('answer-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') document.getElementById('btn-submit').click();
});