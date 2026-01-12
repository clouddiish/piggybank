const Button = ({
  variant = "primary", 
  icon: Icon,         
  children,
  ...props
}) => {
  const baseStyle = {
    padding: "8px 16px",
    border: "none",
    borderRadius: "4px",
    fontWeight: "bold",
    display: "inline-flex",
    alignItems: "center",
    cursor: "pointer",
    background: variant === "primary" ? "#1976d2" : "#e0e0e0",
    color: variant === "primary" ? "#fff" : "#333",
    gap: Icon ? "8px" : "0",
  };

  return (
    <button style={baseStyle} {...props}>
      {Icon && <Icon />}
      {children}
    </button>
  );
};

export default Button;