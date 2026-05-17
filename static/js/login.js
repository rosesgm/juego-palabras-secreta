
document.getElementById('btn-login').addEventListener('click', async () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();
    if (data.success) {
        window.location.href = data.redirect;
    } else {
        Swal.fire({
            icon: 'error',
            title: 'Ha ocurrido un error al iniciar sesión',
            text: data.message,
            confirmButtonColor: '#243b55'
        });
    }

    document.getElementById('password').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('btn-login').click();
    }
    });
});