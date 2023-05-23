export interface Success {
    id?: string,
    email?: string,
    emailCode?: string,
}

export interface DoctorSign {
    _id?: string,
    id: string,
    name: string,
    password?: string,
    email: string,
    doctornum: number,
    hospitalname: string,
    type?: string
    state?: boolean,
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

export interface DoctorInfo {
    _id: string,
    name: string,
    hospitalname?: string,
    patientNum?: number,
}