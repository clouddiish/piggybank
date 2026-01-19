import TrTableRow from "./TrTableRow";


const TrTable = ({transactions, onEditTransaction }) => {
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
    <table className="table my-3">
      <thead>
        <tr>
          <th>date</th>
          <th>value</th>
          <th>category</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  );
}

export default TrTable;