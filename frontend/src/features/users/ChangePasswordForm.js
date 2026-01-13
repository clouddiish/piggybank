import { useState } from "react";
import { FiEdit } from "react-icons/fi";

import Button from "../../components/Button";


const ChangePasswordForm = ({ onChangePassword }) => {
	const [oldPassword, setOldPassword] = useState("");
	const [newPassword, setNewPassword] = useState("");

	const handleSubmit = async (e) => {
		e.preventDefault();
		await onChangePassword(oldPassword, newPassword);
	};

	return (
        <>
            <h2>change password</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="password"
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                    required
                    placeholder="old password"
                />
                <input
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                    placeholder="new password"
                />
                <Button type="submit" variant="secondary" icon={FiEdit}>change password</Button>
            </form>
        </>
	);
};

export default ChangePasswordForm;
