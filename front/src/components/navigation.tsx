import Link from "next/link";

export default function Navigation () {
    return (
        <div className="px-[120px] py-8 w-full h-10 bg-white drop-shadow sticky top-0 text-center items-center flex flex justify-between">
            <div>
                <Link href="/" className="text-lg font-bold flex gap-2">
                    <div className="text-color-primary-500">Motion</div>
                    <div>Doctor</div>
                </Link>

            </div>

            <div>
                <Link href="/">
                    로그인
                </Link>
            </div>
        </div>
    )
}
