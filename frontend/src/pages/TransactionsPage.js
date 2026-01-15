import { useEffect, useState } from "react";
import { FiPlus } from "react-icons/fi";
import { FiFilter } from "react-icons/fi";

import { getCategories } from "../api/categories.api";
import { getTransactions, getTransactionsTotal } from "../api/transactions.api";
import { getTypes } from "../api/types.api";
import Button from "../components/Button";
import Navbar from "../components/Navbar";
import TrFilterModal from "../features/transactions/TrFilterModal";
import TrSummaryCard from "../features/transactions/TrSummaryCard";
import TrTable from "../features/transactions/TrTable";


const TransactionsPage = () => {
  const [transactions, setTransactions] = useState([]);
  const [typeMap, setTypeMap] = useState(new Map());
  const [categoryMap, setCategoryMap] = useState(new Map());
  const [incomeTotal, setIncomeTotal] = useState(0);
  const [expensesTotal, setExpensesTotal] = useState(0);
  const [isFilterModalOpen, setIsFilterModalOpen] = useState(false);
  const [filters, setFilters] = useState({});

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
    getTransactions(filters)
      .then((res) => setTransactions(res.data))
      .catch(() => setTransactions([]));
  }, [filters]);

  useEffect(() => {
    if (Object.keys(typeMap).length === 0) return;

    const incomeTypeId = Object.keys(typeMap).find(id => typeMap[id] === "income");
    const expenseTypeId = Object.keys(typeMap).find(id => typeMap[id] === "expense");

    if (incomeTypeId) {
      getTransactionsTotal({ type_id: incomeTypeId, ...filters }).then(res => setIncomeTotal(res.data.total));
    }
    if (expenseTypeId) {
      getTransactionsTotal({ type_id: expenseTypeId, ...filters }).then(res => setExpensesTotal(res.data.total));
    }
  }, [typeMap, filters]);

  const handleFilter = (form) => {
    const query = {};
    if (form.dateFrom) query.date_gt = form.dateFrom;
    if (form.dateTo) query.date_lt = form.dateTo;
    if (form.type) query.type_id = form.type;
    if (form.category) query.category_id = form.category;
    if (form.valueFrom) query.value_gt = form.valueFrom;
    if (form.valueTo) query.value_lt = form.valueTo;
    if (form.comment) query.comment = form.comment;
    setFilters(query);
  };

  const mappedTransactions = transactions.map(tr => ({
    ...tr,
    type: typeMap[tr.type_id] || tr.type_id,
    category: categoryMap[tr.category_id] || tr.category_id
  }));

  const balanceTotal = incomeTotal - expensesTotal;
  const typeOptions = Object.entries(typeMap).map(([id, name]) => ({ id, name }));
  const categoryOptions = Object.entries(categoryMap).map(([id, name]) => ({ id, name }));

	return (
    <>
      <Navbar />
      <h1>transactions</h1>
      <Button
        variant="secondary"
        icon={FiFilter}
        onClick={() => setIsFilterModalOpen(true)}
      >
        filter
      </Button>
      <Button variant="primary" icon={FiPlus}>add</Button>
      <TrSummaryCard title="income" value={incomeTotal} />
      <TrSummaryCard title="expenses" value={expensesTotal} />
      <TrSummaryCard title="balance" value={balanceTotal} />
      <TrTable transactions={mappedTransactions}></TrTable>
      <TrFilterModal
        open={isFilterModalOpen}
        onClose={() => setIsFilterModalOpen(false)}
        typeOptions={typeOptions}
        categoryOptions={categoryOptions}
        onFilter={handleFilter}
      />
    </>
  );
};

export default TransactionsPage;