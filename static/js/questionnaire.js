// Handle the step-by-step questionnaire navigation
document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const questionSteps = document.querySelectorAll('.question-step');
    const nextButtons = document.querySelectorAll('.btn-next');
    const prevButtons = document.querySelectorAll('.btn-prev');
    const progressBar = document.querySelector('.progress-bar');
    const submitButton = document.querySelector('#submit-questionnaire');

    let currentStep = 0;

    // Update progress bar
    function updateProgressBar() {
        const progress = ((currentStep + 1) / questionSteps.length) * 100;
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
    }

    // Show current step and hide others
    function showStep(stepIndex) {
        questionSteps.forEach((step, index) => {
            if (index === stepIndex) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

        // Update button visibility
        updateButtonStates();
        updateProgressBar();
    }

    // Update next/prev button states
    function updateButtonStates() {
        // Show/hide prev button based on current step
        prevButtons.forEach(btn => {
            if (currentStep === 0) {
                btn.classList.add('invisible');
            } else {
                btn.classList.remove('invisible');
            }
        });

        // Show submit button on last step
        if (currentStep === questionSteps.length - 1) {
            nextButtons.forEach(btn => btn.classList.add('d-none'));
            if (submitButton) {
                submitButton.classList.remove('d-none');
            }
        } else {
            nextButtons.forEach(btn => btn.classList.remove('d-none'));
            if (submitButton) {
                submitButton.classList.add('d-none');
            }
        }
    }

    // Go to next step
    function nextStep() {
        // Perform validation if needed
        if (validateCurrentStep()) {
            currentStep = Math.min(currentStep + 1, questionSteps.length - 1);
            showStep(currentStep);
        }
    }

    // Go to previous step
    function prevStep() {
        currentStep = Math.max(currentStep - 1, 0);
        showStep(currentStep);
    }

    // Validate current step
    function validateCurrentStep() {
        const currentQuestionStep = questionSteps[currentStep];
        const requiredInputs = currentQuestionStep.querySelectorAll('input[required], select[required]');

        let isValid = true;

        requiredInputs.forEach(input => {
            if (!input.value) {
                isValid = false;
                // Add invalid class or feedback
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });

        return isValid;
    }

    // Add event listeners for next buttons
    nextButtons.forEach(button => {
        button.addEventListener('click', nextStep);
    });

    // Add event listeners for prev buttons
    prevButtons.forEach(button => {
        button.addEventListener('click', prevStep);
    });

    // Handle budget range inputs
    const budgetMinInput = document.querySelector('#budget_min');
    const budgetMaxInput = document.querySelector('#budget_max');
    const budgetMinValue = document.querySelector('#budget_min_value');
    const budgetMaxValue = document.querySelector('#budget_max_value');

    if (budgetMinInput && budgetMaxInput) {
        // Update display value when slider changes
        budgetMinInput.addEventListener('input', function() {
            budgetMinValue.textContent = formatIndianCurrency(budgetMinInput.value);
            // Ensure min doesn't exceed max
            if (parseInt(budgetMinInput.value) > parseInt(budgetMaxInput.value)) {
                budgetMaxInput.value = budgetMinInput.value;
                budgetMaxValue.textContent = formatIndianCurrency(budgetMaxInput.value);
            }
        });

        budgetMaxInput.addEventListener('input', function() {
            budgetMaxValue.textContent = formatIndianCurrency(budgetMaxInput.value);
            // Ensure max isn't below min
            if (parseInt(budgetMaxInput.value) < parseInt(budgetMinInput.value)) {
                budgetMinInput.value = budgetMaxInput.value;
                budgetMinValue.textContent = formatIndianCurrency(budgetMinInput.value);
            }
        });
    }

    // Handle priority sliders
    const prioritySliders = document.querySelectorAll('.priority-slider');

    prioritySliders.forEach(slider => {
        const valueDisplay = document.querySelector(`#${slider.id}_value`);
        if (valueDisplay) {
            slider.addEventListener('input', function() {
                // Convert numeric value to text representation
                let priorityText;
                switch (parseInt(slider.value)) {
                    case 1: priorityText = 'Not Important'; break;
                    case 2: priorityText = 'Somewhat Important'; break;
                    case 3: priorityText = 'Important'; break;
                    case 4: priorityText = 'Very Important'; break;
                    case 5: priorityText = 'Critical'; break;
                    default: priorityText = 'Important';
                }
                valueDisplay.textContent = priorityText;
            });
        }
    });

    // Format budget values in Indian format
    function formatIndianCurrency(amount) {
        return '₹' + amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }


    // Initialize the first step
    showStep(currentStep);
});