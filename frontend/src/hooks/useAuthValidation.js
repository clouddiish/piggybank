import { useState } from "react";


const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const useAuthValidation = () => {
  const [validationErrors, setValidationErrors] = useState({});

  const validateEmail = (email) => {
    if (!email) {
      setValidationErrors((prev) => ({ ...prev, email: "email is required" }));
      return false;
    }
    if (email.length > 254) {
      setValidationErrors((prev) => ({ ...prev, email: "email must be at most 254 characters long" }));
      return false;
    }
    if (!emailRegex.test(email)) {
      setValidationErrors((prev) => ({ ...prev, email: "enter a valid email address" }));
      return false;
    }
    setValidationErrors((prev) => ({ ...prev, email: null }));
    return true;
  };

  const validatePassword = (password, fieldName = "password") => {
    if (!password) {
      setValidationErrors((prev) => ({ ...prev, [fieldName]: "password is required" }));
      return false;
    }
    if (password.length < 8) {
      setValidationErrors((prev) => ({ ...prev, [fieldName]: "password must be at least 8 characters long" }));
      return false;
    }
    if (password.length > 128) {
      setValidationErrors((prev) => ({ ...prev, [fieldName]: "password must be at most 128 characters long" }));
      return false;
    }
    setValidationErrors((prev) => ({ ...prev, [fieldName]: null }));
    return true;
  };

  const validateConfirmPassword = (password, confirmPassword) => {
    if (password !== confirmPassword) {
      setValidationErrors((prev) => ({ ...prev, confirmPassword: "passwords do not match" }));
      return false;
    }
    setValidationErrors((prev) => ({ ...prev, confirmPassword: null }));
    return true;
  };

  return {
    validationErrors,
    validateEmail,
    validatePassword,
    validateConfirmPassword,
  };
};

export default useAuthValidation;