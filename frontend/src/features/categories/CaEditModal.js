import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";
import { FiTrash } from "react-icons/fi";

import { getCategory } from "../../api/categories.api";
import Button from "../../components/Button";
import useCaValidation from "../../hooks/useCaValidation";


const initialState = {
    name: "",
};

const CaEditModal = ({ open, onClose, categoryId, onEdit, onDelete, className }) => {
  const [form, setForm] = useState(initialState);
  const [loading, setLoading] = useState(false);
  const [editError, setEditError] = useState(null);
  const { validationErrors, validateName } = useCaValidation();

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
    if (open && categoryId) {

      getCategory(categoryId).then(res => {
        setForm({...initialState, 
          name: res.data.name || "",
        });
      });
    }
  }, [open, categoryId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => {
      return { ...prev, [name]: value };
    }
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setEditError(null);

    if (!validateName(form.name)) {
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
      if (onDelete) await onDelete(categoryId);
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
    }
  }

  if (!open) return null;

  return (
    <>
    <div className={cls} tabIndex="-1" role="dialog" aria-modal="true" style={style}>
        <div className="modal-dialog">
          <div className="modal-content">

            <div className="modal-header justify-content-between">
              <h1>edit category</h1>
              <Button onClick={onClose} icon={IoCloseOutline} variant="secondary" />
            </div>

            <form onSubmit={handleSubmit} aria-busy={loading}>

              <div className="modal-body">
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

export default CaEditModal;