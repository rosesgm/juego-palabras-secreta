document.getElementById('btn-logout').addEventListener('click', function(e) {
    e.preventDefault(); // Evita que el enlace '#' recargue la página abruptamente

    Swal.fire({
        title: '¿Cerrar sesión?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d9534f',
        cancelButtonColor: '#aaa',
        confirmButtonText: 'Sí, salir',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "/logout"; 
        }
    });
});