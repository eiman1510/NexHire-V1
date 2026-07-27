import unittest

from services.education_matching import (
    education_matches,
    normalize_education_text,
)


class EducationMatchingTests(unittest.TestCase):
    def test_reported_bachelors_in_variant_matches_bachelors_degree(self):
        self.assertTrue(
            education_matches("Bachelor's degree", ["Bachelors in"])
        )

    def test_bachelor_of_science_and_abbreviations_match(self):
        for parsed_degree in (
            "Bachelor of Science in Computer Science",
            "B.Sc. Computer Science",
            "BS Computer Science",
        ):
            with self.subTest(parsed_degree=parsed_degree):
                self.assertTrue(
                    education_matches("Bachelors", [parsed_degree])
                )

    def test_higher_degree_satisfies_lower_minimum(self):
        self.assertTrue(
            education_matches("Bachelor's degree", ["Master of Science"])
        )

    def test_all_candidate_education_entries_are_considered(self):
        self.assertTrue(
            education_matches(
                "Bachelor's degree",
                ["FSC Pre-Engineering", "Bachelors in"],
            )
        )

    def test_lower_or_unrelated_qualification_is_rejected(self):
        self.assertFalse(
            education_matches(
                "Bachelor's degree",
                ["FSC Pre-Engineering", "AWS Academy Graduate"],
            )
        )

    def test_specialized_requirement_uses_word_boundaries(self):
        self.assertTrue(
            education_matches(
                "Computer Science",
                ["Bachelors in Computer Science"],
            )
        )
        self.assertFalse(
            education_matches("Art", ["Artificial Intelligence"])
        )

    def test_normalization_handles_curly_apostrophe(self):
        self.assertEqual(
            normalize_education_text("Bachelor’s Degree"),
            "bachelors degree",
        )

    def test_missing_requirement_does_not_block_candidate(self):
        self.assertTrue(education_matches("", []))


if __name__ == "__main__":
    unittest.main()
