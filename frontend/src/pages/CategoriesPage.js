import { useEffect, useState } from "react";
import { FiPlus } from "react-icons/fi";

import { getCategories, createCategory, updateCategory, deleteCategory } from "../api/categories.api";
import { getTypes } from "../api/types.api";
import Navbar from "../components/Navbar";
import Button from "../components/Button";
import CaAddModal from "../features/categories/CaAddModal";
import CaCard from "../features/categories/CaCard";


const CategoriesPage = () => {
  const [categories, setCategories] = useState([]);
  const [typeMap, setTypeMap] = useState(new Map());
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);

  useEffect(() => {
    Promise.all([getTypes(), getCategories()])
      .then(([typesRes, categoriesRes]) => {
        const typeObj = {};
        typesRes.data.forEach(t => { typeObj[t.name] = t.id; });
        setTypeMap(typeObj);
        
        setCategories(categoriesRes.data);
    });
  }, []);

  const handleAdd = (form) => {
      const query = {};
      if (form.type) query.type_id = form.type;
      if (form.name) query.name = form.name;
  
      createCategory(query)
        .then(() => {
          setIsAddModalOpen(false);
          getCategories().then(res => setCategories(res.data));
        });
    };

  const expenseCategories = categories.filter(c => c.type_id === typeMap["expense"]);
  const incomeCategories = categories.filter(c => c.type_id === typeMap["income"]);
  const typeOptions = Object.entries(typeMap).map(([name, id]) => ({ id, name }));

	return (
    <>
      <Navbar />
      <h1>categories</h1>
      <Button icon={FiPlus} variant="primary" onClick={() => setIsAddModalOpen(true)}>add</Button>
      <h2>income</h2>
      {incomeCategories.map(category => (
        <CaCard key={category.id} category={category} />
      ))}
      <h2>expense</h2>
      {expenseCategories.map(category => (
        <CaCard key={category.id} category={category} />
      ))}
      <CaAddModal
        open={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        typeOptions={typeOptions}
        onAdd={handleAdd}
      />
    </>
  );
};

export default CategoriesPage;