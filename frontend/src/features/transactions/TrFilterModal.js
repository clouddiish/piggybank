import { useEffect, useState } from "react";
import { IoCloseOutline } from "react-icons/io5";

import Button from "../../components/Button";


const initialState = {
    dateFrom: "",
    dateTo: "",
    type: "",
    category: "",
    valueFrom: "",
    valueTo: "",
    comment: ""
};

const TrFilterModal = ({ open, onClose, typeOptions = [], categoryOptions = [], onFilter, className }) => {
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
              <h1>filter transactions</h1>
              <Button onClick={onClose} icon={IoCloseOutline} variant="secondary" />
            </div>

            <form onSubmit={handleSubmit}>

              <div className="modal-body">
                  <label htmlFor="date-from" className="form-label">date from:</label>
                  <input 
                    type="date" 
                    name="dateFrom" 
                    value={form.dateFrom} 
                    onChange={handleChange}
                    className="form-control mb-3"
                    id="date-from"
                  />
                  <label htmlFor="date-to" className="form-label">date to:</label>
                  <input 
                    type="date" 
                    name="dateTo" 
                    value={form.dateTo} 
                    onChange={handleChange}
                    className="form-control mb-3"
                    id="date-to"
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
                  <label htmlFor="value-from" className="form-label">value from:</label> 
                  <input 
                    type="number" 
                    name="valueFrom" 
                    value={form.valueFrom} 
                    onChange={handleChange}
                    className="form-control mb-3"
                    id="value-from"
                  />
                  <label htmlFor="value-to" className="form-label">value to:</label>
                  <input 
                    type="number" 
                    name="valueTo" 
                    value={form.valueTo} 
                    onChange={handleChange}
                    className="form-control mb-3"
                    id="value-to" 
                  />
                  <label htmlFor="comment-contains" className="form-label">comment contains:</label>
                  <input 
                    type="text" 
                    name="comment" 
                    value={form.comment} 
                    onChange={handleChange}
                    className="form-control"
                    id="comment-contains" 
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

export default TrFilterModal;
