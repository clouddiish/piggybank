import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";

import Button from "../../components/Button";
import useGoValidation from "../../hooks/useGoValidation";


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
  const [loading, setLoading] = useState(false);
  const [filterError, setFilterError] = useState(null);
  const { validationErrors, validateName, validateDate, validateValue } = useGoValidation();

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

    const isStartDateFromValid = validateDate(form.startDateFrom, false, "startDateFrom");
    const isStartDateToValid = validateDate(form.startDateTo, false, "startDateTo");
    const isEndDateFromValid = validateDate(form.endDateFrom, false, "endDateFrom");
    const isEndDateToValid = validateDate(form.endDateTo, false, "endDateTo");
    const isTargetValueFromValid = validateValue(form.targetValueFrom, false, "targetValueFrom");
    const isTargetValueToValid = validateValue(form.targetValueTo, false, "targetValueTo");
    const isNameValid = validateName(form.name, false);

    if (!isStartDateFromValid || !isStartDateToValid || !isEndDateFromValid || !isEndDateToValid || !isTargetValueFromValid || !isTargetValueToValid || !isNameValid) {
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
              <h1>filter goals</h1>
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
                <label htmlFor="name-contains" className="form-label">name contains:</label>
                <input
                  id="name-contains"
                  type="text" 
                  name="name" 
                  value={form.name} 
                  onChange={(e) => {
                    handleChange(e);
                    if (validationErrors.name) validateName(e.target.value, false);
                  }}
                  onBlur={() => validateName(form.name, false)}
                  className={`form-control ${validationErrors.name ? "is-invalid" : ""}`}
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
                <label htmlFor="start-date-from" className="form-label">start date from:</label>
                <input 
                  id="start-date-from"
                  type="date" 
                  name="startDateFrom" 
                  value={form.startDateFrom} 
                  onChange={(e) => {
                    handleChange(e);
                    if (validationErrors.startDateFrom) validateDate(e.target.value, false, "startDateFrom");
                  }}
                  onBlur={() => validateDate(form.startDateFrom, false, "startDateFrom")}
                  className={`form-control mb-1 ${validationErrors.startDateFrom ? "is-invalid" : ""}`}
                />
                <div
                  className="invalid-feedback"
                  role="alert"
                  aria-live="polite"
                  style={{
                    display: "block",
                    visibility: validationErrors.startDateFrom ? "visible" : "hidden",
                    minHeight: "1.25rem",
                  }}
                >
                  {validationErrors.startDateFrom || "\u00A0"}
                </div>
                <label htmlFor="start-date-to" className="form-label">start date to:</label>
                <input
                  id="start-date-to"
                  type="date" 
                  name="startDateTo" 
                  value={form.startDateTo} 
                  onChange={(e) => {
                    handleChange(e);
                    if (validationErrors.startDateTo) validateDate(e.target.value, false, "startDateTo");
                  }}
                  onBlur={() => validateDate(form.startDateTo, false, "startDateTo")}
                  className={`form-control mb-1 ${validationErrors.startDateTo ? "is-invalid" : ""}`}
                />
                <div
                  className="invalid-feedback"
                  role="alert"
                  aria-live="polite"
                  style={{
                    display: "block",
                    visibility: validationErrors.startDateTo ? "visible" : "hidden",
                    minHeight: "1.25rem",
                  }}
                >
                  {validationErrors.startDateTo || "\u00A0"}
                </div>
                <label htmlFor="end-date-from" className="form-label">end date from:</label>
                <input
                  id="end-date-from"
                  type="date" 
                  name="endDateFrom" 
                  value={form.endDateFrom} 
                  onChange={(e) => {
                    handleChange(e);
                    if (validationErrors.endDateFrom) validateDate(e.target.value, false, "endDateFrom");
                  }}
                  onBlur={() => validateDate(form.endDateFrom, false, "endDateFrom")}
                  className={`form-control mb-1 ${validationErrors.endDateFrom ? "is-invalid" : ""}`}
                />
                <div
                  className="invalid-feedback"
                  role="alert"
                  aria-live="polite"
                  style={{
                    display: "block",
                    visibility: validationErrors.endDateFrom ? "visible" : "hidden",
                    minHeight: "1.25rem",
                  }}
                >
                  {validationErrors.endDateFrom || "\u00A0"}
                </div>
                <label htmlFor="end-date-to" className="form-label">end date to:</label>
                <input
                  id="end-date-to"
                  type="date" 
                  name="endDateTo" 
                  value={form.endDateTo} 
                  onChange={(e) => {
                    handleChange(e);
                    if (validationErrors.endDateTo) validateDate(e.target.value, false, "endDateTo");
                  }}
                  onBlur={() => validateDate(form.endDateTo, false, "endDateTo")}
                  className={`form-control mb-1 ${validationErrors.endDateTo ? "is-invalid" : ""}`}
                />
                <div
                  className="invalid-feedback"
                  role="alert"
                  aria-live="polite"
                  style={{
                    display: "block",
                    visibility: validationErrors.endDateTo ? "visible" : "hidden",
                    minHeight: "1.25rem",
                  }}
                >
                  {validationErrors.endDateTo || "\u00A0"}
                </div>
                <label htmlFor="target-value-from" className="form-label">target value from:</label> 
                <input 
                  id="target-value-from"
                  type="number" 
                  name="targetValueFrom" 
                  value={form.targetValueFrom} 
                  onChange={(e) => {
                      handleChange(e);
                      if (validationErrors.targetValueFrom) validateValue(e.target.value, false, "targetValueFrom");
                    }}
                    onBlur={() => validateValue(form.targetValueFrom, false, "targetValueFrom")}
                    className={`form-control mb-1 ${validationErrors.targetValueFrom ? "is-invalid" : ""}`}
                  />
                  <div
                    className="invalid-feedback"
                    role="alert"
                    aria-live="polite"
                    style={{
                      display: "block",
                      visibility: validationErrors.targetValueFrom ? "visible" : "hidden",
                      minHeight: "1.25rem",
                    }}
                  >
                    {validationErrors.targetValueFrom || "\u00A0"}
                  </div>
                <label htmlFor="target-value-to" className="form-label">target value to:</label>
                <input
                  id="target-value-to"
                  type="number" 
                  name="targetValueTo" 
                  value={form.targetValueTo} 
                  onChange={(e) => {
                      handleChange(e);
                      if (validationErrors.targetValueTo) validateValue(e.target.value, false, "targetValueTo");
                    }}
                    onBlur={() => validateValue(form.targetValueTo, false, "targetValueTo")}
                    className={`form-control mb-1 ${validationErrors.targetValueTo ? "is-invalid" : ""}`}
                  />
                  <div
                    className="invalid-feedback"
                    role="alert"
                    aria-live="polite"
                    style={{
                      display: "block",
                      visibility: validationErrors.targetValueTo ? "visible" : "hidden",
                      minHeight: "1.25rem",
                    }}
                  >
                    {validationErrors.targetValueTo || "\u00A0"}
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

export default GoFilterModal;
