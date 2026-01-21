const TrSummaryCard = ({ title, value }) => {
  return (
    <div className="col-md-12 col-sm-4 container my-1 border rounded pt-1">
      <p className="text-center fw-bold">{title}</p>
      <p className="text-center">{value}</p>
    </div>
  );
}

export default TrSummaryCard;