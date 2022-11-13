let registration_wrapper = document.getElementById('reg-steps-wrapper');
let wrapper_width = registration_wrapper.offsetWidth;

function swipe_next_reg_step() {
    deactivate_swipe_step_button('reg-previous-step__button')
    return registration_wrapper.style.left = registration_wrapper.offsetLeft - wrapper_width + 'px';
}

function swipe_prev_reg_step() {
    deactivate_swipe_step_button('reg-next-step__button')
    return registration_wrapper.style.left = registration_wrapper.offsetLeft + wrapper_width  + 'px';
}

function deactivate_swipe_step_button(button_id) {
    let swipe_step_btn = document.getElementById(button_id)
    swipe_step_btn.setAttribute('disabled', '')
    setTimeout(function () {
        swipe_step_btn.removeAttribute('disabled')
    }, 500)
}

function swipe_to_reg_step_with_errorlist() {
    const reg_form = document.getElementById('reg-form');
    let reg_steps = reg_form.querySelectorAll('fieldset')

    for (let reg_step_number = 0; reg_step_number <= reg_steps.length; reg_step_number++) {
        let reg_step = reg_steps[reg_step_number]
        const error_list = reg_step.getElementsByClassName('errorlist')
        if ( error_list !== undefined ) {
            return registration_wrapper.style.left = registration_wrapper.offsetLeft - (wrapper_width * reg_step_number) + 'px';
        }
    }
}

function init() {
    swipe_to_reg_step_with_errorlist();
}

init();
