import re
from django.urls import path, re_path
from pytest_django.asserts import test_case

from apps.testcases.apis import views


app_name = 'testcases'

urlpatterns = [
    path('test-case/', views.TestCaseListView.as_view()),
    path('create/test-case/', views.TestCaseView.as_view()),
    path('test-step/', views.TestCaseStepView.as_view()),
    path('test-step/<int:id>/', views.TestStepDeleteView.as_view()),
    path('test-case/history/', views.DemoHistoryView.as_view()),
    path('test-case/<int:id>/', views.TestCaseDetailView.as_view(), name='testcase-details'),
    path('test-case/natco/<int:id>/', views.TestCaseNatcoView.as_view(), name='testcase-natco'),
    path('test-case/natco-list/', views.TestCaseNatcoList.as_view(), name='natco-list'),
    path('test-case/natco-list/<int:pk>/', views.TestCaseNatcoDetail.as_view(), name='natco-details'),
    path('report-filter/', views.TestResultFilterView.as_view()),
    path('testcase-filters/', views.FiltersView.as_view()),
    path('navbar-filter/', views.NavBarFilter.as_view()),
    path('report-data/', views.TestCaseReportView.as_view()),
    path('test-route/<str:type>/', views.TestCaseDetailReport.as_view()),
    path('testing/', views.TestView.as_view()),
    path('test/', views.ReportView.as_view()),
    path('tes/', views.TestReportGraphView.as_view()),
    path('demo/', views.DemoView.as_view()),
    path('testcase/issues/<int:id>/', views.ScriptIssueView.as_view()),
    path('testcase/issue-detail/<int:id>/', views.ScriptIssueDetailView.as_view(), name='testcase-issue-detail'),
    path('testcase/issues/comment/<int:id>/', views.CommentsView.as_view()),
    path('testcase/issues/comment-detail/<int:pk>/', views.CommentEditView.as_view()),
    re_path(r"excel/(?P<path>.*)$", views.ExcelUploadView.as_view()),
    re_path(r"update-bulk/(?P<path>.*)$", views.BulkFieldUpdateView.as_view())

]
