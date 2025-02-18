from datetime import datetime

from github import Github, GithubException, InputFileContent


def format_datetime_into_date(
    date: str | datetime, input_format: str, output_format: str
) -> str:
    if isinstance(date, str):
        date = datetime.strptime(date, input_format)
        format_date = date.strftime(output_format)
    else:
        format_date = date.strftime(output_format)
    return format_date


def create_gist(token: str, gist_name: str, content: str):
    g = Github(token)
    user = g.get_user()
    try:
        gist_file = {gist_name: InputFileContent(content)}
        gist = user.create_gist(
            public=True,
            files=gist_file,
            description='Weather forecast message',
        )
    except GithubException as e:
        raise GithubException(e.message)
    return gist.html_url
