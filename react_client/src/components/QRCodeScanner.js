
import React, { useState, useEffect } from "react";
import { Html5QrcodeScanner } from "html5-qrcode";
import "./QRCodeScanner.css";

const QRCodeScanner = ({ studentId }) => {
    const [scanResult, setScanResult] = useState(null);
    const [error, setError] = useState("");

    useEffect(() => {
        const scanner = new Html5QrcodeScanner("qr-reader", { fps: 10, qrbox: 250 });

        scanner.render(
            (decodedText) => {
                setScanResult(decodedText);
                scanner.clear();
                submitAttendance(decodedText);
            },
            (err) => setError("Scanning failed. Try again.")
        );

        return () => scanner.clear();
    }, []);

    const submitAttendance = async (scannedPayload) => {
        try {
            const response = await fetch("http://127.0.0.1:8091/graphql_mutation", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ encrypted_payload: scannedPayload, student_id: studentId }),
            });

            const data = await response.json();
            if (data.status === "SUCCESS") {
                alert("Attendance recorded successfully!");
            } else {
                alert("Attendance error: " + data.error_message);
            }
        } catch (error) {
            console.error("Error submitting attendance:", error);
            alert("Error submitting attendance. Please try again.");
        }
    };

    return (
        <div className="scanner-container">
            <h2>Scan QR Code for Attendance</h2>
            <div id="qr-reader"></div>
            {scanResult && <p>Scanned Data: {scanResult}</p>}
            {error && <p className="error">{error}</p>}
        </div>
    );
};

export default QRCodeScanner;

