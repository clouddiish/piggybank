import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";
import { FiTrash } from "react-icons/fi";

import { getGoal } from "../../api/goals.api";
import { getCategories } from "../../api/categories.api";
import Button from "../../components/Button";
import useGoValidation from "../../hooks/useGoValidation";


const initialState = {
    type: "",
    category: "",
    name: "",
    start_date: "",
    end_date: "",
    target_value: "",
};

const GoEditModal = ({ open, onClose, goalId, typeOptions = [], onEdit, onDelete, className }) => {
  const [form, setForm] = useState(initialState);
  const [categoryOptions, setCategoryOptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editError, setEditError] = useState(null);
  const { validationErrors, validateName, validateDate, validateEndDateAfterStartDate, validateValue } = useGoValidation();

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
    if (open && goalId) {

      getGoal(goalId).then(res => {
        setForm({...initialState, 
          type: res.data.type_id || "",
          category: res.data.category_id || "",
          name: res.data.name || "",
          start_date: res.data.start_date || "",
          end_date: res.data.end_date || "",
          target_value: res.data.target_value || ""
        });
      });
    }
  }, [open, goalId]);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setEditError(null);

    const isNameValid = validateName(form.name);
    const isStartDateValid = validateDate(form.start_date, true, "startDate");
    const isEndDateValid = validateDate(form.end_date, true, "endDate");
    const isEndAfterStartValid = validateEndDateAfterStartDate(form.start_date, form.end_date);
    const isTargetValueValid = validateValue(form.target_value);

    if (!isNameValid || !isStartDateValid || !isEndDateValid || !isEndAfterStartValid || !isTargetValueValid) {
      return;
    }

    setLoading(true);

    try {
      if (onEdit) await onEdit(form);
      if (onClose) onClose();
    } catch (err) { 
      const status = err?.response?.status;
      const data = err?.response?.data;
      const backendMsg =
        data?.detail || data?.message || (typeof data === "string" ? data : null);

      if (status === 401) {
        setEditError(backendMsg || "unauthorized - please log in");
      } else if (status === 403) {
        setEditError(backendMsg || "forbidden - you don't have permission to perform this action");
      } else if (status === 404) {
        setEditError(backendMsg || "not found - the requested resource was not found");
      } else if (status === 409) {
        setEditError(backendMsg || "conflict - the request could not be completed due to a conflict with the current state of the resource");
      } else if (status === 422) {
        setEditError(backendMsg || "validation error - please check your input");
      } else if (status >= 500) {
        setEditError(backendMsg || "server error - please try again later");
      } else if (err?.request) {
        setEditError("network error - please check your connection");
      } else {
        setEditError(err?.message || "an unexpected error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    try {
      if (onDelete) await onDelete(goalId);
      if (onClose) onClose();
    } catch (err) {
      const status = err?.response?.status;
      const data = err?.response?.data;
      const backendMsg =
        data?.detail || data?.message || (typeof data === "string" ? data : null);

      if (status === 401) {
        setEditError(backendMsg || "unauthorized - please log in");
      } else if (status === 403) {
        setEditError(backendMsg || "forbidden - you don't have permission to perform this action");
      } else if (status === 404) {
        setEditError(backendMsg || "not found - the requested resource was not found");
      } else if (status === 422) {
        setEditError(backendMsg || "validation error - please check your input");
      } else if (status >= 500) {
        setEditError(backendMsg || "server error - please try again later");
      } else if (err?.request) {
        setEditError("network error - please check your connection");
      } else {
        setEditError(err?.message || "an unexpected error occurred");
      }
    } finally {
      setLoading(false);
    } 
  }

  if (!open) return null;

  return (
    <>
      <div className={cls} tabIndex="-1" role="dialog" aria-modal="true" style={style}>
        <div className="modal-dialog">
          <div className="modal-content">

            <div className="modal-header justify-content-between">
              <h1>edit goal</h1>
              <Button onClick={onClose} icon={IoCloseOutline} variant="secondary" />
            </div>

            <form onSubmit={handleSubmit}>

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
                <label htmlFor="name" className="form-label">name: *</label>
                <input 
                  id="name"
                  type="text" 
                  name="name" 
                  value={form.name} 
                  onChange={(e) => {
                    handleChange(e);
                    if (validationErrors.name) validateName(e.target.value);
                  }}
                  onBlur={() => validateName(form.name)}
                  required
                  className={`form-control mb-1 ${validationErrors.name ? "is-invalid" : ""}`}
                />
                <div
                  className="invalid-feedback"
                  role="alert"
                  aria-live="polite"
                  style={{
                    display: "block",
                    visibility: validationErrors.name ? "visible" : "hidden",
                    minHeight: "1.25rem",
                  }}
                >
                  {validationErrors.name || "\u00A0"}
                </div>
                <label htmlFor="start-date" className="form-label">start date: *</label>
                <input 
                  id="start-date"
                  type="date" 
                  name="start_date" 
                  value={form.start_date} 
                 onChange={(e) => {
                    handleChange(e);
                    if (validationErrors.startDate) validateDate(e.target.value, "startDate");
                  }}
                  onBlur={() => validateDate(form.startDate, "startDate")}
                  required
                  className={`form-control mb-1 ${validationErrors.startDate ? "is-invalid" : ""}`}
                />
                <div
                  className="invalid-feedback"
                  role="alert"
                  aria-live="polite"
                  style={{
                    display: "block",
                    visibility: validationErrors.startDate ? "visible" : "hidden",
                    minHeight: "1.25rem",
                  }}
                >
                  {validationErrors.startDate || "\u00A0"}
                </div>
                <label htmlFor="end-date" className="form-label">end date: *</label> 
                <input 
                  id="end-date"
                  type="date" 
                  name="end_date" 
                  value={form.end_date} 
                  onChange={(e) => {
                    handleChange(e);
                    if (validationErrors.endDate) {
                      validateDate(e.target.value, "endDate");
                      validateEndDateAfterStartDate(form.start_date, e.target.value);
                    }
                  }}
                  onBlur={() => {
                    validateDate(form.endDate, "endDate"); 
                    validateEndDateAfterStartDate(form.start_date, form.end_date);
                  }}
                  required
                  className={`form-control mb-1 ${validationErrors.endDate ? "is-invalid" : ""}`}
                />
                <div
                  className="invalid-feedback"
                  role="alert"
                  aria-live="polite"
                  style={{
                    display: "block",
                    visibility: validationErrors.endDate ? "visible" : "hidden",
                    minHeight: "1.25rem",
                  }}
                >
                  {validationErrors.endDate || "\u00A0"}
                </div>
                <label htmlFor="target-value" className="form-label">target value: *</label>
                <input 
                  id="target-value"
                  type="number" 
                  name="target_value" 
                  value={form.target_value} 
                  onChange={(e) => {
                    handleChange(e);
                    if (validationErrors.value) validateValue(e.target.value);
                  }}
                  onBlur={() => validateValue(form.target_value)}
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
              </div>
              
              <div className="modal-footer">
                <div
                  className="alert alert-danger"
                  role="alert"
                  aria-live="polite"
                  style={{
                    display: "block",
                    visibility: editError ? "visible" : "hidden",
                    minHeight: "1.25rem",
                  }}
                >
                  {editError || "\u00A0"}
                </div>
                <Button type="submit" variant="primary" disabled={loading}>
                  {loading ? "saving..." : "save"}
                </Button>
                <Button type="button" onClick={handleDelete} variant="secondary" icon={FiTrash} disabled={loading}>
                  {loading ? "deleting..." : "delete"}
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

export default GoEditModal;
