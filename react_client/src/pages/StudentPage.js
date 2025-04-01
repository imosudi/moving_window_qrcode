import React from "react";
import QRCodeScanner from "../components/QRCodeScanner";

const StudentPage = () => {
    const studentId = "STU456"; // Replace with actual student ID

    return (
        <div className="container">
            <h1>Student QR Code Scanner</h1>
            <QRCodeScanner studentId={studentId} />
        </div>
    );
};

export default StudentPage;
