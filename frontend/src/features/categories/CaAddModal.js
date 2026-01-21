import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";

import Button from "../../components/Button";

const initialState = {
    type: "",
    name: "",
  };

const CaAddModal = ({ open, onClose, typeOptions = [], onAdd }) => {
  const [form, setForm] = useState(initialState);

  useEffect(() => {
    if (open && typeOptions.length > 0) {
      const expenseTypeId = typeOptions.find(opt => opt.name === "expense")?.id || "";
      setForm({ ...initialState, type: expenseTypeId });
    }
  }, [open, typeOptions]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onAdd) onAdd(form);
    if (onClose) onClose();
  };
  
  if (!open) return null;

  return (
    <>
      <Button onClick={onClose} icon={IoCloseOutline} variant="secondary" />
      <h1>add category</h1>
      <form onSubmit={handleSubmit}>
        <label>type: 
        <select name="type" value={form.type} onChange={handleChange}>
          {typeOptions.map(opt => (
          <option key={opt.id} value={opt.id}>{opt.name}</option>
          ))}
        </select>
        </label>
        <label>name: <input type="text" name="name" value={form.name} onChange={handleChange} /></label>
        <Button type="submit" variant="primary">add</Button>
      </form>
    </>
  );
};

export default CaAddModal;
