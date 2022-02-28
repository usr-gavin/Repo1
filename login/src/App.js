import React from "react";
import axios from "axios";
import Hello from './components/Hello';

class App extends React.Component {
	state = {
		details: [],
		user: "",
		quote: "",
	};

	componentDidMount() {
		let data;

		axios
			.get("http://localhost:8000/wel/")
			.then((res) => {
				data = res.data;
				this.setState({
					details: data,
				});
			})
			.catch((err) => {});
	}

	renderSwitch = (param) => {
		switch (param + 1) {
			case 1:
				return "primary ";
			case 2:
				return "secondary";
			case 3:
				return "success";
			case 4:
				return "danger";
			case 5:
				return "warning";
			case 6:
				return "info";
			default:
				return "yellow";
		}
	};

	handleInput = (e) => {
		this.setState({
			[e.target.name]: e.target.value,
		});
	};

	handleSubmit = (e) => {
		e.preventDefault();

		axios
			.post("http://localhost:8000/wel/", {
				name: this.state.user,
				detail: this.state.quote,           
			})
			.then((res) => {
				this.setState({
					user: "",
					quote: "",
				});
			})
			.catch((err) => {});
	};

	render() {
		return (
			<div className="container jumbotron ">
				<form onSubmit={this.handleSubmit}>
					<div className="input-group mb-3">
						<div className="input-group-prepend">
							<span className="input-group-text"
								id="basic-addon1">
								{" "}
								Username{" "}
							</span>
						</div>
						<input type="text" className="form-control"
							placeholder="Enter your email or username"
							aria-label="Username"
							aria-describedby="basic-addon1"
							value={this.state.user} name="user"
							onChange={this.handleInput} />
					</div>

					<div className="input-group mb-3">
						<div className="input-group-prepend">
							<span className="input-group-text">
							Password
							</span>
						</div>
						<textarea className="form-control "
								aria-label="With textarea"
								placeholder="Enter your Password"
								value={this.state.quote} name="quote"
								onChange={this.handleInput}>
						</textarea>
					</div>

					<button type="submit" className="btn btn-primary mb-5">
						Login
					</button>
				</form>

				<hr
					style={{
						color: "#000000",
						backgroundColor: "#000000",
						height: 0.5,
						borderColor: "#000000",
					}}
				/>

				{this.state.details.map((detail, id) => (
					<div key={id}>
						<div className="card shadow-lg">
							<div className={"bg-" + this.renderSwitch(id % 6) +
										" card-header"}>Quote {id + 1}</div>
							<div className="card-body">
								<blockquote className={"text-" + this.renderSwitch(id % 6) +
												" blockquote mb-0"}>
									<h1> {detail.detail} </h1>
									<footer className="blockquote-footer">
										{" "}
										<cite title="Source Title">{detail.name}</cite>
									</footer>
								</blockquote>
							</div>
						</div>
						<span className="border border-primary "></span>
					</div>
				))}
				<Hello/>
			</div>
		);
	}
}
export default App;
