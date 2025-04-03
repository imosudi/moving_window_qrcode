
import React from "react";
import QRCodeDisplay from "../components/QRCodeDisplay";


const InstructorPage = () => {
    console.log("InstructorPage Loaded"); // Debugging line
    return (
        <div className="container">
            <h1>Instructor QR Code Generator</h1>
            {/* Remove QRCodeDisplay temporarily */}
             <QRCodeDisplay instructorId="INS123" courseCode="SEN312" /> 
        </div>
    );
};



export default InstructorPage;

