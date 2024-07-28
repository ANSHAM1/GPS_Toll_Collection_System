import React, { useState } from "react";
import styles from "./RealTimeTracker.module.css";
import Envoices from "../Envoices/Envoices.jsx";
import Map from "../Map/Map";

import SocketComponent from "./SocketIO";
import GPSTracker from "./GPSTracker.jsx";

const RealTimeTracker = ({ content, Tracker }) => {
  const [current, setCurrent] = useState([26.666989, 80.809133]);
  const [prop, setProp] = useState({
    totalDistance: 0,
    tollRoadDistance: 0,
    tollRoad: "NH1",
    tollTax: 1,
  });
  const [envoices, setEnvoices] = useState([]);

  const handleEnvoices = (value) => {
    setEnvoices(value);
  };

  const handleCurrent = (value) => {
    setCurrent(value);
  };

  const handleProps = (props) => {
    setProp(props);
  };

  const handleContent = () => {
    if (content === "Real Time Tracking") {
      return (
        <>
          <div className={styles.left}>
            {[
              ["Distance Travelled in km : ", prop.totalDistance],
              ["Current Toll Road if any : ", prop.tollRoad],
              [
                `Distance Travelled on ${prop.tollRoad} : `,
                prop.tollRoadDistance,
              ],
              ["Toll Tax in Current Zone in rupees : ", prop.tollTax],
              ["Current Location : ", `${current[0]} , ${current[1]}`],
            ].map((val, index) => (
              <div key={index} className={styles.info}>
                <h3>
                  {val[0]} <span>{val[1]}</span>
                </h3>
              </div>
            ))}
          </div>
          <div className={styles.right}>
            <Map position={current} style={{ height: "100%", width: "100%" }} />
          </div>
        </>
      );
    } else if (content === "Envoices") {
      return <Envoices envoices={envoices} />;
    }
  };

  const handleTracker = () => {
    if (Tracker === "SIM") {
      return (
        <SocketComponent
          handleProps={handleProps}
          handleCurrent={handleCurrent}
          handleEnvoices={handleEnvoices}
        />
      );
    } else if (Tracker === "GPS") {
      return (
        <GPSTracker
          current={current}
          handleProps={handleProps}
          handleCurrent={handleCurrent}
          handleEnvoices={handleEnvoices}
        />
      );
    }
  };

  return (
    <div className={styles.container}>
      {handleTracker()}
      {handleContent()}
    </div>
  );
};

export default RealTimeTracker;
