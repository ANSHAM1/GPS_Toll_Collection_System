import { useEffect, useState, useRef } from "react";
import styles from "./RealTimeTracker.module.css";
import io from "socket.io-client";

const SocketComponent = ({ handleProps, handleCurrent, handleEnvoices }) => {
  const [active, setActive] = useState(false);
  const [simulation, setSimulation] = useState(false);
  const [speed, setSpeed] = useState(1);
  const socketRef = useRef(null);

  useEffect(() => {
    const socket = io("http://127.0.0.1:5000");
    socketRef.current = socket;
    return () => {
      socketRef.current.disconnect();
    };
  }, []);

  useEffect(() => {
    socketRef.current.on("connect", () => {
      setActive(true);
    });

    socketRef.current.on("message_from_server", (data) => {
      handleCurrent(data[0]);
      handleProps(data[1]);
      if (data[2] === "End") {
        setSimulation("End");
        socketRef.current.emit("message_from_client_for_end", "end");
      }
      socketRef.current.emit("message_from_client", speed);
    });

    socketRef.current.on("message_from_server_for_envoices", (data) => {
      handleEnvoices(data);
    });

    return () => {
      socketRef.current.off("connect");
      socketRef.current.off("message_from_server");
      socketRef.current.off("message_from_server_for_envoices");
    };
  }, [speed]);

  function sendMessage() {
    setSimulation(true);
    socketRef.current.emit("message_from_client", "Start...");
  }

  function handleBtnText() {
    if (simulation == false) {
      return "Start Simulation";
    } else if (simulation == true) {
      return "Simulation is Running";
    } else if (simulation === "End") {
      return "Simulation Ended";
    }
  }

  useEffect(() => {
    const handleKeyDown = (event) => {
      const step = 1;
      let newValue = speed;

      if (event.key === "ArrowRight") {
        newValue += step;
      } else if (event.key === "ArrowLeft") {
        newValue -= step;
      }

      newValue = Math.max(1, Math.min(60, newValue));
      setSpeed(newValue);
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [speed]);

  return (
    <>
      {active ? (
        <>
          <button
            className={styles.btn}
            onClick={sendMessage}
            disabled={simulation === "End" ? true : false}
          >
            {handleBtnText()}
          </button>
          <input
            className={styles.speed}
            type="range"
            min="1"
            max="60"
            value={speed}
            onChange={(e) => setSpeed(Number(e.target.value))}
          ></input>
        </>
      ) : (
        <>
          <button className={styles.btnDisabled} disabled>
            Connecting to Server....
          </button>
          <input
            className={styles.speed}
            type="range"
            min="1"
            max="60"
            value={speed}
            onChange={(e) => setSpeed(Number(e.target.value))}
          ></input>
        </>
      )}
    </>
  );
};

export default SocketComponent;
