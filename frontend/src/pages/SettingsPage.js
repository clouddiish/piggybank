import { useEffect, useState } from "react";

import { logout } from "../api/auth.api"
import { getUserMe, updateUser, deleteUser } from "../api/users.api";
import Navbar from "../components/Navbar";
import AvatarWithText from "../components/AvatarWithText";
import ChangePasswordForm from "../features/users/ChangePasswordForm";
import DeleteAccount from "../features/users/DeleteAccount";
import ConfirmModal from "../components/ConfirmModal";


const SettingsPage = () => {
  const [user, setUser] = useState(null);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    getUserMe().then((res) => setUser(res.data)).catch(() => setUser(null));
  }, []);

  const handleChangePassword = async (oldPassword, newPassword) => {
    if (!user) return;
    const updatedUser = { 
      email: user.email,
      role_id: user.role_id,
      old_password: oldPassword, 
      new_password: newPassword };
    await updateUser(user.id, updatedUser);
    logout();
    window.location.reload();
  };

  const openDeleteConfirm = () => {
    if (!user) return;
    setIsConfirmOpen(true);
  };

  const confirmDeleteAccount = async () => {
    if (!user) return;
    setIsDeleting(true);
    try {
      await deleteUser(user.id);
      logout();
      window.location.reload();
    } finally {
      setIsDeleting(false);
      setIsConfirmOpen(false);
    }
  };

  return (
    <>
      <Navbar />
      <div className="mx-md-5 mx-2 py-3 align-items-center">
        <h1 className="mb-3">settings</h1>
        <AvatarWithText className="mb-5" text={user ? user.email : "..."} />
        <ChangePasswordForm className="mb-5" onChangePassword={handleChangePassword} />
        <DeleteAccount className="mb-5" onDeleteAccount={openDeleteConfirm} />
        <ConfirmModal
          open={isConfirmOpen}
          title="delete account"
          message="are you sure you want to delete your account? this action cannot be undone"
          onClose={() => setIsConfirmOpen(false)}
          onConfirm={confirmDeleteAccount}
          confirmLabel="delete"
          cancelLabel="cancel"
          loading={isDeleting}
        />
      </div>
    </>
  );
};

export default SettingsPage;