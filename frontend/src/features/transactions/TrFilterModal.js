import { useEffect, useState } from "react";
import { IoCloseOutline } from "react-icons/io5";

import Button from "../../components/Button";
import useTrValidation from "../../hooks/useTrValidation";


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
  const [loading, setLoading] = useState(false);
  const [filterError, setFilterError] = useState(null);
  const { validationErrors, validateDate, validateValue, validateComment } = useTrValidation();

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
    setFilterError(null);

    const isDateFromValid = validateDate(form.dateFrom, false, "dateFrom");
    const isDateToValid = validateDate(form.dateTo, false, "dateTo");
    const isValueFromValid = validateValue(form.valueFrom, false, "valueFrom");
    const isValueToValid = validateValue(form.valueTo, false, "valueTo");
    const isCommentValid = validateComment(form.comment, false);

    if (!isDateFromValid || !isDateToValid || !isValueFromValid || !isValueToValid || !isCommentValid) {
      return;
    }

    setLoading(true);

    try {
      if (onFilter) onFilter(form);
      if (onClose) onClose();
    } catch (err) {
      const status = err?.response?.status;
      const data = err?.response?.data;
      const backendMsg =
        data?.detail || data?.message || (typeof data === "string" ? data : null);
      
      if (status === 401) {
        setFilterError(backendMsg || "unauthorized - please log in");
      } else if (status === 422) {
        setFilterError(backendMsg || "validation error - please check your input");
      } else if (status >= 500) {
        setFilterError(backendMsg || "server error - please try again later");
      } else if (err?.request) {
        setFilterError("network error - please check your connection");
      } else {
        setFilterError(err?.message || "an unexpected error occurred");
      }
    } finally {
      setLoading(false);
    }
    
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

            <form onSubmit={handleSubmit} aria-busy={loading}>

              <div className="modal-body">
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
                  <label htmlFor="date-from" className="form-label">date from:</label>
                  <input
                    id="date-from"
                    type="date" 
                    name="dateFrom" 
                    value={form.dateFrom} 
                    onChange={(e) => {
                      handleChange(e);
                      if (validationErrors.dateFrom) validateDate(e.target.value, false, "dateFrom");
                    }}
                    onBlur={() => validateDate(form.dateFrom, false, "dateFrom")}
                    className={`form-control mb-1 ${validationErrors.dateFrom ? "is-invalid" : ""}`}
                  />
                  <div
                    className="invalid-feedback"
                    role="alert"
                    aria-live="polite"
                    style={{
                      display: "block",
                      visibility: validationErrors.dateFrom ? "visible" : "hidden",
                      minHeight: "1.25rem",
                    }}
                  >
                    {validationErrors.dateFrom || "\u00A0"}
                  </div>
                  <label htmlFor="date-to" className="form-label">date to:</label>
                  <input 
                    id="date-to"
                    type="date" 
                    name="dateTo" 
                    value={form.dateTo} 
                    onChange={(e) => {
                      handleChange(e);
                      if (validationErrors.dateTo) validateDate(e.target.value, false, "dateTo");
                    }}
                    onBlur={() => validateDate(form.dateTo, false, "dateTo")}
                    className={`form-control mb-1 ${validationErrors.dateTo ? "is-invalid" : ""}`}
                  />
                  <div
                    className="invalid-feedback"
                    role="alert"
                    aria-live="polite"
                    style={{
                      display: "block",
                      visibility: validationErrors.dateTo ? "visible" : "hidden",
                      minHeight: "1.25rem",
                    }}
                  >
                    {validationErrors.dateTo || "\u00A0"}
                  </div>
                  <label htmlFor="value-from" className="form-label">value from:</label> 
                  <input 
                    id="value-from"
                    type="number" 
                    name="valueFrom" 
                    value={form.valueFrom} 
                    onChange={(e) => {
                      handleChange(e);
                      if (validationErrors.valueFrom) validateValue(e.target.value, false, "valueFrom");
                    }}
                    onBlur={() => validateValue(form.valueFrom, false, "valueFrom")}
                    className={`form-control mb-1 ${validationErrors.valueFrom ? "is-invalid" : ""}`}
                  />
                  <div
                    className="invalid-feedback"
                    role="alert"
                    aria-live="polite"
                    style={{
                      display: "block",
                      visibility: validationErrors.valueFrom ? "visible" : "hidden",
                      minHeight: "1.25rem",
                    }}
                  >
                    {validationErrors.valueFrom || "\u00A0"}
                  </div>
                  <label htmlFor="value-to" className="form-label">value to:</label>
                  <input 
                    id="value-to"
                    type="number" 
                    name="valueTo" 
                    value={form.valueTo} 
                    onChange={(e) => {
                      handleChange(e);
                      if (validationErrors.valueTo) validateValue(e.target.value, false, "valueTo");
                    }}
                    onBlur={() => validateValue(form.valueTo, false, "valueTo")}
                    className={`form-control mb-1 ${validationErrors.valueTo ? "is-invalid" : ""}`}
                  />
                  <div
                    className="invalid-feedback"
                    role="alert"
                    aria-live="polite"
                    style={{
                      display: "block",
                      visibility: validationErrors.valueTo ? "visible" : "hidden",
                      minHeight: "1.25rem",
                    }}
                  >
                    {validationErrors.valueTo || "\u00A0"}
                  </div>
                  <label htmlFor="comment-contains" className="form-label">comment contains:</label>
                  <input 
                    id="comment-contains"
                    type="text" 
                    name="comment" 
                    value={form.comment} 
                    onChange={(e) => {
                      handleChange(e);
                      if (validationErrors.comment) validateComment(e.target.value);
                    }}
                    onBlur={() => validateComment(form.comment)}
                    className={`form-control ${validationErrors.comment ? "is-invalid" : ""}`}
                  />
                  <div
                    className="invalid-feedback"
                    role="alert"
                    aria-live="polite"
                    style={{
                      display: "block",
                      visibility: validationErrors.comment ? "visible" : "hidden",
                      minHeight: "1.25rem",
                    }}
                  >
                    {validationErrors.comment || "\u00A0"}
                  </div>
                </div>
              
                <div className="modal-footer">
                  <div
                    className="alert alert-danger"
                    role="alert"
                    aria-live="polite"
                    style={{
                      display: "block",
                      visibility: filterError ? "visible" : "hidden",
                      minHeight: "1.25rem",
                    }}
                  >
                    {filterError || "\u00A0"}
                  </div>
                  <Button type="button" variant="secondary" onClick={handleClear}>clear all</Button>
                  <Button type="submit" variant="primary" disabled={loading}>
                    {loading ? "filtering..." : "filter"}
                  </Button>
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
