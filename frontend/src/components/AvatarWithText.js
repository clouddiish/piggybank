const AvatarWithText = ({ text, className }) => {
  const firstChar = text ? text.charAt(0).toUpperCase() : "?";
  return (
    <div className={className} style={{ display: "flex", alignItems: "center", gap: 12 }}>
      <div
        style={{
          width: 40,
          height: 40,
          borderRadius: "50%",
          background: "#f3d216",
          color: "#080e1b",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 20,
        }}
      >
        {firstChar}
      </div>
      <span style={{ fontSize: 18 }}>{text}</span>
    </div>
  );
};

export default AvatarWithText;
