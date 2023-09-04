import requests
import argparse
import logging
from os import getcwd
import pathlib
import wandb

#url = "https://github.com/someguy/brilliant/blob/master/somefile.txt"

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()



def get_data(args):
    basename = pathlib.Path(args.url).name.split("?")[0].split("#")[0]
    directory = getcwd() + f"\{basename}"   

    logger.info(f"basename: {basename} ...")   

    with open(basename,'wb+') as f:
        logger.info("Creating run")
        with wandb.init(project=args.project_name, job_type="download_data") as run:

            # Download the file streaming and write to open file
            with requests.get(args.url, stream=True) as r:
                f.write(r.content)
                
                logger.info("Creating artifact")
                
                artifact = wandb.Artifact(
                name=args.artifact_name,
                type=args.artifact_type,
                description=args.artifact_description,
                metadata={'original_url': args.url}
            )
                artifact.add_file(directory, name=basename)

                logger.info("Logging artifact")
                run.log_artifact(artifact)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download a file and upload it as an artifact to W&B", fromfile_prefix_chars="@"
    )

    parser.add_argument(
        "--url", type=str, help="URL to the input file", required=True
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--project_name", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    args = parser.parse_args()

    get_data(args)

