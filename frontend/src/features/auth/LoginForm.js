import { useState } from "react";

import Button from "../../components/Button";
import useAuthValidation from "../../hooks/useAuthValidation";


const LoginForm = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [loginError, setLoginError] = useState(null);
  const { validationErrors, validateEmail, validatePassword } = useAuthValidation();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoginError(null);

    if (!validateEmail(email) || !validatePassword(password)) {
      return;
    }

    setLoading(true);

    try {
      await onLogin(email, password);
    } catch (err) {
      const status = err?.response?.status;
      const data = err?.response?.data;
      const backendMsg =
        data?.detail || data?.message || (typeof data === "string" ? data : null);

      if (status === 401) {
        setLoginError(backendMsg || "invalid email or password");
      } else if (status >= 500) {
        setLoginError(backendMsg || "server error - please try again later");
      } else if (err?.request) {
        setLoginError("network error - please check your connection");
      } else {
        setLoginError(err?.message || "an unexpected error occurred");
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
          <div
            className="alert alert-danger"
            role="alert"
            aria-live="polite"
            style={{
              display: "block",
              visibility: loginError ? "visible" : "hidden",
              minHeight: "1.25rem",
            }}
          >
            {loginError || "\u00A0"}
          </div>
          <Button type="submit" variant="primary" className="w-100" disabled={loading}>
            {loading ? "logging in..." : "login"}
          </Button>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;