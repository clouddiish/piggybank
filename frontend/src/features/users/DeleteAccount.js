import { FiTrash } from "react-icons/fi";

import Button from "../../components/Button";


const DeleteAccount = ({ onDeleteAccount, className }) => {
	const cls = ["row", className].filter(Boolean).join(" ");

	const handleDeleteAccount = async (e) => {
		e.preventDefault();
		await onDeleteAccount();
	};

	return (
    <div className={cls}>
      <h2 className="mb-3">delete account</h2>
      <div className="col-12 col-md-6">
        <Button onClick={handleDeleteAccount} variant="primary" className="w-100" icon={FiTrash}>delete account</Button>
      </div>
    </div>
	);
};

export default DeleteAccount;
