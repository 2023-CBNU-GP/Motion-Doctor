export interface Errors {
    id : string,
    name : string,
    license : string,
    hospitalname : string,
    email : string,
    emailCode : string,
    password : string,
    checkPassword : string,
    isEmailCertified : boolean,
    isIdCertified: boolean,
    type: string
}

export default function validate({ login, id, name, license, hospitalname, email, emailValue, password, checkPassword, isEmailCertified, isIdCertified, emailCode, type }) {
    const errors = {} as Errors;
    if (login) {
        if (!id) {
            errors.id = "아이디가 입력되지 않았습니다.";
        }

        if (!password) {
            errors.password = "비밀번호가 입력되지 않았습니다.";
        }

    } else {
        if (type === "doctor") {
            if (!license) {
                errors.license = "의사번호가 입력되지 않았습니다.";
            } else if (!/^[0-9]/.test(license)) {
                errors.license = "유효한 양식이 아닙니다.";
            }

            if (!hospitalname) {
                errors.hospitalname = "병원 이름이 입력되지 않았습니다.";
            }
        }

        if (!id) {
            errors.id = "아이디가 입력되지 않았습니다.";
        } else if(!isIdCertified) {
            errors.id = "아이디 중복 확인이 완료되지 않았습니다.";
        }

        if (!name) {
            errors.name = "이름이 입력되지 않았습니다.";
        }

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

        if (!checkPassword){
            errors.checkPassword = "비밀번호가 입력되지 않았습니다.";
        } else if (checkPassword !== password) {
            errors.checkPassword = "비밀번호가 동일하지 않습니다.";
        }
    }

    return errors;
}
