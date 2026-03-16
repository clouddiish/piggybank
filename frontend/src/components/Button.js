const Button = ({
  variant = "primary", 
  icon: Icon,         
  children,
  className,
  ...props
}) => {
  const variantClass = `btn-${variant}`;
  const cls = ["btn", variantClass, className].filter(Boolean).join(" ");

  return (
    <button className={cls} {...props}>
      {Icon && (
        <span className="btn-icon" aria-hidden="true">
          <Icon className="me-2"/>
        </span>
      )}
      {children}
    </button>
  );
};

export default Button;