import { useEffect, useState } from "react";
import { FiPlus } from "react-icons/fi";

import { getCategories, createCategory, updateCategory, deleteCategory } from "../api/categories.api";
import { getTypes } from "../api/types.api";
import Navbar from "../components/Navbar";
import Button from "../components/Button";
import CaAddModal from "../features/categories/CaAddModal";
import CaCard from "../features/categories/CaCard";
import CaEditModal from "../features/categories/CaEditModal";


const CategoriesPage = () => {
  const [categories, setCategories] = useState([]);
  const [typeMap, setTypeMap] = useState(new Map());
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editingCategoryId, setEditingCategoryId] = useState(null);

  useEffect(() => {
    const fetchTypesAndCategories = async () => {
      const [typesRes, categoriesRes] = await Promise.all([getTypes(), getCategories()]);

      const typeObj = {};
      typesRes.data.forEach(t => { typeObj[t.name] = t.id; });
      setTypeMap(typeObj);

      setCategories(categoriesRes.data);
    }
    fetchTypesAndCategories();
  }, []);

  const handleAdd = async (form) => {
      const query = {};
      if (form.type) query.type_id = form.type;
      if (form.name) query.name = form.name;

      await createCategory(query);
      setIsAddModalOpen(false);
      
      const updatedCategories = await getCategories();
      setCategories(updatedCategories.data);
    };

  const handleEdit = async (form) => {
      const query = {};
      if (form.type) query.type_id = form.type;
      if (form.name) query.name = form.name;

      await updateCategory(editingCategoryId, query);
      setIsEditModalOpen(false);
      setEditingCategoryId(null);

      const updatedCategories = await getCategories();
      setCategories(updatedCategories.data);
    };
    
  const handleDelete = async (categoryId) => {
    await deleteCategory(categoryId);
    setIsEditModalOpen(false);
    setEditingCategoryId(null);
    const updatedCategories = await getCategories();
    setCategories(updatedCategories.data);
  };

  const expenseCategories = categories.filter(c => c.type_id === typeMap["expense"]);
  const incomeCategories = categories.filter(c => c.type_id === typeMap["income"]);
  const typeOptions = Object.entries(typeMap).map(([name, id]) => ({ id, name }));

	return (
    <>
      <Navbar />
      <div className="mx-md-5 mx-2 py-3 align-items-center">
        <h1 className="mb-5">categories</h1>
        <div className="row mb-5">
          <div className="col-12 col-md-auto">
            <Button 
              icon={FiPlus} 
              variant="primary" 
              onClick={() => setIsAddModalOpen(true)}
              className="w-100"
            >
              add
            </Button>
          </div>
        </div>
        <div className="mb-5">
        <h2 className="mb-3">income</h2>
          {incomeCategories.map(category => (
            <CaCard 
              key={category.id} 
              category={category} 
              onClick={() => {
                setEditingCategoryId(category.id);
                setIsEditModalOpen(true);
              }} 
            />
          ))}
        </div>
        <div className="mb-5">
          <h2 className="mb-3">expense</h2>
          {expenseCategories.map(category => (
            <CaCard 
              key={category.id} 
              category={category} 
              onClick={() => {
                setEditingCategoryId(category.id);
                setIsEditModalOpen(true);
              }} 
            />
          ))}
        </div>

      </div>

      <CaAddModal
        open={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        typeOptions={typeOptions}
        onAdd={handleAdd}
      />
      <CaEditModal
        open={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        categoryId={editingCategoryId}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
    </>
  );
};

export default CategoriesPage;