export interface Errors {
    id : string,
    license : string,
    email : string,
    isEmailCertified : boolean,
    password : string,
    checkPassword : string,
}

export default function validate({ id, license, email, password, emailValue ,isEmailCertified, checkPassword }) {
    const errors = {} as Errors;

    console.log(license);

    if (!email) {
        errors.email = "이메일이 입력되지 않았습니다.";
    } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(email+'@'+emailValue)) {
        errors.email = "입력된 이메일이 유효하지 않습니다.";
    } else if (!isEmailCertified) {
        errors.email = "이메일 검증이 완료되지 않았습니다.";
    }

    if (!password) {
        errors.password = "비밀번호가 입력되지 않았습니다.";
    } else if (password.length < 8) {
        errors.password = "8자 이상의 패스워드를 사용해야 합니다.";
    }

    if (!license) {
        errors.license = "의사번호가 입력되지 않았습니다.";
    }

    if (!id) {
        errors.id = "아이디가 입력되지 않았습니다."
    }

    return errors;
}
