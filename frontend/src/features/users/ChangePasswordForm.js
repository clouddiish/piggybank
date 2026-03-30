import { useState } from "react";
import { FiEdit } from "react-icons/fi";

import Button from "../../components/Button";
import useAuthValidation from "../../hooks/useAuthValidation";


const ChangePasswordForm = ({ onChangePassword, className }) => {
	const [oldPassword, setOldPassword] = useState("");
	const [newPassword, setNewPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [changeError, setChangeError] = useState(null);
  const { validationErrors, validatePassword } = useAuthValidation();

  const cls = ["row", className].filter(Boolean).join(" ");

	const handleSubmit = async (e) => {
		e.preventDefault();
    setChangeError(null);

    const isOldPasswordValid = validatePassword(oldPassword, "oldPassword");
    const isNewPasswordValid = validatePassword(newPassword, "newPassword");

    if (!isOldPasswordValid || !isNewPasswordValid) {
      return;
    }

    setLoading(true);

    try {
      await onChangePassword(oldPassword, newPassword);
    } catch (err) {
      const status = err?.response?.status;
      const data = err?.response?.data;
      const backendMsg =
        data?.detail || data?.message || (typeof data === "string" ? data : null);

      if (status === 401) {
        setChangeError(backendMsg || "unauthorized - please log in");
      } else if (status === 403) {
        setChangeError(backendMsg || "forbidden - you don't have permission to perform this action");
      } else if (status === 404) {
        setChangeError(backendMsg || "user not found");
      } else if (status === 422) {
        setChangeError(backendMsg || "invalid input - please check your data");
      } else if (status >= 500) {
        setChangeError(backendMsg || "server error - please try again later");
      } else if (err?.request) {
        setChangeError("network error - please check your connection");
      } else {
        setChangeError(err?.message || "an unexpected error occurred");
      }
    } finally {
      setLoading(false);
    }
		
	};

	return (
    <div className={cls}>
      <h2 className="mb-3">change password</h2>
      <div className="col-12 col-md-6">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="old-password" className="form-label">old password</label>
            <input
              id="old-password"
              type="password"
              value={oldPassword}
              onChange={(e) => {
                setOldPassword(e.target.value);
                if (validationErrors.oldPassword) validatePassword(e.target.value, "oldPassword");
              }}
              onBlur={() => validatePassword(oldPassword, "oldPassword")}
              required
              placeholder="old password"
              className={`form-control ${validationErrors.oldPassword ? "is-invalid" : ""}`}
            />
            <div
              className="invalid-feedback"
              role="alert"
              aria-live="polite"
              style={{
                display: "block",
                visibility: validationErrors.oldPassword ? "visible" : "hidden",
                minHeight: "1.25rem",
              }}
            >
              {validationErrors.oldPassword || "\u00A0"}
            </div>
          </div>
          <div className="mb-3">
            <label htmlFor="new-password" className="form-label">new password</label>
            <input
              id="new-password"
              type="password"
              value={newPassword}
              onChange={(e) => {
                setNewPassword(e.target.value);
                if (validationErrors.newPassword) validatePassword(e.target.value, "newPassword");
              }}
              onBlur={() => validatePassword(newPassword, "newPassword")}
              required
              placeholder="new password"
              className={`form-control ${validationErrors.newPassword ? "is-invalid" : ""}`}
            />
            <div
              className="invalid-feedback"
              role="alert"
              aria-live="polite"
              style={{
                display: "block",
                visibility: validationErrors.newPassword ? "visible" : "hidden",
                minHeight: "1.25rem",
              }}
            >
              {validationErrors.newPassword || "\u00A0"}
            </div>
          </div>
          <div
            className="alert alert-danger"
            role="alert"
            aria-live="polite"
            style={{
              display: "block",
              visibility: changeError ? "visible" : "hidden",
              minHeight: "1.25rem",
            }}
          >
            {changeError || "\u00A0"}
          </div>
          <Button type="submit" variant="primary" className="w-100" icon={FiEdit} disabled={loading}>
            {loading ? "changing password..." : "change password"}
          </Button>
        </form>
      </div>
    </div>
	);
};

export default ChangePasswordForm;
