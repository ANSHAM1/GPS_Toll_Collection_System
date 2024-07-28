import styles from "./Main.module.css";
import RealTimeTracker from "../RealTimeTracker/RealTimeTracker.jsx";

import { useState } from "react";

function Main() {
  const [content, setContent] = useState("Real Time Tracking");
  const [activeBtn, setActiveBtn] = useState([true, false]);
  const [trackerType, setTrackerType] = useState("SIM");

  const handleOnClick = (value, index) => {
    setContent(value);
    const newActiveBtn = [false, false];
    newActiveBtn[index] = true;
    setActiveBtn(newActiveBtn);
  };

  return (
    <>
      <div className={styles.body}>
        <div className={styles.header}>
          <h3>GPS Based Toll Collection System.</h3>
          {["Real Time Tracking", "Envoices"].map((val, index) => (
            <p
              key={index}
              onClick={() => handleOnClick(val, index)}
              style={activeBtn[index] ? { color: "rgb(255, 36, 73)" } : {}}
            >
              {val}
            </p>
          ))}
          <select className={styles.dropdown} onChange={(e) => setTrackerType(e.target.value)}>
          <option value="SIM">Simulation</option>
          <option value="GPS">GPS Tracker</option>
          </select>
        </div>
        <RealTimeTracker
          content={content}
          Tracker={trackerType}
        />
      </div>
    </>
  );
}

export default Main;
