import axios from "axios";
import { error } from "console";
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./activate-user.css";

function ActivateUser() {
  const [isSuccess, setIsSuccess] = useState(false);
  const [isMadeRequest, setIsMadeRequest] = useState(false);
  let params = useParams();
  let userActivationUUID = params.userActivationUUID;

  let successMsg = (
    <p>
      Your account active, now{" "}
      <a href="/login" className="log-in-link">
        log in
      </a>
    </p>
  );

  let errorMsg = <p>Your activate code is incapacitated.</p>;

  if (!isMadeRequest) {
    axios
      .put(
        `http://localhost:8000/api/v1/user/activate-user/${userActivationUUID}`,
      )
      .then(function(response) {
        setIsSuccess(true);
        setIsMadeRequest(true);
      })
      .catch(function(error) {
        setIsSuccess(false);
        setIsMadeRequest(true);
      });
  }

  return (
    <div className="activate-user-container">
      <div className="activate-user-box">
        {isSuccess ? successMsg : errorMsg}
      </div>
    </div>
  );
}

export default ActivateUser;
