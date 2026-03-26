import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";

import { getCategories } from "../../api/categories.api";
import Button from "../../components/Button";
import useTrValidation from "../../hooks/useTrValidation";


const initialState = {
    type: "",
    category: "",
    date: "",
    value: "",
    comment: ""
};

const TrAddModal = ({ open, onClose, typeOptions = [], onAdd, className}) => {
  const [form, setForm] = useState(initialState);
  const [categoryOptions, setCategoryOptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [addError, setAddError] = useState(null);
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setAddError(null);

    if (!validateDate(form.date) || !validateValue(form.value) || !validateComment(form.comment)) {
      return;
    }

    setLoading(true);

    try {
      if (onAdd) await onAdd(form);
      if (onClose) onClose();
    } catch (err) {
      const status = err?.response?.status;
      const data = err?.response?.data;
      const backendMsg =
        data?.detail || data?.message || (typeof data === "string" ? data : null);

      if (status === 401) {
        setAddError(backendMsg || "unauthorized - please log in");
      } else if (status === 403) {
        setAddError(backendMsg || "forbidden - you don't have permission to perform this action");
      } else if (status === 404) {
        setAddError(backendMsg || "not found - the requested resource was not found");
      } else if (status === 409) {
        setAddError(backendMsg || "conflict - the request could not be completed due to a conflict with the current state of the resource");
      } else if (status === 422) {
        setAddError(backendMsg || "validation error - please check your input");
      } else if (status >= 500) {
        setAddError(backendMsg || "server error - please try again later");
      } else if (err?.request) {
        setAddError("network error - please check your connection");
      } else {
        setAddError(err?.message || "an unexpected error occurred");
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
              <h1>add transaction</h1>
              <Button onClick={onClose} icon={IoCloseOutline} variant="secondary" />
            </div>

            <form onSubmit={handleSubmit} aria-busy={loading}>

              <div className="modal-body">
                <label htmlFor="type" className="form-label">type: *</label>
                <select 
                  id="type"
                  name="type" 
                  value={form.type} 
                  onChange={handleChange}
                  className="form-select mb-3"
                >
                  {typeOptions.map(opt => (
                  <option key={opt.id} value={opt.id}>{opt.name}</option>
                  ))}
                </select>
                <label htmlFor="category" className="form-label">category:</label>
                <select
                  id="category"
                  name="category" 
                  value={form.category} 
                  onChange={handleChange}
                  className="form-select mb-3"
                >
                  <option value="">-- select category --</option>
                  {categoryOptions.map(opt => (
                  <option key={opt.id} value={opt.id}>{opt.name}</option>
                  ))}
                </select>
                <label htmlFor="date" className="form-label">date: *</label> 
                <input 
                  id="date"
                  type="date" 
                  name="date" 
                  value={form.date} 
                  onChange={(e) => {
                    handleChange(e);
                    if (validationErrors.date) validateDate(e.target.value);
                  }}
                  onBlur={() => validateDate(form.date)}
                  required
                  className={`form-control mb-1 ${validationErrors.date ? "is-invalid" : ""}`}
                />
                <div
                  className="invalid-feedback"
                  role="alert"
                  aria-live="polite"
                  style={{
                    display: "block",
                    visibility: validationErrors.date ? "visible" : "hidden",
                    minHeight: "1.25rem",
                  }}
                >
                  {validationErrors.date || "\u00A0"}
                </div>
                <label htmlFor="value" className="form-label">value: *</label>
                <input
                  id="value"
                  type="number" 
                  name="value" 
                  value={form.value} 
                  onChange={(e) => {
                    handleChange(e);
                    if (validationErrors.value) validateValue(e.target.value);
                  }}
                  onBlur={() => validateValue(form.value)}
                  required
                  className={`form-control mb-1 ${validationErrors.value ? "is-invalid" : ""}`}
                />
                <div
                  className="invalid-feedback"
                  role="alert"
                  aria-live="polite"
                  style={{
                    display: "block",
                    visibility: validationErrors.value ? "visible" : "hidden",
                    minHeight: "1.25rem",
                  }}
                >
                  {validationErrors.value || "\u00A0"}
                </div>
                <label htmlFor="comment" className="form-label">comment:</label>
                <input
                  id="comment"
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
                    visibility: addError ? "visible" : "hidden",
                    minHeight: "1.25rem",
                  }}
                >
                  {addError || "\u00A0"}
                </div>
                <Button type="submit" variant="primary" disabled={loading}>
                  {loading ? "adding..." : "add"}
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

export default TrAddModal;
