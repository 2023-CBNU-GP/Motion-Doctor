import { useEffect, useState } from "react"
import { Errors } from "@md/hooks/validate";
import axios from "@md/utils/axiosInstance";
import { Success } from "@md/interfaces/user.interface";

function useForm({initialValues, onSubmit, validate}: any) {
    const [values, setValues] = useState(initialValues);
    const [errors, setErrors] = useState({} as Errors);
    const [submitting, setSubmitting] = useState(false);
    const [success, setSuccess] = useState({} as Success);
    const [codeCheck, setCodeCheck] = useState<any>(null);

    const certifyId = () => {
        axios.post('/api/id_check', {
            id: values.id,
            type: values.type
        }).then((response) => {
            if (response.status === 200) {
                values["isIdCertified"] = true;
                errors["id"] = "";
                setSuccess({id: "사용가능한 아이디입니다"});
            }
        }).catch(() => {
            errors["id"] = "이미 존재하는 아이디입니다";
        });
    };

    const certifyEmail = () => {
        axios.post('/api/email_check', {
            email: values.email + "@" + values.emailValue,
            type: values.type
        }).then((response) => {
            if (response.status === 200) {
                alert("인증코드를 전송하였습니다");
                values["isEmailCertified"] = true;
                errors["email"] = "";
                setCodeCheck(true);
            }
        });
    };

    const certifyCode = () => {
        axios.post('/api/code_check', {
            email: values.email + "@" + values.emailValue,
            code: parseInt(values.emailCode)
        }).then((response) => {
            if (response.status === 200) {
                setSuccess({emailCode: "이메일 인증이 완료되었습니다"});
                values["isCodeCertified"] = true;
                errors["email"] = "";
            }
        }).catch((error) => {
            errors["emailCode"] = "유효하지 않은 코드 입니다.";
        });
    }


    const handleChange = (event: any) => {
        const {name, value} = event.target;
        setValues({...values, [name]: value});
    }

    const handleSubmit = async (event: any) => {
        setSubmitting(true);
        event.preventDefault();
        setErrors(validate(values));
    }

    useEffect(() => {
        if (submitting) {
            if (Object.keys(errors).length === 0) {
                onSubmit(values);
            }
            setSubmitting(false);
        }
    }, [errors]);

    return {
        values,
        errors,
        submitting,
        success,
        codeCheck,
        certifyCode,
        certifyId,
        certifyEmail,
        handleChange,
        handleSubmit,
    };
}

export default useForm;
