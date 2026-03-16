import TrTableRow from "./TrTableRow";


const TrTable = ({transactions, onEditTransaction, className }) => {
  const cls = ["table", className].filter(Boolean).join(" ");

  let rows = transactions.map((transaction) => {
    return (
      <TrTableRow
        key={transaction.id}
        transaction={transaction}
        onClick={() => onEditTransaction(transaction.id)}
      />
    );
  });

  return (
    <table className={cls}>
      <thead>
        <tr>
          <th>date</th>
          <th>value</th>
          <th>category</th>
        </tr>
      </thead>
      <tbody className="table-group-divider">
        {rows}
      </tbody>
    </table>
  );
}

export default TrTable;