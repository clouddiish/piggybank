const TrTableRow = ({
  transaction,
  onClick
}) => {
  return (
    <tr onClick={onClick} style={{ cursor: onClick ? 'pointer' : 'default' }}>
      <td>{transaction.date}</td>
      <td>{transaction.type === "income" ? "+" + transaction.value : "-" + transaction.value}</td>
      <td>{transaction.category}</td>
    </tr>
  );
}

export default TrTableRow;