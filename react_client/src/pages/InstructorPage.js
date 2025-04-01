import React from "react";
import QRCodeDisplay from "../components/QRCodeDisplay";

const InstructorPage = () => {
    return (
        <div className="container">
            <h1>Instructor QR Code Generator</h1>
            <QRCodeDisplay />
        </div>
    );
};

export default InstructorPage;
