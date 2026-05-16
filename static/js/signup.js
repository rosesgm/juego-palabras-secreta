document.getElementById('btn-register').addEventListener('click', async function() {
    const nombre = document.getElementById('user-name').value;
    const email = document.getElementById('user-email').value;
    const password = document.getElementById('user-password').value;
    const repeatPassword = document.getElementById('user-repeat-password').value;
    
    if (!nombre || !email || !password || !repeatPassword) {
        alert('Completa todos los campos');
        return;
    }
    
    if (password !== repeatPassword) {
        alert('Las contraseñas no coinciden');
        return;
    }
    
   
    const response = await fetch('/api/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({nombre, email, password})
    });
    
    const result = await response.json();
    
    if (response.ok) {
        alert('¡Registro exitoso!');
        window.location.href = '/'; 
    } else {
        alert(result.error);
    }
});