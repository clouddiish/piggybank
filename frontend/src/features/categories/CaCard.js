const CaCard = ({ category, onClick, className }) => {
  const cls = ["border rounded text-bg-secondary pt-2 mb-3", className].filter(Boolean).join(" ");
  
  return (
    <div onClick={onClick} style={{ cursor: onClick ? 'pointer' : 'default' }} className={cls}>
      <p className="text-center">{category.name}</p>
    </div>
  );
}

export default CaCard;