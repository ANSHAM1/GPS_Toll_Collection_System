import styles from "./Envoices.module.css";

const Envoices = ({ envoices }) => {
  return (
    <>
      <div className={styles.container}>
        {envoices.map((val, index) => (
          <div className={styles.box} key={index}>
            <div className={styles.envoice}>ENVOICE {index}</div>
            <div className={styles.message}>
              TOLL FOR TRAVELLING ON ROAD - {val[0]} is {val[1]}.
            </div>
          </div>
        ))}
      </div>
    </>
  );
};

export default Envoices;
