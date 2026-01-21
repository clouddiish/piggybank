import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";

import { getCategories } from "../../api/categories.api";
import Button from "../../components/Button";


const initialState = {
    type: "",
    category: "",
    date: "",
    value: "",
    comment: ""
};

const TrAddModal = ({ open, onClose, typeOptions = [], onAdd }) => {
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
      <h1>add transaction</h1>
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
        <label>date: <input type="date" name="date" value={form.date} onChange={handleChange} /></label>
        <label>value: <input type="number" name="value" value={form.value} onChange={handleChange} /></label>
        <label>comment: <input type="text" name="comment" value={form.comment} onChange={handleChange} /></label>
        <Button type="submit" variant="primary">add</Button>
      </form>
    </>
  );
};

export default TrAddModal;
