import Head from 'next/head'
import Layout from "@md/components/layout";
import { useState } from "react";
import Link from "next/link";
import useForm from "@md/hooks/useForm";
import validate from "@md/hooks/validate";
import axios from "@md/hooks/axiosInstance";

export interface DoctorLogin {

}

export default function Home() {
    const { values, errors, submitting, handleChange, handleSubmit } = useForm({
        initialValues: { id: "", name: "", license: "", hospitalname: "", email: "" + '', emailValue: "gmail.com", password: "", checkPassword: "", isIdCertified: false, isEmailCertified: false, isCodeCertified: false, type: "doctor"},
        onSubmit: (values) => {
            if (values.type === "doctor") {
                const data : DoctorSign = {
                    id : values.id,
                    name : values.name,
                    password : values.password,
                    email : values.email,
                    doctornum : parseInt(values.doctornum),
                    hospitalname : values.hospitalname,
                    type : values.type
                };
                axios.post('/api/signup', data <DoctorSign>).then(response => {
                    if(response.status === 200) {
                        alert("회원가입에 성공하셨습니다.");
                        router.push('/');
                    }
                });
            }
        },
        validate,
    });


    const [isLogin, setIsLogin] = useState(false);
    const [isPatient, setIsPatient] = useState(true);

    const [user, setUser] = useState({
        userID : '',
        password: ''
    });

    const handleInputChange = (e) => {
        setUser({ ...user, [e.target.name]: e.target.value });
    };

  return (
    <>
        { isLogin ?
            <Layout>
                <Head>
                    <title>모션 닥터 | 메인페이지</title>
                    <meta name="description" content="Generated by create next app" />
                    <meta name="viewport" content="width=device-width, initial-scale=1" />
                    <link rel="icon" href="/favicon.ico" />
                </Head>
                <main>
                    메인페이지
                </main>
            </Layout>
            :

            <div className="bg-gray-50 h-screen">
                <Layout>
                <Head>
                    <title>모션 닥터 | 로그인</title>
                    <meta name="description" content="Generated by create next app" />
                    <meta name="viewport" content="width=device-width, initial-scale=1" />
                    <link rel="icon" href="/favicon.ico" />
                </Head>
                <main className="flex justify-center pt-20">
                    <div className="bg-white px-28 w-2/3 drop-shadow-xl rounded-2xl py-20">
                        <div className="text-5xl font-bold text-color-primary-500">Motion</div>
                        <div className="text-5xl font-bold ">Doctor</div>
                        <div className="flex justify-evenly gap-4 pt-10">
                            <div className={`cursor-pointer px-6 py-1 ${isPatient && "border-b-2 border-color-primary-500 font-bold"}`}
                                 onClick={() => {setIsPatient(true); setUser({userID: '', password: ''});}}>환자용</div>
                            <div className={`cursor-pointer px-6 py-1 ${!isPatient && "border-b-2 border-color-primary-500 font-bold"}`}
                                 onClick={() => {setIsPatient(false); setUser({userID: '', password: ''});}}>의사용</div>
                        </div>
                        <div className="pt-8">
                            {
                                isPatient ?
                                    <form className="flex flex-col gap-5 px-16 items-end">
                                        <div className="flex w-full items-center gap-2 border-b-[1px] border-stone-200 pb-1.5">
                                            <label className="w-24 text-sm pb-1">아이디</label>
                                            <input  name="userID"
                                                    value={user.userID}
                                                    onChange={(e) => {handleInputChange(e)}}
                                                    className="w-full p-1 focus:outline-none" type="text" />
                                        </div>
                                        <div className="flex w-full items-center gap-2 border-b-[1px] border-stone-200 pb-1.5">
                                            <label className="w-24 text-sm pb-1">비밀번호</label>
                                            <input  name="password"
                                                    value={user.password}
                                                    onChange={(e) => {handleInputChange(e)}}
                                                    className="w-full p-1 focus:outline-none" type="password" />
                                        </div>
                                        <div className="flex w-full items-baseline justify-between">
                                            <a className="text-sm text-stone-300 hover:text-color-info-500" href="/signup/patient">회원가입하기</a>
                                            <button className="mt-3 py-1 rounded-sm font-bold bg-color-primary-500 text-white w-[42%]" type="submit">로그인 하기</button>
                                        </div>
                                    </form>
                                    :
                                    <form className="flex flex-col gap-5 px-16 items-end">
                                        <div className="flex w-full items-center gap-2 border-b-[1px] border-stone-200 pb-1.5">
                                            <label className="w-32 text-sm pb-1">의사 면허 번호</label>
                                            <input  name="userID"
                                                    value={user.userID}
                                                    onChange={(e) => {handleInputChange(e)}}
                                                    className="w-full p-1 focus:outline-none" type="text" />
                                        </div>
                                        <div className="flex w-full items-center gap-2 border-b-[1px] border-stone-200 pb-1.5">
                                            <label className="w-32 text-sm pb-1">비밀번호</label>
                                            <input  name="password"
                                                    value={user.password}
                                                    onChange={(e) => {handleInputChange(e)}}
                                                    className="w-full p-1 focus:outline-none" type="password" />
                                        </div>
                                        <div className="flex w-full items-baseline justify-between">
                                            <Link className="text-sm text-stone-300 hover:text-color-info-500" href="/signup/doctor">
                                                회원가입하기
                                            </Link>
                                            <button className="mt-3 py-1 rounded-sm font-bold bg-color-primary-500 text-white w-[42%]" type="submit">로그인 하기</button>
                                        </div>
                                    </form>
                            }
                        </div>

                    </div>
                </main>
                </Layout>
            </div>
        }

    </>
  )
}
