import { useEffect, useState } from "react";

import { logout } from "../api/auth.api"
import { getUserMe, updateUser, deleteUser } from "../api/users.api";
import Navbar from "../components/Navbar";
import AvatarWithText from "../components/AvatarWithText";
import ChangePasswordForm from "../features/users/ChangePasswordForm";
import DeleteAccount from "../features/users/DeleteAccount";


const SettingsPage = () => {
  const [user, setUser] = useState(null);

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

  const handleDeleteAccount = async () => {
    if (!user) return;
    const confirmed = window.confirm("Are you sure you want to delete your account? This action cannot be undone.");
    if (!confirmed) return;
    await deleteUser(user.id);
    logout();
    window.location.reload();
  };

  return (
    <>
      <Navbar />
      <h1>settings</h1>
      <AvatarWithText text={user ? user.email : "..."} />
      <ChangePasswordForm onChangePassword={handleChangePassword} />
      <DeleteAccount onDeleteAccount={handleDeleteAccount} />
    </>
  );
};

export default SettingsPage;