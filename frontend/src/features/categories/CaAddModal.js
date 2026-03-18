import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";

import Button from "../../components/Button";

const initialState = {
    type: "",
    name: "",
};

const CaAddModal = ({ open, onClose, typeOptions = [], onAdd, className }) => {
  const [form, setForm] = useState(initialState);

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
      <div className={cls} tabIndex="-1" role="dialog" aria-modal="true" style={style}>
        <div className="modal-dialog">
          <div className="modal-content">

            <div className="modal-header justify-content-between">
              <h1>add category</h1>
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
                
                <label htmlFor="name" className="form-label">name:</label>
                <input 
                  type="text" 
                  name="name" 
                  value={form.name} 
                  onChange={handleChange}
                  className="form-control"
                  id="name"
                />
              </div>

              <div className="modal-footer">
                <Button type="submit" variant="primary">add</Button>
              </div>

            </form>

          </div>
        </div>
      </div>

      <div className="modal-backdrop fade show"></div>
    </>
  );
};

export default CaAddModal;
