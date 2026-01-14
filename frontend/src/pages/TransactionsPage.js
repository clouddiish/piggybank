import { useEffect, useState } from "react";
import { FiPlus } from "react-icons/fi";
import { FiFilter } from "react-icons/fi";

import { getCategories } from "../api/categories.api";
import { getTransactions, getTransactionsTotal } from "../api/transactions.api";
import { getTypes } from "../api/types.api";
import Button from "../components/Button";
import Navbar from "../components/Navbar";
import TrSummaryCard from "../features/transactions/TrSummaryCard";
import TrTable from "../features/transactions/TrTable";


const TransactionsPage = () => {
  const [transactions, setTransactions] = useState([]);
  const [typeMap, setTypeMap] = useState(new Map());
  const [categoryMap, setCategoryMap] = useState(new Map());
  const [incomeTotal, setIncomeTotal] = useState(0);
  const [expensesTotal, setExpensesTotal] = useState(0);

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

  useEffect(() => {
    if (Object.keys(typeMap).length === 0) return;

    const incomeTypeId = Object.keys(typeMap).find(id => typeMap[id] === "income");
    const expenseTypeId = Object.keys(typeMap).find(id => typeMap[id] === "expense");

    if (incomeTypeId) {
      getTransactionsTotal({ type_id: incomeTypeId }).then(res => setIncomeTotal(res.data.total));
    }
    if (expenseTypeId) {
      getTransactionsTotal({ type_id: expenseTypeId }).then(res => setExpensesTotal(res.data.total));
    }
  }, [typeMap]);

  const mappedTransactions = transactions.map(tr => ({
    ...tr,
    type: typeMap[tr.type_id] || tr.type_id,
    category: categoryMap[tr.category_id] || tr.category_id
  }));

  const balanceTotal = incomeTotal - expensesTotal;

	return (
    <>
      <Navbar />
      <h1>transactions</h1>
      <Button variant="secondary" icon={FiFilter}>filter</Button>
      <Button variant="primary" icon={FiPlus}>add</Button>
      <TrSummaryCard title="income" value={incomeTotal} />
      <TrSummaryCard title="expenses" value={expensesTotal} />
      <TrSummaryCard title="balance" value={balanceTotal} />
      <TrTable transactions={mappedTransactions}></TrTable>
    </>
  );
};

export default TransactionsPage;