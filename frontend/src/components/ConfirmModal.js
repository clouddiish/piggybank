import { IoCloseOutline } from "react-icons/io5";

import Button from "./Button";


const ConfirmModal = ({ open, title = "Confirm", message = "Are you sure?", onClose, onConfirm, confirmLabel = "Confirm", cancelLabel = "Cancel", loading = false, className }) => {
  const cls = ["modal", "fade", open ? "show" : "", className].filter(Boolean).join(" ");
  const style = open ? { display: "block" } : undefined;

  if (!open) return null;

  return (
    <>
    <div className={cls} tabIndex="-1" role="dialog" aria-modal="true" style={style}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header justify-content-between">
            <h1 className="modal-title">{title}</h1>
            <Button onClick={onClose} icon={IoCloseOutline} variant="secondary" />
          </div>
          <div className="modal-body">
            <p>{message}</p>
          </div>
          <div className="modal-footer">
            <Button type="button" variant="secondary" onClick={onClose} disabled={loading}>{cancelLabel}</Button>
            <Button type="button" variant="danger" onClick={onConfirm} disabled={loading}>{loading ? `${confirmLabel.toLowerCase()}...` : confirmLabel}</Button>
          </div>
        </div>
      </div>
    </div>
    <div className="modal-backdrop fade show"></div>
  </>
  );
};

export default ConfirmModal;
