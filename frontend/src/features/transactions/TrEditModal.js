import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";
import { FiTrash } from "react-icons/fi";

import { getTransaction } from "../../api/transactions.api";
import { getCategories } from "../../api/categories.api";
import Button from "../../components/Button";


const TrEditModal = ({ open, onClose, transactionId, typeOptions = [], onEdit, onDelete}) => {
  const initialState = {
    type: "",
    category: "",
    date: "",
    value: "",
    comment: ""
  };
  const [form, setForm] = useState(initialState);
  const [ categoryOptions, setCategoryOptions ] = useState([]);

  useEffect(() => {
    if (open && transactionId) {

      getTransaction(transactionId).then(res => {
        setForm({...initialState, 
          type: res.data.type_id || "",
          category: res.data.category_id || "",
          date: res.data.date || "",
          value: res.data.value || "",
          comment: res.data.comment || ""
        });
      });
    }
  }, [open, transactionId]);

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

  if (!open) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => {
      if (name === "type") {
        return { ...prev, [name]: value, category: "" };
      }
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
    if (onDelete) onDelete(transactionId);
    if (onClose) onClose();
  }

  return (
    <>
      <Button onClick={onClose} icon={IoCloseOutline} variant="secondary" />
      <h1>edit transaction</h1>
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
        <Button type="submit" variant="primary">save</Button>
        <Button type="button" onClick={handleDelete} variant="secondary" icon={FiTrash}>delete</Button>
      </form>
    </>
  );
};

export default TrEditModal;
