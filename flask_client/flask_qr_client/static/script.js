
// Ensure the function is only called when the instructor page is loaded
document.addEventListener("DOMContentLoaded", () => {
    const instructorId = "INS123";  // Replace with dynamic values if necessary
    const courseCode = "SEN312";    // Replace with dynamic values if necessary

    if (document.getElementById("qr-container")) {
        fetchQRCode(instructorId, courseCode);
    }

    if (typeof Html5Qrcode === "undefined") {
        console.error("Html5Qrcode is not loaded. Ensure the library is included.");
        return;
    }

    if (document.getElementById("start-scanner")) {
        document.getElementById("start-scanner").addEventListener("click", startScanner);
    }
});

function reloadQRCode() {
    location.reload(); // Simple way to refresh the page
}

