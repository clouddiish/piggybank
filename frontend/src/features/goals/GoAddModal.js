import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";

import { getCategories } from "../../api/categories.api";
import Button from "../../components/Button";


const GoAddModal = ({ open, onClose, typeOptions = [], onAdd }) => {
  const initialState = {
    type: "",
    category: "",
    name: "",
    start_date: "",
    end_date: "",
    target_value: "",
  };
  const [form, setForm] = useState(initialState);
  const [ categoryOptions, setCategoryOptions ] = useState([]);

  useEffect(() => {
    if (open && typeOptions.length > 0) {
      const expenseTypeId = typeOptions.find(opt => opt.name === "expense")?.id || "";
      setForm({ ...initialState, type: expenseTypeId });
    }
  }, [open, typeOptions]);

  useEffect(() => {
    if (form.type) {
      getCategories({ type_id: form.type }).then(res => setCategoryOptions(res.data));
    } else {
      setCategoryOptions([]);
    }
  }, [form.type]);

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
      <h1>add goal</h1>
      <form onSubmit={handleSubmit}>
        <label>type: 
        <select name="type" value={form.type} onChange={handleChange}>
          {typeOptions.map(opt => (
          <option key={opt.id} value={opt.id}>{opt.name}</option>
          ))}
        </select>
        </label>
        <label>category: 
        <select name="category" value={form.category} onChange={handleChange}>
          <option value="">-- select category --</option>
          {categoryOptions.map(opt => (
          <option key={opt.id} value={opt.id}>{opt.name}</option>
          ))}
        </select>
        </label>
        <label>name: <input type="text" name="name" value={form.name} onChange={handleChange} /></label>
        <label>start date: <input type="date" name="start_date" value={form.start_date} onChange={handleChange} /></label>
        <label>end date: <input type="date" name="end_date" value={form.end_date} onChange={handleChange} /></label>
        <label>target value: <input type="number" name="target_value" value={form.target_value} onChange={handleChange} /></label>
        <Button type="submit" variant="primary">add</Button>
      </form>
    </>
  );
};

export default GoAddModal;
