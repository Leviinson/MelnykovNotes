const registrationWrapper = document.getElementById('reg-steps-wrapper');
const wrapperWidth = registrationWrapper.offsetWidth;
const transitionDuration = window.getComputedStyle(registrationWrapper).transitionDuration;
const prevStepButton = document.getElementById('reg-previous-step__button');
const submitStepButton = document.getElementById('reg-submit-step__button');
const nextStepButton = document.getElementById('reg-next-step__button');

function swipePrevStep() {
    submitStepButton.disabled = true;
    prevStepButton.disabled = true;
    setTimeout(
        () => nextStepButton.disabled = false,
        parseFloat(transitionDuration) * 1000
    );
    registrationWrapper.style.left = registrationWrapper.offsetLeft + wrapperWidth + 'px';
}

function swipeNextStep() {
    nextStepButton.disabled = true;
    setTimeout(() => {
        prevStepButton.disabled = false;
        submitStepButton.disabled = false;
    }, parseFloat(transitionDuration) * 1000);
    registrationWrapper.style.left = registrationWrapper.offsetLeft - wrapperWidth + 'px';
}

function swipeToStepWithErrorsOnReloadPage() {
    const form = document.getElementById('reg-form');
    const steps = Array.from(form.querySelectorAll('fieldset'));
    for (let step of steps) {
        if (step.getElementsByClassName('errorlist').length > 0) {
            prevStepButton.disabled = false
            submitStepButton.disabled = false
            registrationWrapper.style.left = registrationWrapper.offsetLeft - (wrapperWidth * steps.indexOf(step)) + 'px';
            return;
        }
    }
}

function init() {
    swipeToStepWithErrorsOnReloadPage();
}

init();