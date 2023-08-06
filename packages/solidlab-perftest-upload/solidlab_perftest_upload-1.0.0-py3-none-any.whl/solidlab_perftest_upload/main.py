import logging
import mimetypes
import sys
import requests
import click

from solidlab_perftest_common.upload_artifact import (
    upload_artifact_file,
    upload_artifact,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


def validate_perftest_endpoint(ctx, param, value: str) -> str:
    if not isinstance(value, str):
        raise click.BadParameter(
            f"perftest_endpoint must be a URL (and thus a string and not {type(value)})"
        )
    if not value.startswith("https://") and not value.startswith("http://"):
        raise click.BadParameter("perftest_endpoint must be a URL")
    if "/perftest/" not in value:
        raise click.BadParameter(
            "perftest_endpoint must be a perftest endpoint (ant thus contain /perftest/)"
        )
    if (
        value.endswith("/")
        or value.endswith("perftest/")
        or value.endswith("perftest")
        or value.endswith("artifact")
        or value.endswith("artifact/")
    ):
        raise click.BadParameter("perftest_endpoint must be a perftest endpoint")
    return value


@click.command()
@click.argument(
    "perftest_endpoint", type=click.STRING, callback=validate_perftest_endpoint
)
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--mime-type",
    default=None,
    type=click.STRING,
    help="Mime-type of file (default: auto based on extension)",
)
@click.option(
    "--type",
    "attach_type",
    type=click.Choice(["GRAPH", "CSV", "LOG", "OTHER"], case_sensitive=False),
    prompt=True,
    help="Type of attachment",
)
@click.option("--sub-type", prompt=True, type=click.STRING, help="The subtype.")
@click.option("--description", prompt=True, help="Description of the file.")
def main(
    perftest_endpoint, filename, mime_type, attach_type, sub_type, description
) -> int:
    with requests.Session() as session:
        attachment_id, attachment_url = upload_artifact_file(
            session,
            perftest_endpoint=perftest_endpoint,
            attach_type=attach_type,
            sub_type=sub_type,
            description=description,
            filename=filename,
            content_type=mime_type,
        )
        click.echo(
            f"Uploaded: {sub_type} {attach_type} to {attachment_id} at {attachment_url}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
