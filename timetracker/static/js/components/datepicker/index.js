import flatpickr from 'flatpickr';
import 'flatpickr/dist/flatpickr.min.css';

export default () => {
    flatpickr('.js-datetime-picker', {
        enableTime: true,
    });
};