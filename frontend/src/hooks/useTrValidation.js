import { useState } from "react";


const commentDisallowedCharsRegex = /[<>&"'\\|~]/;

const useTrValidation = () => {
  const [validationErrors, setValidationErrors] = useState({});

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

  const validateValue = (value, isRequired = true, fieldName = "value") => {
    if (isRequired && (value === "" || value === null || value === undefined || isNaN(Number(value)))) {
      setValidationErrors((prev) => ({ ...prev, [fieldName]: `${fieldName} is required and must be a number` }));
      return false;
    }

    setValidationErrors((prev) => ({ ...prev, [fieldName]: null }));
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