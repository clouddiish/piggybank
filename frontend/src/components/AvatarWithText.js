const AvatarWithText = ({ text }) => {
  const firstChar = text ? text.charAt(0).toUpperCase() : "?";
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
      <div
        style={{
          width: 40,
          height: 40,
          borderRadius: "50%",
          background: "#1976d2",
          color: "#fff",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontWeight: "bold",
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
