import { useState } from "react";

import Button from "../../components/Button";


const RegisterForm = ({ onRegister }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    await onRegister(email, password, confirmPassword);
  };

    return (
      <div className="row">
  			<div className="col-12 col-md-6">
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="email" className="form-label">email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="email"
                className="form-control"
							  id="email"
              />
            </div>
            <div className="mb-3">
              <label htmlFor="password" className="form-label">password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="password"
                className="form-control"
							  id="password"
              />
            </div>
            <div className="mb-3">
              <label htmlFor="cpassword" className="form-label">confirm password</label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                placeholder="confirm password"
                className="form-control"
							  id="cpassword"
              />
            </div>
            <Button type="submit" variant="primary" className="w-100">register</Button>
          </form>
        </div>
      </div>
    );
};

export default RegisterForm;
