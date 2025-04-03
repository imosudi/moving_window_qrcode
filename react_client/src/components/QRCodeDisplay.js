import React, { useState, useEffect } from "react";
import { QRCodeCanvas } from "qrcode.react"; // Import QR Code generator

function QRCodeDisplay({ instructorId, courseCode }) {
  const [qrData, setQrData] = useState(null);
  const [expiryTime, setExpiryTime] = useState(null);

  const fetchQrCode = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8091/graphql_mutation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: `
            mutation {
              generateQrCode(instructorId: "${instructorId}", courseCode: "${courseCode}") {
                qrCodePayload
                expiryTime
              }
            }
          `,
        }),
      });

      const result = await response.json();
      if (result.data && result.data.generateQrCode) {
        setQrData(result.data.generateQrCode.qrCodePayload);
        setExpiryTime(result.data.generateQrCode.expiryTime * 1000); // Convert to milliseconds
      }
    } catch (error) {
      console.error("Error fetching QR Code:", error);
    }
  };

  useEffect(() => {
    fetchQrCode(); // Initial fetch

    const interval = setInterval(() => {
      if (expiryTime && Date.now() >= expiryTime) {
        console.log("QR Code expired! Fetching new one...");
        fetchQrCode(); // Refresh the QR code
      }
    }, 1000); // Check every second

    return () => clearInterval(interval); // Cleanup on unmount
  }, [expiryTime]);

  if (!qrData) return <p>Loading QR Code...</p>;

  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <h2>QR Code for {courseCode}</h2>
      <p>Instructor ID: {instructorId}</p>
      <p>Expires at: {new Date(expiryTime).toLocaleTimeString()}</p>
      <p><strong>QR Code Payload:</strong> {qrData}</p> {/* Displaying QR Code Payload */}
      <QRCodeCanvas value={qrData} size={300} />
    </div>
  );
}

export default QRCodeDisplay;
