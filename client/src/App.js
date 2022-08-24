import React, { useState } from "react";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";


function App() {
  const [userId, setUserId] = useState(1);
  const [data, setData] = useState(null);
  const [showResults, setShowResults] = useState(false);

  const handleClick = async () => {
    const response = await fetch(`/${userId}`).then((response) =>
      response.json()
    );

    setData(response);
    setShowResults(true);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    handleClick();
  };

  const currencyFormat = (num) => {
    return "$" + num.toFixed(2).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
  };

  return (
    <Container style={{ textAlign: "center", paddingTop: "3rem" }}>
      <h1> Retirement Calculator </h1>
      <form style={{ paddingTop: "2rem" }} onSubmit={handleSubmit}>
        <label>
          Enter user id:{" "}
          <input
            type="number"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
          />
        </label>
      </form>
      <div style={{ paddingTop: "2rem" }}>
        <Button onClick={handleClick}>Calculate Retirement</Button>
      </div>
      <br />
      {showResults && (
        <div>
          <h3 style={{ fontWeight: "bold" }}>Results</h3>
          <h4>To retire at age {data.assumptions.retirement_age}:</h4>
          <h4>You will need {data.user_info.amount_needed}</h4>
          <h4>You will have saved {data.user_info.amount_saved}</h4>
          <br />
          <h3 style={{ fontWeight: "bold" }}>Assumptions</h3>
          <h4>
            Pre Retirement Income Percent:{" "}
            {data.assumptions.pre_retirement_income_percent}%
          </h4>
          <h4>Life Expectancy: {data.assumptions.life_expectancy}</h4>
          <h4>
            Expected Rate of Return: {data.assumptions.expected_rate_of_return}%
          </h4>
          <h4>Inflation: 3%</h4>
          <h4>Yearly Salary Increase: 2%</h4>
          <h4>Retirement Rate of Return: 5%</h4>
          <br />
          <h3 style={{ fontWeight: "bold" }}>User Info</h3>
          <h4>Date of Birth: {data.user_info.date_of_birth}</h4>
          <h4>
            Household Income: {currencyFormat(data.user_info.household_income)}
          </h4>
          <h4>
            Current Savings:{" "}
            {currencyFormat(data.user_info.current_retirement_savings)}
          </h4>
        </div>
      )}
    </Container>
  );
}

export default App;
