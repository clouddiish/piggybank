import { FiTrash } from "react-icons/fi";

import Button from "../../components/Button";


const DeleteAccount = ({ onDeleteAccount }) => {
	const handleDeleteAccount = async (e) => {
		e.preventDefault();
		await onDeleteAccount();
	};

	return (
    <>
      <h2>delete account</h2>
      <Button onClick={handleDeleteAccount} variant="secondary" icon={FiTrash}>delete account</Button>
    </>
	);
};

export default DeleteAccount;
