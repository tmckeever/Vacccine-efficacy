
# Import functions

from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    codelist_from_csv
)

# Import codelists

chronic_cardiac_disease_codes = codelist_from_csv(
    "codelists/opensafely-chronic-cardiac-disease.csv", system="ctv3", column="CTV3ID"
)
chronic_liver_disease_codes = codelist_from_csv(
    "codelists/opensafely-chronic-liver-disease.csv", system="ctv3", column="CTV3ID"
)
chronic_kidney_disease_codes = codelist_from_csv(
    "codelists/opensafely-chronic_kidney_disease_codescsv", system="ctv3", column="CTV3ID"
)
hypertension_codes = codelist_from_csv(
    "codelists/opensafely-hypertension_codes.csv", system="ctv3", column="CTV3ID"
)
chronic_diabetes_codes = codelist_from_csv(
    "codelists/opensafely-chronic_diabetes_codes.csv", system="ctv3", column="CTV3ID"
)
chronic_respiratory_disease_disease_codes = codelist_from_csv(
    "codelists/opensafely-chronic-respiratory_disease_codes.csv", system="ctv3", column="CTV3ID"
)
solid_organ_transplantation_codes = codelist_from_csv(
    "codelists/opensafely-solid-organ-transplantation-codes.csv", system="ctv3", column="CTV3ID"
)
stroke_codes = codelist_from_csv(
    "codelists/opensafely-stroke-codes.csv", system="ctv3", column="CTV3ID"
)
cancer-excluding-lung-and-haemotological = codelist_from_csv(
    "codelists/opensafely-cancer-excluding-lung-and-haemotological.csv", system="ctv3", column="CTV3ID"
)

cancer-haemotological-cancer = codelist_from_csv(
    "codelists/opensafely-haemotological-cancer.csv", system="ctv3", column="CTV3ID"
)
dementia= codelist_from_csv(
    "codelists/opensafely-dementia-complete-48c76cf8.csv", system="ctv3", column="CTV3ID"
)



Lung cancer
Smoking ethnicity
IMD
bmi
flu vaccine

COIVD test
location
consultating rate



# Specifiy study defeinition

study = StudyDefinition(
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "exponential_increase",
    },
    # This line defines the study population
    population=patients.registered_with_one_practice_between(
        "2019-02-01", "2021-02-01"
    ),

    # https://github.com/opensafely/risk-factors-research/issues/49
    age=patients.age_as_of(
        "2021-03-01",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),



    # https://github.com/opensafely/risk-factors-research/issues/46
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),

    # https://codelists.opensafely.org/codelist/opensafely/chronic-cardiac-disease/2020-04-08/
    chronic_cardiac_disease=patients.with_these_clinical_events(
        chronic_cardiac_disease_codes,
        returning="date",
        find_first_match_in_period=True,
        include_month=True,
        return_expectations={"incidence": 0.2},
    ),

    # https://codelists.opensafely.org/codelist/opensafely/chronic-liver-disease/2020-06-02/
    chronic_liver_disease=patients.with_these_clinical_events(
        chronic_liver_disease_codes,
        returning="date",
        find_first_match_in_period=True,
        include_month=True,
        return_expectations={
            "incidence": 0.2,
            "date": {"earliest": "1950-01-01", "latest": "today"},
        },
    ),

    # https://github.com/opensafely/risk-factors-research/issues/51
    bmi=patients.most_recent_bmi(
        on_or_after="2010-02-01",
        minimum_age_at_measurement=16,
        include_measurement_date=True,
        include_month=True,
        return_expectations={
            "incidence": 0.6,
            "float": {"distribution": "normal", "mean": 35, "stddev": 10},
        },
    ),

    # https://github.com/opensafely/risk-factors-research/issues/48
    bp_sys=patients.mean_recorded_value(
        systolic_blood_pressure_codes,
        on_most_recent_day_of_measurement=True,
        on_or_before="2020-02-01",
        include_measurement_date=True,
        include_month=True,
        return_expectations={
            "incidence": 0.6,
            "float": {"distribution": "normal", "mean": 80, "stddev": 10},
        },
    ),

    # https://github.com/opensafely/risk-factors-research/issues/48
    bp_dias=patients.mean_recorded_value(
        diastolic_blood_pressure_codes,
        on_most_recent_day_of_measurement=True,
        on_or_before="2020-02-01",
        include_measurement_date=True,
        include_month=True,
        return_expectations={
            "incidence": 0.6,
            "float": {"distribution": "normal", "mean": 120, "stddev": 10},
        },
    ),

    # https://github.com/opensafely/risk-factors-research/issues/44
    stp=patients.registered_practice_as_of(
        "2020-02-01",
        returning="stp_code",
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"STP1": 0.5, "STP2": 0.5}},
        },
    ),

    # https://github.com/opensafely/risk-factors-research/issues/44
    msoa=patients.registered_practice_as_of(
        "2020-02-01",
        returning="msoa_code",
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"MSOA1": 0.5, "MSOA2": 0.5}},
        },
    ),

    # https://github.com/opensafely/risk-factors-research/issues/45
    imd=patients.address_as_of(
        "2020-02-01",
        returning="index_of_multiple_deprivation",
        round_to_nearest=100,
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"100": 0.1, "200": 0.2, "300": 0.7}},
        },
    ),

    # https://github.com/opensafely/risk-factors-research/issues/47
    rural_urban=patients.address_as_of(
        "2020-02-01",
        returning="rural_urban_classification",
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"rural": 0.1, "urban": 0.9}},
        },
    ),

    # https://codelists.opensafely.org/codelist/opensafely/asthma-inhaler-salbutamol-medication/2020-04-15/
    recent_salbutamol_count=patients.with_these_medications(
        salbutamol_codes,
        between=["2018-02-01", "2020-02-01"],
        returning="number_of_matches_in_period",
        return_expectations={
            "incidence": 0.6,
            "int": {"distribution": "normal", "mean": 8, "stddev": 2},
        },
    ),
)
