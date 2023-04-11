export interface Success {
    id: string,
    email: string,
}

export interface DoctorSign {
    name: string,
    id: string,
    password: string,
    email: string,
    doctornum: number,
    hospitalname: string,
    type: string

}

export interface PatientSign {
    name: string,
    id: string,
    password: string,
    email: string,
    type: string
}

export interface UserLogin {
    id: string,
    password: string,
    type: string
}