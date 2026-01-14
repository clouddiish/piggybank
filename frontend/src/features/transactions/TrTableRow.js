const TrTableRow = ({
  transaction
}) => {
  return (
    <tr>
      <td>{transaction.date}</td>
      <td>{transaction.type === "income" ? "+" + transaction.value : "-" + transaction.value}</td>
      <td>{transaction.category}</td>
    </tr>
  );
}

export default TrTableRow;