import { useState } from "react";


const useCaValidation = () => {
  const [validationErrors, setValidationErrors] = useState({});

  const validateName = (name) => {
    if (!name || name.trim() === "") {
      setValidationErrors((prev) => ({ ...prev, name: "name is required" }));
      return false;
    }

    if (name.length > 255) {
      setValidationErrors((prev) => ({ ...prev, name: "name must be at most 255 characters long" }));
      return false;
    }

    if (!name.replace(" ", "").match(/^[a-zA-Z0-9\s]+$/)) {
      setValidationErrors((prev) => ({ ...prev, name: "name must only contain alphanumeric characters and spaces" }));
      return false;
    }

    setValidationErrors((prev) => ({ ...prev, name: null }));
    return true;
  };

  return {
    validationErrors,
    validateName,
  }

}

export default useCaValidation;