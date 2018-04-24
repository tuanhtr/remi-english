# -*- coding: utf-8 -*-
"""
Account Manage Module
"""
from django.db import IntegrityError, transaction
from default.logic.createcourselogic import *
from django.shortcuts import render, redirect
from default.config.config_menu import *
from default.logic.loglogic import *
from .authen import check_login
from helper.lagform import *
from django.http import JsonResponse


@check_login
@transaction.atomic(using=DatabaseRouter.data_database)
def list_courses(request):

    logging_user = LoginUser.get_login_user()
    params = request.POST
    if not logging_user.is_view_right():
        return
    action = params.get('action_type', 0)
    action = int(action)
    part_id = int(params.get('lesson_id', 0))

    # if action == 1:
    #     #is edit
    #     result = CreateCourseLogic.edit_lesson(lesson_id)
    #     edit_form = LagForm()
    #     edit_form.set_form_name('create_course_form')
    #     edit_form.set_action('/create_course/')
    #     edit_form.set_title("Edit Course")
    #     context = {
    #         'user': logging_user,
    #         'keuForm': edit_form,
    #         'screen_name': ScreenName.CreateCourse
    #     }
    #
    #     return render(request, 'create_course.html', context)

    if action == 2:
        #delete
        keu_form = LagForm()
        keu_form.set_form_name('create_course_form')
        keu_form.set_action('/list_courses/')
        keu_form.set_title("Course List")
        CreateCourseLogic.delete_part(part_id)

        context = {
            'user': logging_user,
            'keuForm': keu_form,
            'screen_name': ScreenName.CreateCourse,
        }
        return render(request, 'create_course.html', context)

    keu_form = LagForm()
    keu_form.set_form_name('create_course_form')
    keu_form.set_action('/list_courses/')
    keu_form.set_title("Course List")

    # List course
    test_dict = CreateCourseLogic.get_course_list()
    keu_form.set_list_course(test_dict)
    context = {
        'user': logging_user,
        'keuForm': keu_form,
        'screen_name': ScreenName.CreateCourse,
    }

    return render(request, 'list_courses.html', context)
