export interface ManagePatients {
    _id: string,
    patientName: string,
    trainCourse: string,
    isCounseled: boolean,
}

export interface ManagePatientDetail {
    _id: string,
    patientName: string,
    trainTitle: string,
    trainList: Array<string>,
    videoList: Array<string | File>,
    scoreList: Array<number>,
}