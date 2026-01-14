import { useEffect, useState } from "react";
import { FiPlus } from "react-icons/fi";
import { FiFilter } from "react-icons/fi";

import { getCategories } from "../api/categories.api";
import { getTransactions } from "../api/transactions.api";
import { getTypes } from "../api/types.api";
import Button from "../components/Button";
import Navbar from "../components/Navbar";
import TrSummaryCard from "../features/transactions/TrSummaryCard";
import TrTable from "../features/transactions/TrTable";


const TransactionsPage = () => {
  const [transactions, setTransactions] = useState([]);
  const [typeMap, setTypeMap] = useState(new Map());
  const [categoryMap, setCategoryMap] = useState(new Map());

  useEffect(() => {
    Promise.all([getTypes(), getCategories()])
      .then(([typesRes, categoriesRes]) => {
        const typeObj = {};
        typesRes.data.forEach(t => { typeObj[t.id] = t.name; });
        setTypeMap(typeObj);

        const categoryObj = {};
        categoriesRes.data.forEach(c => { categoryObj[c.id] = c.name; });
        setCategoryMap(categoryObj);
    });
  }, []);

  useEffect(() => {
    getTransactions()
      .then((res) => setTransactions(res.data))
      .catch(() => setTransactions([]));
  }, []);

  const mappedTransactions = transactions.map(tr => ({
    ...tr,
    type: typeMap[tr.type_id] || tr.type_id,
    category: categoryMap[tr.category_id] || tr.category_id
  }));

	return (
    <>
      <Navbar />
      <h1>transactions</h1>
      <Button variant="secondary" icon={FiFilter}>filter</Button>
      <Button variant="primary" icon={FiPlus}>add</Button>
      <TrSummaryCard title="income" value="200" />
      <TrSummaryCard title="expenses" value="100" />
      <TrSummaryCard title="balance" value="100" />
      <TrTable transactions={mappedTransactions}></TrTable>
    </>
  );
};

export default TransactionsPage;