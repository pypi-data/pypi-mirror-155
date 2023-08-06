import argparse
from .io import (
    update_grader_and_notebook_version,
    update_notebook_version,
    tag_notebook,
    init_grader,
    generate_learner_version,
    grade_parts,
)
from .config import Config


def parse_dlai_grader_args() -> None:
    """Parses command line flags and performs desired actions"""
    parser = argparse.ArgumentParser(
        description="Helper library to build automatic graders for DLAI courses."
    )
    parser.add_argument(
        "-i",
        "--init",
        action="store_true",
        help="Initialize a grader workspace with common files and directories.",
    )
    parser.add_argument(
        "-u",
        "--upgrade",
        action="store_true",
        help="Upgrade the grader and notebook version.",
    )
    parser.add_argument(
        "-v",
        "--versioning",
        action="store_true",
        help="Add version to notebook metadata that matches current grader version.",
    )
    parser.add_argument(
        "-t",
        "--tag",
        action="store_true",
        help="Add graded tag to all code cells of notebook.",
    )
    parser.add_argument(
        "-l",
        "--learner",
        action="store_true",
        help="Generate learner facing version.",
    )
    parser.add_argument(
        "-g",
        "--grade",
        action="store_true",
        help="Grade using coursera_autograder tool.",
    )
    parser.add_argument(
        "-p",
        "--partids",
        type=str,
        help="Partids encoded as a single string separated by spaces.",
    )
    parser.add_argument(
        "-d",
        "--docker",
        type=str,
        help="Docker image to use for grading.",
    )
    parser.add_argument(
        "-m",
        "--memory",
        type=str,
        help="Memory to assign to the container.",
    )
    parser.add_argument(
        "-s",
        "--submission",
        type=str,
        help="Submission directory.",
    )
    args = parser.parse_args()
    c = Config()
    if args.init:
        init_grader()
    if args.upgrade:
        update_grader_and_notebook_version()
    if args.versioning:
        update_notebook_version(
            path="./mount/submission.ipynb", version=c.latest_version
        )
    if args.tag:
        tag_notebook("./mount/submission.ipynb")
    if args.learner:
        generate_learner_version(
            filename_source="./mount/submission.ipynb",
            filename_target=f"./learner/{c.assignment_name}.ipynb",
        )
    if args.grade:
        if not args.partids:
            print("partids not provided")
            return
        if not args.docker:
            print("docker not provided")
            return
        if not args.memory:
            print("memory not provided")
            return
        if not args.submission:
            print("submission not provided")
            return

        grade_parts(args.partids, args.docker, args.submission, args.memory)
