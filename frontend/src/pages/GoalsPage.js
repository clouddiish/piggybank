import { useEffect, useState } from "react";
import { FiPlus } from "react-icons/fi";
import { FiFilter } from "react-icons/fi";

import { getCategories } from "../api/categories.api";
import { getGoals, createGoal } from "../api/goals.api";
import { getTransactionsTotal } from "../api/transactions.api";
import { getTypes } from "../api/types.api";
import Button from "../components/Button";
import Navbar from "../components/Navbar";
import GoCard from "../features/goals/GoCard";
import GoAddModal from "../features/goals/GoAddModal";
import GoFilterModal from "../features/goals/GoFilterModal";

const GoalsPage = () => {
  const [goals, setGoals] = useState([]);
  const [goalTotals, setGoalTotals] = useState({});
  const [typeMap, setTypeMap] = useState(new Map());
  const [categoryMap, setCategoryMap] = useState(new Map());
  const [isFilterModalOpen, setIsFilterModalOpen] = useState(false);
  const [filters, setFilters] = useState({});
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);

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
    getGoals(filters)
      .then((res) => setGoals(res.data))
      .catch(() => setGoals([]));
  }, [filters]);

  useEffect(() => {
    const fetchTotals = async () => {
      const totals = {};
      await Promise.all(goals.map(async (goal) => {
        try {
          const res = await getTransactionsTotal({
            type_id: goal.type_id,
            category_id: goal.category_id,
            date_gt: goal.start_date,
            date_lt: goal.end_date
          });
          totals[goal.id] = res.data.total;
        } catch {
          totals[goal.id] = "error";
        }
      }));
      setGoalTotals(totals);
    };
    if (goals.length > 0) fetchTotals();
  }, [goals]);

  const handleFilter = (form) => {
    const query = {};
    if (form.startDateFrom) query.start_date_gt = form.startDateFrom;
    if (form.startDateTo) query.start_date_lt = form.startDateTo;
    if (form.endDateFrom) query.end_date_gt = form.endDateFrom;
    if (form.endDateTo) query.end_date_lt = form.endDateTo;
    if (form.type) query.type_id = form.type;
    if (form.category) query.category_id = form.category;
    if (form.targetValueFrom) query.target_value_gt = form.targetValueFrom;
    if (form.targetValueTo) query.target_value_lt = form.targetValueTo;
    if (form.name) query.name = form.name;
    setFilters(query);
  };

  const handleAdd = (form) => {
      const query = {};
      if (form.type) query.type_id = form.type;
      if (form.category) query.category_id = form.category;
      if (form.name) query.name = form.name;
      if (form.start_date) query.start_date = form.start_date;
      if (form.end_date) query.end_date = form.end_date;
      if (form.target_value) query.target_value = form.target_value;
  
      createGoal(query)
        .then(() => {
          setIsAddModalOpen(false);
          setFilters({ ...filters });
        });
    };

  const mappedGoals = goals.map(goal => ({
    ...goal,
    current_value: goalTotals[goal.id] ?? "",
    type: typeMap[goal.type_id] || goal.type_id,
    category: categoryMap[goal.category_id] || goal.category_id
  }));
  const goCards = mappedGoals.map(goal => (<GoCard key={goal.id} goal={goal} />));
  const typeOptions = Object.entries(typeMap).map(([id, name]) => ({ id, name }));
  const categoryOptions = Object.entries(categoryMap).map(([id, name]) => ({ id, name }));

	return (
    <>
      <Navbar />
      <h1>goals</h1>
      <Button
        variant="secondary"
        icon={FiFilter}
        onClick={() => setIsFilterModalOpen(true)}
      >
        filter
      </Button>
      <Button 
        variant="primary" 
        icon={FiPlus}
        onClick={() => setIsAddModalOpen(true)}
      >
        add
      </Button>
      {goCards}
      <GoFilterModal
        open={isFilterModalOpen}
        onClose={() => setIsFilterModalOpen(false)}
        typeOptions={typeOptions}
        categoryOptions={categoryOptions}
        onFilter={handleFilter}
      />
      <GoAddModal
        open={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        typeOptions={typeOptions}
        categoryOptions={categoryOptions}
        onAdd={handleAdd}
      />
    </>
  );
};

export default GoalsPage;