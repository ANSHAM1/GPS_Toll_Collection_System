import styles from "./Envoices.module.css";

const Envoices = ({ envoices }) => {
  return (
    <>
      <div className={styles.container}>
        {envoices.map((val, index) => (
          <div className={styles.box} key={index}>
            <h1>{val[0]}</h1>
            <h6>{val[1]}</h6>
          </div>
        ))}
      </div>
    </>
  );
};

export default Envoices;
