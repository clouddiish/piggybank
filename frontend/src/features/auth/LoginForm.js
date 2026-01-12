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
		<form onSubmit={handleSubmit}>
			<input
				type="email"
				value={email}
				onChange={(e) => setEmail(e.target.value)}
				required
				placeholder="email"
			/>
			<input
				type="password"
				value={password}
				onChange={(e) => setPassword(e.target.value)}
				required
				placeholder="password"
			/>
			<Button type="submit" variant="primary">Login</Button>
		</form>
	);
};

export default LoginForm;
