import React, { useState } from "react";
import { QrReader } from "react-qr-reader";
import axios from "axios";

const AttendanceApp = () => {
  const [studentId, setStudentId] = useState("");
  const [authToken, setAuthToken] = useState("");
  const [scannedPayload, setScannedPayload] = useState(null);
  const [message, setMessage] = useState("");
  
  const authenticate = () => {
    if (!studentId || !authToken) {
      setMessage("Authentication failed. Please log in.");
      return false;
    }
    return true;
  };

  const handleScan = (data) => {
    if (data) {
      setScannedPayload(data.text);
      submitAttendance(data.text);
    }
  };

  const handleError = (err) => {
    console.error(err);
  };

  const submitAttendance = async (payload) => {
    if (!authenticate()) return;

    try {
      const response = await axios.post("http://your-server.com/api/validateAttendance", {
        encrypted_payload: payload,
        student_id: studentId,
      });

      if (response.data.status === "SUCCESS") {
        setMessage("Attendance recorded successfully.");
      } else {
        setMessage("Attendance error: " + response.data.error_message);
      }
    } catch (error) {
      setMessage("Error submitting attendance.");
    }
  };

  return (
    <div className="container text-center mt-5">
      <h2>Student Attendance System</h2>
      <div>
        <input
          type="text"
          placeholder="Student ID"
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
        />
        <input
          type="password"
          placeholder="Auth Token"
          value={authToken}
          onChange={(e) => setAuthToken(e.target.value)}
        />
      </div>
      <QrReader
        onResult={(result, error) => {
          if (result) handleScan(result);
          if (error) handleError(error);
        }}
        style={{ width: "300px" }}
      />
      <p>{message}</p>
    </div>
  );
};

export default AttendanceApp;
