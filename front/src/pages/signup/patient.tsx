import Head from "next/head";
import Navigation from "@md/components/navigation";
import Layout from "@md/components/layout";
import useForm from "@md/hooks/useForm";
import validate from "@md/hooks/validate";

export default function Patient () {
    const { values, errors, submitting, handleChange, handleSubmit } = useForm({
        initialValues: { id: "", email: "", password: "", emailValue: "gmail.com"},
        onSubmit: (values) => {
            alert(JSON.stringify(values, null, 2));
        },
        validate,
    });

    return (
        <div>
            <Head>
                <title>모션 닥터 | 환자 회원가입</title>
                <meta name="description" content="Generated by create next app" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <Navigation></Navigation>

            <Layout>
                <div className="flex flex-col justify-center items-center">
                    <div className="w-[40%] mt-28">
                        <div className="text-xl font-bold mb-4">환자 회원가입</div>
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
                                        placeholder="아이디를 입력해주세요"
                                        className={`${errors.id && "border-color-danger-500"} w-[calc(100%-50px)] focus:outline-none border border-gray-300 rounded-sm pl-1 py-0.5`}
                                    />
                                    <button type={"button"} className="bg-stone-500 font-bold text-white min-w-fit py-1 w-[50px]">인증</button>
                                </div>
                                {errors.id && <div className="text-color-danger-500 text-sm pl-[100px]">{errors.id}</div>}
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
                                    <button type="button" className="bg-stone-500 font-bold text-white min-w-fit py-1 w-[50px]">인증</button>

                                </div>
                                {errors.email && <div className="text-color-danger-500 text-sm pl-[100px]">{errors.email}</div>}
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
                                        className={`${errors.email && "border-color-danger-500"} w-full focus:outline-none border border-gray-300 rounded-sm pl-1 py-0.5`}
                                    />
                                </div>
                                {errors.password && <div className="text-color-danger-500 text-sm pl-[100px]">{errors.password}</div>}
                            </div>

                            <div className="flex gap-1 flex-col">
                                <div className="flex gap-2">
                                    <label className="w-[120px] font-semibold">비밀번호 확인</label>
                                    <input
                                        type="password"
                                        name="password"
                                        value={values.password}
                                        onChange={handleChange}
                                        placeholder="비밀번호를 다시 확인해주세요"
                                        className={`${errors.email && "border-color-danger-500"} w-full focus:outline-none border border-gray-300 rounded-sm pl-1 py-0.5`}
                                    />
                                </div>
                                {errors.password && <div className="text-color-danger-500 text-sm pl-[100px]">{errors.password}</div>}
                            </div>


                            <button className="bg-color-primary-500 text-white font-bold py-0.5" type="submit" disabled={submitting}>회원가입하기</button>
                        </form>
                    </div>
                </div>
            </Layout>
        </div>
    );
}