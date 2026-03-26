import { useState } from "react";

import Button from "../../components/Button";
import useAuthValidation from "../../hooks/useAuthValidation";


const RegisterForm = ({ onRegister }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [registerError, setRegisterError] = useState(null);
  const { validationErrors, validateEmail, validatePassword, validateConfirmPassword } = useAuthValidation();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateEmail(email)) return;
    if (!validatePassword(password)) return;
    if (!validateConfirmPassword(password, confirmPassword)) return;

    setLoading(true);

    try {
      await onRegister(email, password, confirmPassword);
    } catch (err) {
      const status = err?.response?.status;
      const data = err?.response?.data;
      const backendMsg =
        data?.detail || data?.message || (typeof data === "string" ? data : null);

      if (status === 422) {
        setRegisterError(backendMsg || "user email already exists");
      } else if (status >= 500) {
        setRegisterError(backendMsg || "server error - please try again later");
      } else if (err?.request) {
        setRegisterError("network error - please check your connection");
      } else {
        setRegisterError(err?.message || "an unexpected error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

    return (
      <div className="row">
  			<div className="col-12 col-md-6">
          <form onSubmit={handleSubmit} aria-busy={loading}>
            <div className="mb-1">
              <label htmlFor="email" className="form-label">email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  if (validationErrors.email) validateEmail(e.target.value);
                }}
                onBlur={() => validateEmail(email)}
                required
                placeholder="email@example.com"
                className={`form-control ${validationErrors.email ? "is-invalid" : ""}`}
              />
              <div
                className="invalid-feedback"
                role="alert"
                aria-live="polite"
                style={{
                  display: "block",
                  visibility: validationErrors.email ? "visible" : "hidden",
                  minHeight: "1.25rem",
                }}
              >
                {validationErrors.email || "\u00A0"}
              </div>
            </div>
            <div className="mb-1">
              <label htmlFor="password" className="form-label">password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (validationErrors.password) validatePassword(e.target.value);
                }}
                onBlur={() => validatePassword(password)}
                required
                placeholder="password"
                className={`form-control ${validationErrors.password ? "is-invalid" : ""}`}
              />
              <div
                className="invalid-feedback"
                role="alert"
                aria-live="polite"
                style={{
                  display: "block",
                  visibility: validationErrors.password ? "visible" : "hidden",
                  minHeight: "1.25rem",
                }}
              >
                {validationErrors.password || "\u00A0"}
              </div>
            </div>
            <div className="mb-1">
              <label htmlFor="cpassword" className="form-label">confirm password</label>
              <input
                id="cpassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => {
                  setConfirmPassword(e.target.value);
                  if (validationErrors.confirmPassword) validateConfirmPassword(password, e.target.value);
                }}
                onBlur={() => validateConfirmPassword(password, confirmPassword)}
                required
                placeholder="confirm password"
                className={`form-control ${validationErrors.confirmPassword ? "is-invalid" : ""}`}
              />
              <div
                className="invalid-feedback"
                role="alert"
                aria-live="polite"
                style={{
                  display: "block",
                  visibility: validationErrors.confirmPassword ? "visible" : "hidden",
                  minHeight: "1.25rem",
                }}
              >
                {validationErrors.confirmPassword || "\u00A0"}
              </div>
            </div>
            <div
              className="alert alert-danger"
              role="alert"
              aria-live="polite"
              style={{
                display: "block",
                visibility: registerError ? "visible" : "hidden",
                minHeight: "1.25rem",
              }}
            >
              {registerError || "\u00A0"}
            </div>
            <Button type="submit" variant="primary" className="w-100" disabled={loading}>
              {loading ? "registering..." : "register"}
            </Button>
          </form>
        </div>
      </div>
    );
};

export default RegisterForm;
