document.getElementById('btn-register').addEventListener('click', async function() {
    const nombre = document.getElementById('user-name').value;
    const email = document.getElementById('user-email').value;
    const password = document.getElementById('user-password').value;
    const repeatPassword = document.getElementById('user-repeat-password').value;
    
    if (!nombre || !email || !password || !repeatPassword) {
        await Swal.fire({
            icon: 'error',
            title: 'Campos incompletos',
            text: 'Por favor, completa todos los campos',
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Entendido'
        });        return;
    }
    
    if (password !== repeatPassword) {
        await Swal.fire({
            icon: 'error',
            title: 'Contraseña incorrecta',
            text: 'Por favor, verificar que ambas contraseñas sean iguales',
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Reintentar'
        }); 
        return;
    }
    
   
    const response = await fetch('/api/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({nombre, email, password})
    });
    
    const result = await response.json();
    
    if (response.ok) {
        await Swal.fire({
                icon: 'success',
                title: '¡Registro exitoso!',
                text: 'Tu cuenta ha sido creada correctamente',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Iniciar sesión',
                timer: 3000,
                timerProgressBar: true
            });       
        window.location.href = '/'; 
    } else {
        await Swal.fire({
                icon: 'error',
                title: 'Error en el registro',
                text: result.error || 'Ocurrió un problema al registrar el usuario',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Intentar de nuevo'
            });
    }
});

    document.getElementById('user-repeat-password').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('btn-register').click();
    }
});