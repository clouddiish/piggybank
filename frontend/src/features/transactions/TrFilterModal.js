import { useState } from "react";
import { IoCloseOutline } from "react-icons/io5";

import Button from "../../components/Button";


const TrFilterModal = ({ open, onClose, typeOptions = [], categoryOptions = [], onFilter }) => {
    const initialState = {
        dateFrom: "",
        dateTo: "",
        type: "",
        category: "",
        valueFrom: "",
        valueTo: "",
        comment: ""
    };
    const [form, setForm] = useState(initialState);

    if (!open) return null;

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

    return (
        <>
        <Button onClick={onClose} icon={IoCloseOutline} variant="secondary" />
        <h1>filter transactions</h1>
        <form onSubmit={handleSubmit}>
            <label>date from: <input type="date" name="dateFrom" value={form.dateFrom} onChange={handleChange} /></label>
            <label>date to: <input type="date" name="dateTo" value={form.dateTo} onChange={handleChange} /></label>
            <label>type: 
            <select name="type" value={form.type} onChange={handleChange}>
                <option value="">-- select type --</option>
                {typeOptions.map(opt => (
                <option key={opt.id} value={opt.id}>{opt.name}</option>
                ))}
            </select>
            </label>
            <label>category: 
            <select name="category" value={form.category} onChange={handleChange}>
                <option value="">-- select category --</option>
                {categoryOptions.map(opt => (
                <option key={opt.id} value={opt.id}>{opt.name}</option>
                ))}
            </select>
            </label>
            <label>value from: <input type="number" name="valueFrom" value={form.valueFrom} onChange={handleChange} /></label>
            <label>value to: <input type="number" name="valueTo" value={form.valueTo} onChange={handleChange} /></label>
            <label>comment contains: <input type="text" name="comment" value={form.comment} onChange={handleChange} /></label>
            <Button type="button" variant="secondary" onClick={handleClear}>clear all</Button>
            <Button type="submit" variant="primary">filter</Button>
        </form>
        </>
    );
};

export default TrFilterModal;
