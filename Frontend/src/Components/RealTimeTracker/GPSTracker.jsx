import styles from "./RealTimeTracker.module.css";
import { useState, useEffect } from "react";

const GPSTracker = ({
  current,
  handleProps,
  handleCurrent,
  handleEnvoices,
}) => {
  const [action, setAction] = useState(false);
  const [location, setLocation] = useState({ latitude: 0, longitude: 0 });

  useEffect(() => {
    const getLocation = () => {
      setInterval(() => {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              const { latitude, longitude } = position.coords;
              setLocation({ latitude, longitude });
            },
            (error) => {
              console.error("Error getting location: ", error);
            }
          );
        } else {
          console.error("Geolocation is not supported by this browser.");
        }
      }, 4000);
    };
    getLocation();
  }, []);

  useEffect(() => {
    const coordinates = async () => {
      if (action === true) {
        handleCurrent([location["latitude"], location["longitude"]]);

        const response = await fetch("http://localhost:4000/coordinates", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(location),
        });
        if (response.ok) {
          const data = await response.json();
          handleProps(data["DATA"]);
        }
      } else if (action === false) {
        const response = await fetch("http://localhost:4000/end");
        if (response.ok) {
          const data = await response.json();
          handleProps(data["DATA"]);
        }
      }
    };
    coordinates();
  }, [action, location]);

  function handleBtnText() {
    if (action === false) {
      return "Start";
    } else if (action === true) {
      return "Pause";
    }
  }

  return (
    <>
      <button
        className={styles.btn}
        onClick={() =>
          setAction((prev) => {
            return !prev;
          })
        }
      >
        {handleBtnText()}
      </button>
    </>
  );
};

export default GPSTracker;
