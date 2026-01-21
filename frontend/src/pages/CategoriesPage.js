import { useEffect, useState } from "react";
import { FiPlus } from "react-icons/fi";

import { getCategories, createCategory, updateCategory, deleteCategory } from "../api/categories.api";
import { getTypes } from "../api/types.api";
import Navbar from "../components/Navbar";
import Button from "../components/Button";
import CaCard from "../features/categories/CaCard";


const CategoriesPage = () => {
  const [categories, setCategories] = useState([]);
  const [typeMap, setTypeMap] = useState(new Map());

  useEffect(() => {
    Promise.all([getTypes(), getCategories()])
      .then(([typesRes, categoriesRes]) => {
        const typeObj = {};
        typesRes.data.forEach(t => { typeObj[t.name] = t.id; });
        setTypeMap(typeObj);
        
        setCategories(categoriesRes.data);
    });
  }, []);

  const expenseCategories = categories.filter(c => c.type_id === typeMap["expense"]);
  const incomeCategories = categories.filter(c => c.type_id === typeMap["income"]);

	return (
    <>
      <Navbar />
      <h1>categories</h1>
      <Button icon={FiPlus} variant="primary">add</Button>
      <h2>income</h2>
      {incomeCategories.map(category => (
        <CaCard key={category.id} category={category} />
      ))}
      <h2>expense</h2>
      {expenseCategories.map(category => (
        <CaCard key={category.id} category={category} />
      ))}
    </>
  );
};

export default CategoriesPage;