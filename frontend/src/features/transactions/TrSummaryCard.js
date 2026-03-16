const TrSummaryCard = ({ title, value, className }) => {
  const cls = ["border rounded text-bg-secondary pt-1", className].filter(Boolean).join(" ");

  return (
    <div className={cls}>
      <p className="text-center fw-bold">{title}</p>
      <p className="text-center">{value}</p>
    </div>
  );
}

export default TrSummaryCard;