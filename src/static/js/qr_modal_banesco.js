document.getElementById("generateQRbanesco").addEventListener("click", function () {
    // Mostrar el modal de carga inmediatamente al hacer clic
    let loadingModalElement = document.getElementById("loadingModal");
    let loadingModal = new bootstrap.Modal(loadingModalElement);
    loadingModal.show();

    fetch("/generarqr")
        .then(response => response.json())
        .then(data => {
            // Ocultar el modal de carga después de recibir la respuesta (éxito o error)
            loadingModal.hide();

            if (data.qr_image) {
                document.getElementById("qrImage").src = data.qr_image;
                let qrModalElement = document.getElementById("qrModal");
                let qrModal = new bootstrap.Modal(qrModalElement);
                qrModal.show();
            } else {
                alert("No se pudo obtener el código QR. Inténtalo nuevamente.");
            }
        })
        .catch(error => {
            // Asegúrate de ocultar el modal de carga también en caso de error
            loadingModal.hide();
            console.error("Error al obtener el código QR:", error);
            alert("Ocurrió un error al obtener el código QR.");
        });
});