function fetchQRCode() {
    fetch("/get_qr_code")
        .then(response => response.json())
        .then(data => {
            if (data.qrCodePayload) {
                document.getElementById("qrPayload").innerText = data.qrCodePayload;
                document.getElementById("qrCodeImage").src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${data.qrCodePayload}`;
                document.getElementById("expiryTime").innerText = data.expiryTime;

                // Schedule next fetch
                let refreshTime = (data.expiryTime * 1000) - Date.now();
                setTimeout(fetchQRCode, Math.max(refreshTime, 1000));
            }
        })
        .catch(error => console.error("Error fetching QR Code:", error));
}

// Initial fetch
fetchQRCode();
