import styles from "./Main.module.css";
import RealTimeTracker from "../RealTimeTracker/RealTimeTracker.jsx";

import { useState } from "react";

function Main() {
  const [content, setContent] = useState("Real Time Tracking");
  const [activeBtn, setActiveBtn] = useState([true, false]);

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
          {["Real Time Tracking", "Envoices"].map(
            (val, index) => (
              <p
                key={index}
                onClick={() => handleOnClick(val, index)}
                style={activeBtn[index] ? { color: "rgb(255, 36, 73)" } : {}}
              >
                {val}
              </p>
            )
          )}
        </div>
        <RealTimeTracker content={content}/>
      </div>
    </>
  );
}

export default Main;
