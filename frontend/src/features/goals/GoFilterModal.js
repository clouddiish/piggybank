import { useState } from "react";
import { IoCloseOutline } from "react-icons/io5";

import Button from "../../components/Button";


const GoFilterModal = ({ open, onClose, typeOptions = [], categoryOptions = [], onFilter }) => {
  const initialState = {
    startDateFrom: "",
    startDateTo: "",
    endDateFrom: "",
    endDateTo: "",
    type: "",
    category: "",
    targetValueFrom: "",
    targetValueTo: "",
    name: ""
  };
  const [form, setForm] = useState(initialState);

  if (!open) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleClear = () => {
    setForm(initialState);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onFilter) onFilter(form);
    if (onClose) onClose();
  };

  return (
    <>
      <Button onClick={onClose} icon={IoCloseOutline} variant="secondary" />
      <h1>filter goals</h1>
      <form onSubmit={handleSubmit}>
        <label>start date from: <input type="date" name="startDateFrom" value={form.startDateFrom} onChange={handleChange} /></label>
        <label>start date to: <input type="date" name="startDateTo" value={form.startDateTo} onChange={handleChange} /></label>
        <label>end date from: <input type="date" name="endDateFrom" value={form.endDateFrom} onChange={handleChange} /></label>
        <label>end date to: <input type="date" name="endDateTo" value={form.endDateTo} onChange={handleChange} /></label>
        <label>type: 
        <select name="type" value={form.type} onChange={handleChange}>
          <option value="">-- select type --</option>
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
        <label>target value from: <input type="number" name="targetValueFrom" value={form.targetValueFrom} onChange={handleChange} /></label>
        <label>target value to: <input type="number" name="targetValueTo" value={form.targetValueTo} onChange={handleChange} /></label>
        <label>name contains: <input type="text" name="name" value={form.name} onChange={handleChange} /></label>
        <Button type="button" variant="secondary" onClick={handleClear}>clear all</Button>
        <Button type="submit" variant="primary">filter</Button>
      </form>
    </>
  );
};

export default GoFilterModal;
