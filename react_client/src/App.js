import React, { useState } from "react";
import InstructorPage from "./pages/InstructorPage";
import StudentPage from "./pages/StudentPage";

function App() {
    const [role, setRole] = useState("instructor");

    return (
        <div className="App">
            <nav>
                <button onClick={() => setRole("instructor")}>Instructor</button>
                <button onClick={() => setRole("student")}>Student</button>
            </nav>
            {role === "instructor" ? <InstructorPage /> : <StudentPage />}
        </div>
    );
}

export default App;
