import uuid

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from tasks.models import Task, TaskComment
from teams.models import Team
from users.models import User


@pytest.fixture
def team_factory():
    def create_team(**kwargs):
        name = kwargs.get("name") or f"Test Team {uuid.uuid4().hex[:8]}"

        email = kwargs.get("admin_email") or f"admin_{
            uuid.uuid4().hex}@example.com"
        admin = User.objects.create_user(
            email=email,
            password="password123",
            role=User.Role.MANAGER,
        )

        team = Team.objects.create(
            name=name,
            admin=admin,
        )
        admin.team = team
        admin.save()
        return team

    return create_team


@pytest.fixture
def user_factory(db, team_factory):
    counter = {"n": 0}

    def create_user(**kwargs):
        counter["n"] += 1
        email = kwargs.get("email", f"user{counter['n']}@example.com")
        first_name = kwargs.get("first_name", "Test")
        last_name = kwargs.get("last_name", "User")
        password = kwargs.get("password", "password123")
        role = kwargs.get("role", User.Role.USER)

        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
        )

        team = kwargs.get("team")
        if team is None:
            if role == User.Role.ADMIN_TEAM:
                team = team_factory(admin=user)
            else:
                team = team_factory()
        user.team = team
        user.save()
        return user
    return create_user


@pytest.fixture
def task_factory(db, user_factory, team_factory):
    def create_task(**kwargs):
        defaults = {
            "title": "Test Task",
            "description": "Task description",
            "status": Task.Status.TO_DO,
            "deadline": timezone.now(),
        }
        defaults.update(kwargs)

        if "team" not in defaults:
            defaults["team"] = team_factory()
        if "created_by" not in defaults:
            defaults["created_by"] = defaults["team"].admin
        defaults.setdefault("assignee", None)

        return Task.objects.create(**defaults)
    return create_task


@pytest.fixture
def comment_factory(db, user_factory, task_factory):
    def create_comment(**kwargs):
        defaults = {
            "content": "Test comment",
        }
        defaults.update(kwargs)
        if "task" not in defaults:
            defaults["task"] = task_factory()
        if "author" not in defaults:
            defaults["author"] = defaults["task"].created_by
        return TaskComment.objects.create(**defaults)
    return create_comment


@pytest.fixture
def task_with_assignee(user_factory, task_factory):
    user_creator = user_factory(first_name="Alice", last_name="Creator")
    user_assignee = user_factory(first_name="Bob", last_name="Assignee")
    task = task_factory(
        team=user_creator.team,
        created_by=user_creator,
        assignee=user_assignee)
    return task, user_creator, user_assignee


@pytest.fixture
def comment_for_task(task_with_assignee, user_factory, comment_factory):
    task, _, user_assignee = task_with_assignee
    comment_author = user_factory(first_name="Charlie", last_name="Commenter")
    comment = comment_factory(
        task=task,
        author=comment_author,
        content="Test comment")
    return comment, comment_author, task


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def manager_user(user_factory, team_factory):
    return user_factory(role=User.Role.MANAGER)
    team = team_factory(admin=user)
    user.admin_teams.add(team)
    return user


@pytest.fixture
def regular_user(user_factory):
    return user_factory(role=User.Role.USER)


@pytest.fixture
def task_for_manager(task_factory, manager_user):
    task = task_factory(team=manager_user.team, created_by=manager_user)
    return task


@pytest.fixture
def task_for_user(task_factory, regular_user):
    task = task_factory(
        team=regular_user.team,
        created_by=regular_user,
        assignee=regular_user)
    return task


@pytest.fixture
def manager_with_team_and_task(manager_user, task_factory, team_factory):
    team = team_factory(admin=manager_user)
    manager_user.admin_teams.add(team)
    manager_user.save()
    task = task_factory(team=team, created_by=manager_user)
    return manager_user, team, task


@pytest.fixture
def user_with_team_and_task(regular_user, task_factory, team_factory):
    team = team_factory()
    team.members.add(regular_user)
    team.save()
    task = task_factory(
        team=team,
        created_by=regular_user,
        assignee=regular_user)
    return regular_user, team, task


@pytest.fixture
def comment_for_user_task(user_with_team_and_task, comment_factory):
    user, _, task = user_with_team_and_task
    comment = comment_factory(task=task, author=user)
    return comment
