const CaCard = ({ 
  category,
  onClick
}) => {
  return (
    <div onClick={onClick} style={{ cursor: onClick ? 'pointer' : 'default' }} className="col-md-12 col-sm-4 container my-1 border rounded pt-1">
      <p className="text-center">{category.name}</p>
    </div>
  );
}

export default CaCard;