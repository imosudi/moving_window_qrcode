import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import QRCodeDisplay from "./QRCodeDisplay"; // Ensure this file exists
import "./index.css"; // Ensure this file exists

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
    <QRCodeDisplay instructorId="INS123" courseCode="SEN312" />
  </React.StrictMode>
);
