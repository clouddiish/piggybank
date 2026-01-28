import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";
import { FiTrash } from "react-icons/fi";

import { getCategory } from "../../api/categories.api";
import Button from "../../components/Button";


const initialState = {
    name: "",
};

const CaEditModal = ({ open, onClose, categoryId, onEdit, onDelete}) => {
  const [form, setForm] = useState(initialState);

  useEffect(() => {
    if (open && categoryId) {

      getCategory(categoryId).then(res => {
        setForm({...initialState, 
          name: res.data.name || "",
        });
      });
    }
  }, [open, categoryId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => {
      return { ...prev, [name]: value };
    }
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onEdit) onEdit(form);
    if (onClose) onClose();
  };

  const handleDelete = () => {
    if (onDelete) onDelete(categoryId);
    if (onClose) onClose();
  }

  if (!open) return null;

  return (
    <>
      <Button onClick={onClose} icon={IoCloseOutline} variant="secondary" />
      <h1>edit category</h1>
      <form onSubmit={handleSubmit}>
        <label>name: <input type="text" name="name" value={form.name} onChange={handleChange} /></label>
        <Button type="submit" variant="primary">save</Button>
        <Button type="button" onClick={handleDelete} variant="secondary" icon={FiTrash}>delete</Button>
      </form>
    </>
  );
};

export default CaEditModal;