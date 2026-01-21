import { useEffect, useState } from "react";
import { FiPlus } from "react-icons/fi";
import { FiFilter } from "react-icons/fi";

import { getCategories } from "../api/categories.api";
import { getGoals } from "../api/goals.api";
import { getTransactionsTotal } from "../api/transactions.api";
import Button from "../components/Button";
import { getTypes } from "../api/types.api";
import Navbar from "../components/Navbar";
import GoCard from "../features/goals/GoCard";



const GoalsPage = () => {
  const [goals, setGoals] = useState([]);
  const [goalTotals, setGoalTotals] = useState({});
  const [typeMap, setTypeMap] = useState(new Map());
  const [categoryMap, setCategoryMap] = useState(new Map());
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

  const mappedGoals = goals.map(goal => ({
    ...goal,
    current_value: goalTotals[goal.id] ?? "",
    type: typeMap[goal.type_id] || goal.type_id,
    category: categoryMap[goal.category_id] || goal.category_id
  }));
  const goCards = mappedGoals.map(goal => (<GoCard key={goal.id} goal={goal} />));

	return (
    <>
      <Navbar />
      <h1>goals</h1>
      <Button variant="secondary" icon={FiFilter}>filter</Button>
      <Button variant="primary" icon={FiPlus}>add</Button>
      {goCards}
    </>
  );
};

export default GoalsPage;