import React, { useState, useEffect } from "react";
import "./register.css";
import axios from "axios";

interface Errors {
  isEmployer: string;
  isEmployee: string;
  firstName: string;
  lastName: string;
  email: string;
  password: string;
}

function Register() {
  const [step, setStep] = useState(1);
  const [employment, setEmployment] = useState<string>("");
  const [isEmployer, setEmployer] = useState(false);
  const [isEmployee, setEmployee] = useState(false);
  const [firstName, setFirstName] = useState<string>("");
  const [lastName, setlastName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [errors, setErrors] = useState<Errors>({
    isEmployer: "",
    isEmployee: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });

  function register() {
    axios
      .post("http://localhost:8000/api/v1/user/register", {
        first_name: firstName,
        last_name: lastName,
        is_employee: isEmployee,
        is_employer: isEmployer,
        email: email,
        password: password,
      })
      .then(function (response) {
        setStep(4);
      })
      .catch(function (error) {
        let errorData: object = error.response.data;
        let newErrors: Errors = { ...errors };

        Object.keys(newErrors).forEach((key) => {
          let camalKey = key.replace(/_([a-z])/g, (match, letter) =>
            letter.toUpperCase(),
          );
          newErrors[camalKey as keyof Errors] = "";
        });

        setErrors(newErrors);

        Object.entries(errorData).forEach(([key, value]) => {
          let camalKey = key.replace(/_([a-z])/g, (match, letter) =>
            letter.toUpperCase(),
          );
          newErrors[camalKey as keyof Errors] = value[0];

          let field = document.getElementById(camalKey);
          field?.classList.add("error-field");
        });

        setErrors(newErrors);
        setStep(1);
      });
  }

  function nextStep() {
    setStep(step + 1);
  }

  function prevStep() {
    setStep(step - 1);
  }

  function handleEmploymentChange(event: React.ChangeEvent<HTMLSelectElement>) {
    let value = event.target.value;
    setEmployment(value);
    if (value == "Employer") {
      setEmployer(true);
      setEmployee(false);
    } else if (value == "Employee") {
      setEmployee(true);
      setEmployer(false);
    }
  }

  function handelFieldChange(event: React.ChangeEvent<HTMLInputElement>) {
    let target = event.target;
    if (target.id == "firstName") {
      setFirstName(target.value);
    }
    if (target.id == "lastName") {
      setlastName(target.value);
    }
    if (target.id == "email") {
      setEmail(target.value);
    }
    if (target.id == "password") {
      setPassword(target.value);
    }
  }
  const handleEmailBlur = (event: React.FocusEvent<HTMLInputElement>) => {
    const newEmail = event.target.value;
    let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    let isEmailValid = emailPattern.test(newEmail);
    let newErrors: Errors = { ...errors };

    if (!isEmailValid) {
      newErrors.email = "Enter a valid email address.";
      setErrors(newErrors);

      let emailField = document.getElementById("email");
      emailField?.classList.add("error-field");
    } else {
      newErrors.email = "";
      setErrors(newErrors);

      let emailField = document.getElementById("email");
      emailField?.classList.remove("error-field");
    }
  };

  let nextButton = (
    <button
      className="pagination-button"
      type="button"
      onClick={nextStep}
      disabled={step == 1 ? !employment : !firstName || !lastName}
    >
      Next
    </button>
  );
  let prevButton = (
    <button className="pagination-button" type="button" onClick={prevStep}>
      Back
    </button>
  );

  let employmentForm = (
    <div className="form-section">
      <select
        id="selectEmployment"
        value={employment}
        onChange={handleEmploymentChange}
      >
        <option value="" disabled>
          Select Employment
        </option>
        <option value="Employer">Employer</option>
        <option value="Employee">Employee</option>
      </select>
      {nextButton}
    </div>
  );

  let profileForm = (
    <div className="form-section">
      <input
        type="text"
        id="firstName"
        value={firstName}
        placeholder="First Name"
        onChange={handelFieldChange}
        className={errors.firstName ? "error-field" : ""}
      />
      <p id="firstNameError" className="error">
        {errors.firstName}
      </p>
      <input
        type="text"
        id="lastName"
        value={lastName}
        placeholder="Last Name"
        onChange={handelFieldChange}
        className={errors.lastName ? "error-field" : ""}
      />
      <p id="lastNameError" className="error">
        {errors.lastName}
      </p>
      {prevButton}
      {nextButton}
    </div>
  );

  let userForm = (
    <div className="form-section">
      <input
        id="email"
        type="email"
        value={email}
        placeholder="Email"
        onChange={handelFieldChange}
        className={errors.email ? "error-field" : ""}
        onBlur={handleEmailBlur}
      />
      <p id="emailError" className="error">
        {errors.email}
      </p>
      <input
        id="password"
        type="password"
        value={password}
        placeholder="Password"
        onChange={handelFieldChange}
        className={errors.password ? "error-field" : ""}
      />
      <p id="passwordError" className="error">
        {errors.password}
      </p>
      {prevButton}
      <button
        id="registerButton"
        className="register-button"
        type="submit"
        disabled={!email || !password}
        onClick={register}
      >
        Register
      </button>
    </div>
  );

  let successMsg = (
    <div className="form-section">
      <p className="success-msg">
        We sent code on your email, to activate account.{" "}
        <a href="/activate-user" className="activate-user">
          Activate user
        </a>
      </p>
    </div>
  );

  return (
    <div className="register-container">
      <div className="register-box">
        {step == 1 && employmentForm}
        {step == 2 && profileForm}
        {step == 3 && userForm}
        {step == 4 && successMsg}
      </div>
    </div>
  );
}

export default Register;
