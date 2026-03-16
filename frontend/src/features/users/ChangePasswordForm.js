import { useState } from "react";
import { FiEdit } from "react-icons/fi";

import Button from "../../components/Button";


const ChangePasswordForm = ({ onChangePassword, className }) => {
	const [oldPassword, setOldPassword] = useState("");
	const [newPassword, setNewPassword] = useState("");
  const cls = ["row", className].filter(Boolean).join(" ");

	const handleSubmit = async (e) => {
		e.preventDefault();
		await onChangePassword(oldPassword, newPassword);
	};

	return (
    <div className={cls}>
      <h2 className="mb-3">change password</h2>
      <div className="col-12 col-md-6">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="old-password" class="form-label">old password</label>
            <input
              type="password"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              required
              placeholder="old password"
              className="form-control"
              id="old-password"
            />
          </div>
          <div className="mb-3">
            <label htmlFor="new-password" class="form-label">new password</label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              placeholder="new password"
              className="form-control"
              id="new-password"
            />
          </div>
          <Button type="submit" variant="primary" className="w-100" icon={FiEdit}>change password</Button>
        </form>
      </div>
    </div>
	);
};

export default ChangePasswordForm;
