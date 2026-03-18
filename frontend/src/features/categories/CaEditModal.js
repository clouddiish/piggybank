import { useState, useEffect } from "react";
import { IoCloseOutline } from "react-icons/io5";
import { FiTrash } from "react-icons/fi";

import { getCategory } from "../../api/categories.api";
import Button from "../../components/Button";


const initialState = {
    name: "",
};

const CaEditModal = ({ open, onClose, categoryId, onEdit, onDelete, className }) => {
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

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onEdit) onEdit(form);
    if (onClose) onClose();
  };

  const handleDelete = () => {
    if (onDelete) onDelete(categoryId);
    if (onClose) onClose();
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

            <form onSubmit={handleSubmit}>

              <div className="modal-body">
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

export default CaEditModal;