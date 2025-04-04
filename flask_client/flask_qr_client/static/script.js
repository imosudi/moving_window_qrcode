function formatTimestamp(timestamp) {
    if (!timestamp) return "N/A";  // Handle missing timestamp case
    const date = new Date(timestamp * 1000);
    return date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
}

document.addEventListener("DOMContentLoaded", function () {
    const expirySpan = document.getElementById("expiryTime");
    const expiryTimestamp = parseInt(expirySpan.getAttribute("data-timestamp"), 10);
    expirySpan.textContent = formatTimestamp(expiryTimestamp);
});

function reloadQRCode() {
    location.reload(); // Simple way to refresh the page
}

async function fetchQRCode(instructorId, courseCode) {
    try {
        const response = await fetch("/generate_qr", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ instructor_id: instructorId, course_code: courseCode }),
        });

        const result = await response.json();

        let qrContainer = document.getElementById("qr-container");
        if (qrContainer) {
            qrContainer.innerHTML = `<img src="data:image/png;base64,${result.qr_code}" alt="QR Code">`;
        }

        let expiryText = document.getElementById("expiry-time");
        if (expiryText) {
            expiryText.innerText = `Expires at: ${new Date(result.expiry * 1000).toLocaleTimeString()}`;
        }
    } catch (error) {
        console.error("Error fetching QR Code:", error);
    }
}

function refreshQRCode() {
    location.reload(); // Simple refresh mechanism for now
}

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

function startScanner() {
    if (typeof Html5Qrcode === "undefined") {
        alert("QR Code scanner library not loaded. Please refresh the page.");
        return;
    }

    const scanner = new Html5Qrcode("qr-reader");

    scanner.start(
        { facingMode: "environment" }, // Rear camera
        { fps: 10, qrbox: 250 },
        (decodedText) => {
            console.log("Scanned QR Code:", decodedText);
            document.getElementById("scan-result").innerText = `Scanned: ${decodedText}`;
            scanner.stop();
            submitAttendance(decodedText);
        },
        (error) => {
            console.warn("Scanning error:", error);
        }
    ).catch((err) => {
        console.error("Error starting scanner:", err);
    });
}

async function submitAttendance(scannedPayload) {
    try {
        const response = await fetch("/submit_attendance", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scanned_payload: scannedPayload, student_id: "STU456" })
        });

        const result = await response.json();
        if (result.status === "SUCCESS") {
            alert("Attendance recorded successfully!");
        } else {
            alert("Attendance error: " + result.error_message);
        }
    } catch (error) {
        console.error("Error submitting attendance:", error);
        alert("Error submitting attendance. Please try again.");
    }
}

// Initial fetch
document.addEventListener("DOMContentLoaded", () => {
    const instructorId = "INS123"; // Replace dynamically if needed
    const courseCode = "SEN312";   // Replace dynamically if needed
    fetchQRCode(instructorId, courseCode);
});

// Initial fetch
fetchQRCode();
