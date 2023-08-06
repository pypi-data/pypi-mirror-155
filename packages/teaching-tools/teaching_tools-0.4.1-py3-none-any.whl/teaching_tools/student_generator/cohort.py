import os

import names
import numpy as np
import pandas as pd
import yaml
from pymongo import MongoClient
from randomtimestamp import randomtimestamp
from yaml import Loader

from teaching_tools.student_generator.repository import (
    AbstractRepository,
    MongoRepository,
)


def load_yaml(filepath):
    with open(filepath, "r") as f:
        return yaml.load(f, Loader=Loader)


def get_cohort_params_path():
    return os.path.join(os.path.dirname(__file__), "cohort-params.yaml")


def load_cohort_params(cohort_params):
    if isinstance(cohort_params, dict):
        return cohort_params
    elif isinstance(cohort_params, str):
        return load_yaml(cohort_params)
    else:
        return load_yaml(get_cohort_params_path())


class CohortGenerator:
    def __init__(
        self,
        start="2022-01-18",
        stop=pd.Timestamp.now(),
        n=1000,
        cohort_params=None,
    ):
        self.start = pd.to_datetime(start) if isinstance(start, str) else start
        self.stop = pd.to_datetime(stop) if isinstance(stop, str) else stop
        self.n = n
        self.cohort_params = load_cohort_params(cohort_params)

    def generate_bday(self, years):
        days_offset = np.random.randint(low=0, high=350)
        birthdate = pd.Timestamp.now() - pd.DateOffset(
            years=years, days=days_offset
        )
        return birthdate.replace(hour=0, minute=0, second=0, microsecond=0)

    def generate_categorical(self, labels, probabilities, size=1):
        labels = np.array(labels)
        probabilities = np.array(probabilities)
        data = np.random.choice(
            a=labels,
            size=size,
            p=probabilities,
        )
        return data

    def generate_email(self, first, last):
        domains = [
            "@yahow.com",
            "@gmall.com",
            "@microsift.com",
            "@hotmeal.com",
        ]
        email = (
            first.lower()
            + "."
            + last.lower()
            + str(np.random.randint(1, 100))
            + np.random.choice(domains, 1)[0]
        )
        return email

    def create_students(self):
        self._data = pd.DataFrame()

        # Add columns from params
        for k, v in self.cohort_params.items():
            self._data[k] = self.generate_categorical(
                labels=list(v.keys()),
                probabilities=list(v.values()),
                size=self.n,
            )

        # Create birthday from age
        self._data["birthday"] = self._data["age"].apply(self.generate_bday)
        self._data.drop(columns=["age"], inplace=True)

        # Create name
        self._data["first_name"] = self._data["gender"].apply(
            lambda x: names.get_first_name(gender=x)
        )
        self._data["last_name"] = [
            names.get_last_name() for x in range(self.n)
        ]

        # Create email
        self._data["email"] = self._data[["first_name", "last_name"]].apply(
            lambda x: self.generate_email(*x), axis=1
        )

        # Create timestamp
        self._data["created"] = [
            randomtimestamp(start=self.start, end=self.stop)
            for x in range(self.n)
        ]

        # Reorder columns
        cols = [
            "created",
            "first_name",
            "last_name",
            "email",
            "birthday",
            "gender",
            "education_level",
            "nationality",
            "completed_quiz",
        ]
        self._data = self._data[cols]

    def yield_students(self):
        if not hasattr(self, "_data"):
            self.create_students()
        for s in self._data.itertuples(index=False, name="Student"):
            yield s._asdict()


class Cohort:
    def __init__(
        self,
        start="2022-01-18",
        stop=pd.Timestamp.now(),
        n=1000,
        cohort_params=None,
    ):
        self.start = pd.to_datetime(start) if isinstance(start, str) else start
        self.stop = pd.to_datetime(stop) if isinstance(stop, str) else stop
        self.n = n
        self.cohort_params = load_cohort_params(cohort_params)
        self.generator = CohortGenerator(
            self.start, self.stop, self.n, self.cohort_params
        )

    def attach_repository(self, repository, repo_name="wqu-abtest"):
        if isinstance(repository, MongoClient):
            self.repo = MongoRepository(repository, repo_name)
        elif isinstance(repository, AbstractRepository):
            self.repo = repository
        else:
            raise Exception("Cannot attach repository.")

    def create_students(self, confirm_msg=True):
        self.generator.create_students()
        if confirm_msg:
            print(f"Added {self.n} students to cohort.")

    def add_cohort_to_repository(
        self, collection="ds-applicants", confirm_msg=True
    ):
        self.repo.create_collection(collection)
        r = self.repo.insert(
            collection,
            records=self.generator.yield_students(),
            return_result=True,
        )
        if confirm_msg:
            if r["acknowledged"]:
                print(f"Added {self.n} students to repository.")
            else:
                print(f"Failed to add {self.n} students to repository.")
