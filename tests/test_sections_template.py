from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from solidcam_api import SolidCAMClient
from solidcam_api.exceptions import SolidCAMAPIError
from solidcam_api.models import ProcessTemplateEntry, TemplateEntry


def test_template_count_returns_int(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.TemplateCount = 5
    assert connected_client.template_count == 5


def test_template_count_returns_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.TemplateCount = 0
    assert connected_client.template_count == 0


def test_get_template_name_returns_string(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetTemplateName.return_value = "Roughing_Template"
    result = connected_client.get_template_name(0)
    assert result == "Roughing_Template"


def test_get_template_returns_entry(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.GetTemplateName.return_value = "Template"
    result = connected_client.get_template(0)
    assert isinstance(result, TemplateEntry)
    assert result.index == 0
    assert result.name == "Template"


def test_list_templates_returns_empty(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.TemplateCount = 0
    assert connected_client.list_templates() == []


def test_list_templates_returns_list(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.TemplateCount = 2
    fake_com.GetTemplateName.side_effect = ["T1", "T2"]
    result = connected_client.list_templates()
    assert len(result) == 2
    assert all(isinstance(t, TemplateEntry) for t in result)


def test_create_job_from_template_calls_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    connected_client.create_job_from_template("Template", "Geometry", 1)
    fake_com.CreateJobFromTemplate.assert_called_once()


def test_create_job_from_template_raises_on_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 1
    with pytest.raises(SolidCAMAPIError):
        connected_client.create_job_from_template("Template", "Geometry", 1)


def test_process_template_count_returns_int(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ProcessTemplateCount = 3
    assert connected_client.process_template_count == 3


def test_process_template_count_returns_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ProcessTemplateCount = 0
    assert connected_client.process_template_count == 0


def test_get_process_template_name_returns_string(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetProcessTemplateName.return_value = "Mill_Process"
    result = connected_client.get_process_template_name(0)
    assert result == "Mill_Process"


def test_get_process_template_returns_entry(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetProcessTemplateName.return_value = "Process"
    result = connected_client.get_process_template(0)
    assert isinstance(result, ProcessTemplateEntry)
    assert result.index == 0
    assert result.name == "Process"


def test_list_process_templates_returns_empty(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ProcessTemplateCount = 0
    assert connected_client.list_process_templates() == []


def test_list_process_templates_returns_list(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ProcessTemplateCount = 2
    fake_com.GetProcessTemplateName.side_effect = ["P1", "P2"]
    result = connected_client.list_process_templates()
    assert len(result) == 2
    assert all(isinstance(p, ProcessTemplateEntry) for p in result)


def test_create_jobs_from_process_template_calls_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    connected_client.create_jobs_from_process_template("Process", "Geometry", 1)
    fake_com.CreateJobsFromProcessTemplate.assert_called_once()


def test_create_jobs_from_process_template_raises_on_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 1
    with pytest.raises(SolidCAMAPIError):
        connected_client.create_jobs_from_process_template("Process", "Geometry", 1)
