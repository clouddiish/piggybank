import { useState, useRef } from "react";

import Button from "../../components/Button";


const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const LoginForm = ({ onLogin }) => {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [emailError, setEmailError] = useState(null);
  const [passwordError, setPasswordError] = useState(null);
  const emailRef = useRef(null);
  const passwordRef = useRef(null);

  const validateEmail = (value = email) => {
    if (!value) {
      setEmailError("email is required");
      return false;
    }
    if (!emailRegex.test(value)) {
      setEmailError("enter a valid email address");
      return false;
    }
    setEmailError(null);
    return true;
  };

  const validatePassword = (value = password) => {
    if (!value) {
      setPasswordError("password is required");
      return false;
    }
    setPasswordError(null);
    return true;
  };

	const handleSubmit = async (e) => {
		e.preventDefault();
    setError(null);

    if (!validateEmail()) {
      emailRef.current?.focus();
      return;
    }

    if (!validatePassword()) {
      passwordRef.current?.focus();
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
        setError(backendMsg || "Invalid email or password.");
      } else if (status >= 500) {
        setError(backendMsg || "Server error - please try again later.");
      } else if (err?.request) {
        setError("Network error - please check your connection.");
      } else {
        setError(err?.message || "An unexpected error occurred.");
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
              ref={emailRef}
              type="email"
              value={email}
              onChange={(e) => { setEmail(e.target.value); if (emailError) validateEmail(e.target.value); }}
              onBlur={() => validateEmail()}
              required
              placeholder="email@example.com"
              className={`form-control ${emailError ? "is-invalid" : ""}`}
            />
            <div
              className="invalid-feedback"
              role="alert"
              aria-live="polite"
              style={{
                display: "block",
                visibility: emailError ? "visible" : "hidden",
                minHeight: "1.25rem",
              }}
            >
              {emailError || "\u00A0"}
            </div>
          </div>
          <div className="mb-1">
            <label htmlFor="password" className="form-label">password</label>
            <input
              id="password"
              ref={passwordRef}
              type="password"
              value={password}
              onChange={(e) => { setPassword(e.target.value); if (passwordError) validatePassword(e.target.value); }}
              onBlur={() => validatePassword()}
              required
              placeholder="password"
              className={`form-control ${passwordError ? "is-invalid" : ""}`}
            />
            <div
              className="invalid-feedback"
              role="alert"
              aria-live="polite"
              style={{
                display: "block",
                visibility: passwordError ? "visible" : "hidden",
                minHeight: "1.25rem",
              }}
            >
              {passwordError || "\u00A0"}
            </div>
          </div>
          <div 
            className="alert alert-danger" 
            role="alert" 
            aria-live="polite"
            style={{
              display: "block",
              visibility: error ? "visible" : "hidden",
              minHeight: "1.25rem",
            }}
          >
            {error || "\u00A0"}
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
