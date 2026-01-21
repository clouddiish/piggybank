import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";
import { FiTrash } from "react-icons/fi";

import { getCategory } from "../../api/categories.api";
import Button from "../../components/Button";


const initialState = {
    type: "",
    name: "",
};

const CaEditModal = ({ open, onClose, categoryId, typeOptions = [], onEdit, onDelete}) => {
  const [form, setForm] = useState(initialState);

  useEffect(() => {
    if (open && categoryId) {

      getCategory(categoryId).then(res => {
        setForm({...initialState, 
          type: res.data.type_id || "",
          name: res.data.name || "",
        });
      });
    }
  }, [open, categoryId]);

  useEffect(() => {
    if (open && typeOptions.length > 0) {
      const expenseTypeId = typeOptions.find(opt => opt.name === "expense")?.id || "";
      setForm({ ...initialState, type: expenseTypeId });
    }
  }, [open, typeOptions]);

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
        <label>type: 
        <select name="type" value={form.type} onChange={handleChange}>
          {typeOptions.map(opt => (
          <option key={opt.id} value={opt.id}>{opt.name}</option>
          ))}
        </select>
        </label>
        <label>name: <input type="text" name="name" value={form.name} onChange={handleChange} /></label>
        <Button type="submit" variant="primary">save</Button>
        <Button type="button" onClick={handleDelete} variant="secondary" icon={FiTrash}>delete</Button>
      </form>
    </>
  );
};

export default CaEditModal;