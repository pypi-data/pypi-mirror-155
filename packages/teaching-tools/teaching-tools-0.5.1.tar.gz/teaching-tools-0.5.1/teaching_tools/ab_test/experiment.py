from typing import Union

from pymongo import MongoClient

from teaching_tools.ab_test.data_model import Cohort
from teaching_tools.ab_test.repository import (
    AbstractRepository,
    MongoRepository,
)


class Experiment:
    """Class to generate experimental student data and insert into repository."""

    def __init__(self, repo: AbstractRepository) -> None:
        self.attach_repository(repo)

    def attach_repository(
        self,
        repository: Union[AbstractRepository, MongoClient],
        repo_name="wqu-abtest",
    ) -> None:
        """Attach new repository to experiment.

        Parameters
        ----------
        repository : AbstractRepository

        repo_name : str, optional
            If ``repository`` is ``MongoClient``, name of database, by default "wqu-abtest".

        Raises
        ------
        Exception
            Failed to attach repository.
        """
        if isinstance(repository, MongoClient):
            self.repo = MongoRepository(repository, repo_name)
        elif isinstance(repository, AbstractRepository):
            self.repo = repository
        else:
            raise Exception("Cannot attach repository.")

    def add_cohort_to_repository(
        self, collection="ds_applicants", overwrite=False, confirm_msg=True
    ) -> None:
        """Add cohort of students to repository.

        Parameters
        ----------
        collection : str, optional
            Name of collection to which cohort will be added, by default "ds_applicants"
        overwrite : bool, optional
            Whether to overwrite collection if already exists, by default False
        confirm_msg : bool, optional
            Whether to print confirmation message, by default True
        """
        self.repo.create_collection(collection, overwrite=overwrite)
        r = self.repo.insert(
            collection,
            records=self.cohort.yield_students(),
            return_result=True,
        )
        if confirm_msg:
            if r["acknowledged"]:
                print(
                    f"Added {len(self.cohort._students)} students to repository."
                )
            else:
                print(
                    f"Failed to add {len(self.cohort._students)} students to repository."
                )

    def run_experiment(self, days: int) -> None:
        """Add experimental student data to repository.

        Parameters
        ----------
        days : int
            Number of days to run the experiment. More days means more students.
        """
        self.cohort = Cohort(days=days, is_experiment=True)
        self.add_cohort_to_repository()

    def reset_experiment(self, confirm_msg=True) -> None:
        """Remove experimental student data from repository.

        Parameters
        ----------
        confirm_msg : bool, optional
            Whether to print confirmation message, by default True
        """
        results = self.repo.drop(
            collection="ds_applicants",
            query={"in_experiment": True},
            return_result=True,
        )
        if results["acknowledged"] and confirm_msg:
            print(f"Deleted {results['deleted_count']} from repository.")
