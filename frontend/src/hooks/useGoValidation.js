import { useState } from "react";


const useGoValidation = () => {
  const [validationErrors, setValidationErrors] = useState({});

  const validateName = (name, isRequired = true) => {
    if (isRequired && (!name || name.trim() === "")) {
      setValidationErrors((prev) => ({ ...prev, name: "name is required" }));
      return false;
    }

    if (name && name.length > 255) {
      setValidationErrors((prev) => ({ ...prev, name: "name must be at most 255 characters long" }));
      return false;
    }

    if (name && !name.replace(" ", "").match(/^[a-zA-Z0-9\s]+$/)) {
      setValidationErrors((prev) => ({ ...prev, name: "name must only contain alphanumeric characters and spaces" }));
      return false;
    }

    setValidationErrors((prev) => ({ ...prev, name: null }));
    return true;
  };

  const validateDate = (dateStr, isRequired = true, fieldName = "date") => {
    if (!dateStr && isRequired) {
      setValidationErrors((prev) => ({ ...prev, [fieldName]: `${fieldName} is required` }));
      return false;
    }
    const date = new Date(dateStr);
    if (dateStr !== "" && isNaN(date.getTime())) {
      setValidationErrors((prev) => ({ ...prev, [fieldName]: "enter a valid date" }));
      return false;
    }
    setValidationErrors((prev) => ({ ...prev, [fieldName]: null }));
    return true;
  };

  const validateEndDateAfterStartDate = (startDateStr, endDateStr) => {
    if (!startDateStr || !endDateStr) {
      // if either date is missing, we can't validate this rule, so we consider it valid
      setValidationErrors((prev) => ({ ...prev, end_date: null }));
      return true;
    }
    const startDate = new Date(startDateStr);
    const endDate = new Date(endDateStr);
    if (endDate < startDate) {
      setValidationErrors((prev) => ({ ...prev, end_date: "end date must be after start date" }));
      return false;
    }
    setValidationErrors((prev) => ({ ...prev, end_date: null }));
    return true;
  };

  const validateValue = (value, isRequired = true, fieldName = "value") => {
    if (isRequired && (value === "" || value === null || value === undefined || isNaN(Number(value)))) {
      setValidationErrors((prev) => ({ ...prev, [fieldName]: `${fieldName} is required and must be a number` }));
      return false;
    }

    setValidationErrors((prev) => ({ ...prev, [fieldName]: null }));
    return true;
  };

  return {
    validationErrors,
    validateName,
    validateDate,
    validateEndDateAfterStartDate,
    validateValue,
  };

}

export default useGoValidation;