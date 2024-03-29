from . import UserViews
from . import EmailViews
from . import FileViews
from . import AdminViews
from . import DoctorViews
from . import PatientViews
from django.urls import path

urlpatterns = [
  path('signup', UserViews.RegisterView.as_view()),
  path('login', UserViews.LoginView.as_view()),
  path('user', UserViews.UserView.as_view()),
  path('logout', UserViews.LogoutView.as_view()),
  path('id_check', UserViews.OverlabId.as_view()),
  path('withdraw', UserViews.UserDrop.as_view()),
  path('modifypw', UserViews.PasswordModify.as_view()),
  path('email_check', EmailViews.EmailView.as_view()),
  path('code_check', EmailViews.EmailCodeView.as_view()),
  path('file_upload', FileViews.FileUpload.as_view()),
  path('file_delete', FileViews.FileDelete.as_view()),
  # path('evaluation', FileViews.PatientEvaluation.as_view()),
  path('isapprove', AdminViews.ApproveRejectDoctor.as_view()),
  path('doctor_list', AdminViews.ListDoctor.as_view()),
  path('video_list', AdminViews.ListDoctorVideo.as_view()),
  path('manage_list', AdminViews.DoctorPatientNum.as_view()),
  path('comment', DoctorViews.DoctorComment.as_view()),
  path('patient_list', DoctorViews.ManagePatientList.as_view()),
  path('test_list', PatientViews.DoctorPatientList.as_view()),
  path('manage/<int:uid>', DoctorViews.PatientTestList.as_view()),
  path('register_video', DoctorViews.DoctorVideo.as_view()),
  path('remove_video', PatientViews.RemoveVideo.as_view()),
  path('check_course', PatientViews.CheckCourse.as_view()),
  # path('approve_patient', DoctorViews.ApprovePatient.as_view()),
  # path('total_patient', DoctorViews.TotalPatientList.as_view())
]
