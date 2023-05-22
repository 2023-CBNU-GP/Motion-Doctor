import fetch from "node-fetch";

export async function getStaticPaths() {
    const res = fetch('http://localhost:3000' + '/')
}

export default function () {
    return (
        <div>

        </div>
    );
}