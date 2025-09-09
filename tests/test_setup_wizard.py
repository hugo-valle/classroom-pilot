"""Test that the setup wizard initializes correctly."""


def test_setup_wizard_import():
    """Test that the setup wizard can be imported and initialized."""
    from classroom_pilot.assignments.setup import AssignmentSetup
    from classroom_pilot.utils.ui_components import Colors

    # Test that the class can be instantiated
    wizard = AssignmentSetup()

    # Test that basic properties are set
    assert wizard.repo_root is not None
    assert wizard.config_file is not None
    assert wizard.total_steps == 8
    assert wizard.current_step == 0

    # Test color class
    assert hasattr(Colors, 'RED')
    assert hasattr(Colors, 'GREEN')
    assert hasattr(Colors, 'BLUE')

    print("✅ Setup wizard initializes correctly")


def test_validation_functions():
    """Test validation functions."""
    from classroom_pilot.assignments.setup import AssignmentSetup

    wizard = AssignmentSetup()

    # Test URL validation
    assert wizard.validate_url("https://github.com/user/repo") == True
    assert wizard.validate_url(
        "https://classroom.github.com/classrooms/123/assignments/test") == True
    assert wizard.validate_url("invalid-url") == False

    # Test organization validation
    assert wizard.validate_organization("valid-org") == True
    assert wizard.validate_organization("ValidOrg123") == True
    assert wizard.validate_organization("invalid_org!") == False

    # Test file path validation
    assert wizard.validate_file_path("test.py") == True
    assert wizard.validate_file_path("notebook.ipynb") == True
    assert wizard.validate_file_path("code.cpp") == True
    assert wizard.validate_file_path("invalid.xyz") == False

    print("✅ Validation functions work correctly")


if __name__ == "__main__":
    test_setup_wizard_import()
    test_validation_functions()
    print("✅ All setup wizard tests passed!")
