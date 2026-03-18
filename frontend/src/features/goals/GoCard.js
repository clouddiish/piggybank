const GoCard = ({ goal, onClick, className }) => {
  const cls = ["border rounded text-bg-secondary pt-2 mb-3", className].filter(Boolean).join(" ");

  return (
    <div onClick={onClick} style={{ cursor: onClick ? 'pointer' : 'default' }} className={cls}>
      <p className="text-center fw-bold">{goal.name}</p>
      <p className="text-center fw-bold">{goal.current_value + "/" + goal.target_value}</p>
      <p className="text-center">{goal.start_date + " - " + goal.end_date}</p>
      <p className="text-center">
        {goal.type}
        {goal.category ? `, ${goal.category}` : ""}
      </p>
    </div>
  );
}

export default GoCard;