document.getElementById('level-select').addEventListener('change', function () {
    const opt = this.options[this.selectedIndex];
    document.getElementById('level-number').value = opt.value;
    document.getElementById('level-hint').value   = opt.dataset.hint || '';
    document.getElementById('level-word').value   = '';
});

document.getElementById('btn-save-level').addEventListener('click', async () => {
    const level_number = document.getElementById('level-number').value;
    const hint         = document.getElementById('level-hint').value.trim();
    const word         = document.getElementById('level-word').value.trim();

    if (!level_number || !hint) {
        Swal.fire('Error', 'Selecciona un nivel y escribe la pista', 'error');
        return;
    }

    if (!word) {
        const confirm = await Swal.fire({
            title: '¿Sin nueva palabra?',
            text: 'No escribiste una palabra secreta. ¿Solo actualizar la pista?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Sí, solo la pista',
            cancelButtonText: 'Cancelar'
        });
        if (!confirm.isConfirmed) return;
    }

    const response = await fetch('/api/level', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ level_number: parseInt(level_number), hint, word })
    });
    const data = await response.json();

    if (data.success) {
        await Swal.fire('¡Guardado!', data.message, 'success');
        // Limpia el formulario y el selector de niveles
        document.getElementById('admin-form').reset();
        document.getElementById('level-select').value = "";
    } else {
        Swal.fire('Error', data.message, 'error');
    }
});