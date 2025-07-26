// Validate form inputs before submission
function validateForm(formData) {
  for (const [key, value] of formData.entries()) {
    if (!value || value.trim() === "") {
      return false;
    }
    // Validate numeric fields are numbers & non-negative
    if (
      ["applicant_income", "coapplicant_income", "loan_amount", "loan_amount_term"].includes(key)
    ) {
      const num = Number(value);
      if (isNaN(num) || num < 0) {
        return false;
      }
    }
  }
  return true;
}

// Handle form submission
document.getElementById("loanForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  if (!validateForm(formData)) {
    showResult("Please fill all fields correctly.", true);
    return;
  }

  // Prepare data to send to API
  const data = {
    Gender: formData.get("gender"),
    Married: formData.get("married"),
    Dependents: formData.get("dependents"),
    Education: formData.get("education"),
    Self_Employed: formData.get("self_employed"),
    ApplicantIncome: parseFloat(formData.get("applicant_income")),
    CoapplicantIncome: parseFloat(formData.get("coapplicant_income")),
    LoanAmount: parseFloat(formData.get("loan_amount")),
    Loan_Amount_Term: parseFloat(formData.get("loan_amount_term")),
    Credit_History: parseFloat(formData.get("credit_history")),
    Property_Area: formData.get("property_area"),
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/predict/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (result.prediction) {
      showResult(`Prediction: <strong>${result.prediction}</strong>`);
    } else if (result.error) {
      showResult(`Error: ${result.error}`, true);
    } else {
      showResult("Unexpected response from server.", true);
    }
  } catch (error) {
    showResult(`Failed to connect to API: ${error}`, true);
  }
});

function showResult(message, isError = false) {
  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = message;
  resultDiv.style.color = isError ? "red" : "#0052cc";
}
