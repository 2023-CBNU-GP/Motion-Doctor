export const debounce = (fn: Function, delay = 1000) => {
    let timeout: ReturnType<typeof setTimeout>;
    return function (value: object) {
        if (timeout) clearTimeout(timeout as ReturnType<typeof setTimeout>);
        timeout = setTimeout(() => {
            fn(value);
        }, delay);
    };
};
