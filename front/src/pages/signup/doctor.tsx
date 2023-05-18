import Layout from "@md/components/layout";
import Navigation from "@md/components/navigation";
import Head from "next/head";
import useForm  from "@md/hooks/useForm";
import validate from "@md/hooks/validate";
import axios from "@md/hooks/axiosInstance";
import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { DoctorSign } from "@md/interfaces/user.interface";

export default function Doctor () {
    const router = useRouter();

    const { values, errors, submitting, success, codeCheck, certifyCode, certifyId, certifyEmail, handleChange, handleSubmit } = useForm({
        initialValues: { login: false, id: "", name: "", license: "", hospitalname: "", email: "" , emailValue: "gmail.com", password: "", checkPassword: "", isIdCertified: false, isEmailCertified: false, isCodeCertified: false, type: "doctor"},
        onSubmit: (values : any) => {
            const data : DoctorSign = {
                id : values.id,
                name : values.name,
                password : values.password,
                email : values.email + "@" + values.emailValue,
                doctornum : parseInt(values.license),
                hospitalname : values.hospitalname,
                type : values.type
            };
            axios.post('/api/signup', data as DoctorSign).then(response => {
                if(response.status === 200) {
                    alert("회원가입에 성공하셨습니다.");
                    router.push('/');
                }
            });
        },
        validate,
    });

    useEffect(() => {
        success["id"] = "";
    }, [values.id]);

    useEffect(() => {

    }, [errors]);

    return (
        <div>
            <Head>
                <title>모션 닥터 | 의사 회원가입</title>
                <meta name="description" content="Generated by create next app" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <Navigation></Navigation>

            <Layout>
                <div className="flex flex-col justify-center items-center">
                    <div className="w-[40%] mt-10">
                        <div className="text-xl font-bold mb-4">의사 회원가입</div>
                        <form className="flex flex-col gap-4"
                              onSubmit={handleSubmit} noValidate>
                            <div className="flex gap-1 flex-col">
                                <div className="flex gap-2 items-center">
                                    <label className="w-[120px] font-semibold">아이디</label>
                                    <input
                                        type="id"
                                        name="id"
                                        value={values.id}
                                        onChange={handleChange}
                                        placeholder="아이디 입력해주세요"
                                        className={`${errors.id && "border-color-danger-500"} w-[calc(100%-50px)] focus:outline-none border border-gray-300 rounded-sm pl-1 py-0.5`}
                                    />
                                    <button onClick={certifyId} type={"button"} className="bg-stone-500 font-bold text-white min-w-fit py-1 w-[50px]">중복</button>
                                </div>
                                {errors.id && <div className="text-color-danger-500 text-sm pl-[100px]">{errors.id}</div>}
                                {success.id && <div className="text-color-success-500 text-sm pl-[100px]">{success.id}</div>}
                            </div>
                            <div className="flex gap-1 flex-col">
                                <div className="flex gap-2 items-center">
                                    <label className="w-[120px] font-semibold">이름</label>
                                    <input
                                        type="name"
                                        name="name"
                                        value={values.name}
                                        onChange={handleChange}
                                        placeholder="이름을 입력해주세요"
                                        className={`${errors.name && "border-color-danger-500"} w-full focus:outline-none border border-gray-300 rounded-sm pl-1 py-0.5`}
                                    />
                                </div>
                                {errors.name && <div className="text-color-danger-500 text-sm pl-[100px]">{errors.name}</div>}
                            </div>
                            <div className="flex gap-1 flex-col">
                                <div className="flex gap-2 items-center">
                                    <label className="w-[120px] font-semibold">의사면허번호</label>
                                    <input
                                        type="license"
                                        name="license"
                                        value={values.license}
                                        onChange={handleChange}
                                        placeholder="의사번호를 입력해주세요"
                                        className={`${errors.license && "border-color-danger-500"} w-full focus:outline-none border border-gray-300 rounded-sm pl-1 py-0.5`}
                                    />
                                </div>
                                {errors.license && <div className="text-color-danger-500 text-sm pl-[100px]">{errors.license}</div>}
                            </div>
                            <div className="flex gap-1 flex-col">
                                <div  className="flex gap-2 items-center">
                                    <label className="w-[120px] font-semibold">병원 이름</label>
                                    <input
                                        type="hospitalname"
                                        name="hospitalname"
                                        value={values.hospitalname}
                                        onChange={handleChange}
                                        placeholder="병원 이름을 입력해주세요"
                                        className={`${errors.hospitalname && "border-color-danger-500"} w-full focus:outline-none border border-gray-300 rounded-sm pl-1 py-0.5`}
                                    />
                                </div>
                                {errors.hospitalname && <div className="text-color-danger-500 text-sm pl-[100px]">{errors.hospitalname}</div>}
                            </div>
                            <div className="flex gap-1 flex-col">
                                <div className="flex gap-2 items-center">
                                    <label className="w-[120px] font-semibold">이메일</label>
                                    <input
                                        type="email"
                                        name="email"
                                        value={values.email}
                                        onChange={handleChange}
                                        placeholder="이메일 입력"
                                        className={`${errors.email && "border-color-danger-500"} w-[calc(100%-290px)] focus:outline-none border border-gray-300 rounded-sm pl-1 py-0.5`}
                                    />
                                    <label>@</label>
                                    <select name="emailValue"
                                            value={values.emailValue}
                                            onChange={handleChange}
                                            className="box-border border border-gray-300 w-[200px] p-1 rounded-sm">
                                        <option value="gmail.com">gmail.com</option>
                                        <option value="naver.com">naver.com</option>
                                        <option value="kakao.com">kakao.com</option>
                                        <option value="nate.com">nate.com</option>
                                    </select>
                                    <button onClick={certifyEmail} type="button" className="bg-stone-500 font-bold text-white min-w-fit py-1 w-[50px]">인증</button>

                                </div>
                                {errors.email && <div className="text-color-danger-500 text-sm pl-[100px]">{errors.email}</div>}

                            </div>

                            <div className=" flex gap-1 flex-col">
                                <div className="flex gap-2 items-center">
                                    <label className="w-[120px] font-semibold">이메일 코드</label>
                                    <input
                                        type="text"
                                        name="emailCode"
                                        value={values.emailCode}
                                        onChange={handleChange}
                                        placeholder="이메일 검증 코드를 입력해주세요"
                                        className={`${errors.emailCode && "border-color-danger-500"} w-[calc(100%-50px)] focus:outline-none border border-gray-300 rounded-sm pl-1 py-0.5`}
                                    />
                                    <button onClick={certifyCode} type={"button"} className="bg-stone-500 font-bold text-white min-w-fit py-1 w-[50px]">인증</button>
                                </div>
                                {errors.emailCode && <div className="text-color-danger-500 text-sm pl-[100px]">{errors.emailCode}</div>}
                                {success.emailCode && <div className="text-color-success-500 text-sm pl-[100px]">{success.emailCode}</div>}
                            </div>

                            <div className="flex gap-1 flex-col">
                                <div className="flex gap-2">
                                    <label className="w-[120px] font-semibold">비밀번호</label>
                                    <input
                                        type="password"
                                        name="password"
                                        value={values.password}
                                        onChange={handleChange}
                                        placeholder="비밀번호를 입력해주세요"
                                        className={`${errors.password && "border-color-danger-500"} w-full focus:outline-none border border-gray-300 rounded-sm pl-1 py-0.5`}
                                    />
                                </div>
                                {errors.password && <div className="text-color-danger-500 text-sm pl-[100px]">{errors.password}</div>}
                            </div>

                            <div className="flex gap-1 flex-col">
                                <div className="flex gap-2">
                                    <label className="w-[120px] font-semibold">비밀번호 확인</label>
                                    <input
                                        type="password"
                                        name="checkPassword"
                                        value={values.checkPassword}
                                        onChange={handleChange}
                                        placeholder="비밀번호를 다시 확인해주세요"
                                        className={`${errors.checkPassword && "border-color-danger-500"} w-full focus:outline-none border border-gray-300 rounded-sm pl-1 py-0.5`}
                                    />
                                </div>
                                {errors.checkPassword && <div className="text-color-danger-500 text-sm pl-[100px]">{errors.checkPassword}</div>}
                            </div>


                            <button className="bg-color-primary-500 text-white font-bold py-0.5" type="submit" disabled={submitting}>회원가입하기</button>
                        </form>
                    </div>
                </div>
            </Layout>
        </div>
    );
};