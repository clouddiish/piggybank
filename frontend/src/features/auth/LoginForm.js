import { useState } from "react";

import Button from "../../components/Button";


const LoginForm = ({ onLogin }) => {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const handleSubmit = async (e) => {
		e.preventDefault();
		await onLogin(email, password);
	};

	return (
		<div className="row">
  			<div className="col-12 col-md-6">
				<form onSubmit={handleSubmit}>
					<div className="mb-3">
						<label htmlFor="email" class="form-label">email</label>
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
						<label htmlFor="password" class="form-label">password</label>
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
					<Button type="submit" variant="primary" className="w-100">login</Button>
				</form>
			</div>
		</div>
	);
};

export default LoginForm;
