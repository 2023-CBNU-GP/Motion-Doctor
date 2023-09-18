import styles from "@md/styles/Timer.module.css";

export default function Timer({time}: { time: number }) {
    return (
        <div className={`z-50 absolute h-screen w-screen backdrop-brightness-100 backdrop-blur`}>
            <div className={`relative w-full h-full flex flex-col justify-center items-center`}>
                <div className={`${styles.loading_cycle} absolute`}></div>
                <div className={`font-bold text-lg text-white`}>{time}</div>
            </div>
        </div>
    );
}