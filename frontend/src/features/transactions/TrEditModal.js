import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";
import { FiTrash } from "react-icons/fi";

import { getTransaction } from "../../api/transactions.api";
import { getCategories } from "../../api/categories.api";
import Button from "../../components/Button";


const initialState = {
    type: "",
    category: "",
    date: "",
    value: "",
    comment: ""
};

const TrEditModal = ({ open, onClose, transactionId, typeOptions = [], onEdit, onDelete, className }) => {
  const [form, setForm] = useState(initialState);
  const [categoryOptions, setCategoryOptions] = useState([]);

  const cls = ["modal", "fade", open ? "show" : "", className].filter(Boolean).join(" ");
  const style = open ? { display: "block" } : undefined;

  useEffect(() => {
    if (open) {
      document.body.classList.add("modal-open");
    } else {
      document.body.classList.remove("modal-open");
    }
    return () => document.body.classList.remove("modal-open");
  }, [open]);

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

  if (!open) return null;

  return (
    <>
      <div className={cls} tabIndex="-1" role="dialog" aria-modal="true" style={style}>
        <div className="modal-dialog">
          <div className="modal-content">

            <div className="modal-header justify-content-between">
              <h1>edit transaction</h1>
              <Button onClick={onClose} icon={IoCloseOutline} variant="secondary" />
            </div>
            
            <form onSubmit={handleSubmit}>

              <div className="modal-body">
                <label htmlFor="type" className="form-label">type:</label>
                <select 
                  name="type" 
                  value={form.type} 
                  onChange={handleChange}
                  className="form-select mb-3"
                  id="type"
                >
                  {typeOptions.map(opt => (
                  <option key={opt.id} value={opt.id}>{opt.name}</option>
                  ))}
                </select>
                <label htmlFor="category" className="form-label">category:</label>
                <select 
                  name="category" 
                  value={form.category} 
                  onChange={handleChange}
                  className="form-select mb-3"
                  id="category"
                >
                  <option value="">-- select category --</option>
                  {categoryOptions.map(opt => (
                  <option key={opt.id} value={opt.id}>{opt.name}</option>
                  ))}
                </select>
                <label htmlFor="date" className="form-label">date:</label>
                <input 
                  type="date" 
                  name="date" 
                  value={form.date} 
                  onChange={handleChange}
                  className="form-control mb-3"
                  id="date"
                />
                <label htmlFor="value" className="form-label">value:</label> 
                <input 
                  type="number" 
                  name="value" 
                  value={form.value} 
                  onChange={handleChange}
                  className="form-control mb-3"
                  id="value"
                />
                <label htmlFor="comment" className="form-label">comment:</label> 
                <input 
                  type="text" 
                  name="comment" 
                  value={form.comment} 
                  onChange={handleChange}
                  className="form-control mb-3"
                  id="comment"
                />
              </div>
              
              <div className="modal-footer">
                <Button type="submit" variant="primary">save</Button>
                <Button type="button" onClick={handleDelete} variant="secondary" icon={FiTrash}>delete</Button>
              </div>

            </form>
        
            </div>
          </div>
        </div>

      <div className="modal-backdrop fade show"></div>
    </>
  );
};

export default TrEditModal;
