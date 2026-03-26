import { useState } from "react";


const commentDisallowedCharsRegex = /[<>&"'\\|~]/;

const useTrValidation = () => {
  const [validationErrors, setValidationErrors] = useState({});

  const validateDate = (dateStr) => {
    if (!dateStr) {
      setValidationErrors((prev) => ({ ...prev, date: "date is required" }));
      return false;
    }
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) {
      setValidationErrors((prev) => ({ ...prev, date: "enter a valid date" }));
      return false;
    }
    setValidationErrors((prev) => ({ ...prev, date: null }));
    return true;
  };

  const validateValue = (value) => {
    if (value === "" || value === null || value === undefined || isNaN(Number(value))) {
      setValidationErrors((prev) => ({ ...prev, value: "value is required and must be a number" }));
      return false;
    }

    setValidationErrors((prev) => ({ ...prev, value: null }));
    return true;
  };

  const validateComment = (comment) => {
    if (comment && comment.length > 255) {
      setValidationErrors((prev) => ({ ...prev, comment: "comment must be at most 255 characters long" }));
      return false;
    }

    if (comment && commentDisallowedCharsRegex.test(comment)) {
      setValidationErrors((prev) => ({ ...prev, comment: "comment contains disallowed characters" }));
      return false;
    }

    setValidationErrors((prev) => ({ ...prev, comment: null }));
    return true;
  };

  return {
    validationErrors,
    validateDate,
    validateValue,
    validateComment,
  };

};

export default useTrValidation;