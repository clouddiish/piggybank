import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";

import Button from "../../components/Button";

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

const GoFilterModal = ({ open, onClose, typeOptions = [], categoryOptions = [], onFilter, className }) => {
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

  if (!open) return null;

  return (
    <>
      <div className={cls} tabIndex="-1" role="dialog" aria-modal="true" style={style}>
        <div className="modal-dialog">
          <div className="modal-content">

            <div className="modal-header justify-content-between">
              <h1>filter goals</h1>
              <Button onClick={onClose} icon={IoCloseOutline} variant="secondary" />
            </div>

            <form onSubmit={handleSubmit}>

              <div className="modal-body">
                <label htmlFor="start-date-from" className="form-label">start date from:</label>
                <input 
                  type="date" 
                  name="startDateFrom" 
                  value={form.startDateFrom} 
                  onChange={handleChange}
                  className="form-control mb-3"
                  id="start-date-from"
                />
                <label htmlFor="start-date-to" className="form-label">start date to:</label>
                <input 
                  type="date" 
                  name="startDateTo" 
                  value={form.startDateTo} 
                  onChange={handleChange}
                  className="form-control mb-3"
                  id="start-date-to"
                />
                <label htmlFor="end-date-from" className="form-label">end date from:</label>
                <input 
                  type="date" 
                  name="endDateFrom" 
                  value={form.endDateFrom} 
                  onChange={handleChange}
                  className="form-control mb-3"
                  id="end-date-from"
                />
                <label htmlFor="end-date-to" className="form-label">end date to:</label>
                <input 
                  type="date" 
                  name="endDateTo" 
                  value={form.endDateTo} 
                  onChange={handleChange}
                  className="form-control mb-3"
                  id="end-date-to"
                />
                <label htmlFor="type" className="form-label">type:</label>
                <select 
                  name="type" 
                  value={form.type} 
                  onChange={handleChange}
                  className="form-select mb-3"
                  id="type"
                >
                  <option value="">-- select type --</option>
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
                <label htmlFor="target-value-from" className="form-label">target value from:</label> 
                <input 
                  type="number" 
                  name="targetValueFrom" 
                  value={form.targetValueFrom} 
                  onChange={handleChange}
                  className="form-control mb-3"
                  id="target-value-from"
                />
                <label htmlFor="target-value-to" className="form-label">target value to:</label>
                <input 
                  type="number" 
                  name="targetValueTo" 
                  value={form.targetValueTo} 
                  onChange={handleChange} 
                  className="form-control mb-3"
                  id="target-value-to"
                />
                <label htmlFor="name-contains" className="form-label">name contains:</label>
                <input 
                  type="text" 
                  name="name" 
                  value={form.name} 
                  onChange={handleChange}
                  className="form-control"
                  id="name-contains"
                />
              </div>
              
              <div className="modal-footer">
                <Button type="button" variant="secondary" onClick={handleClear}>clear all</Button>
                <Button type="submit" variant="primary">filter</Button>
              </div>

            </form>

          </div>
        </div>
      </div>

      <div className="modal-backdrop fade show"></div>
    </>
  );
};

export default GoFilterModal;
