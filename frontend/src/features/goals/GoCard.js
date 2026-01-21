const GoCard = ({ goal }) => {
  return (
    <div className="col-md-12 col-sm-4 container my-1 border rounded pt-1">
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