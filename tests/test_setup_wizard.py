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
    assert hasattr(wizard, 'config_values')
    assert hasattr(wizard, 'token_files')

    # Test color class
    assert hasattr(Colors, 'RED')
    assert hasattr(Colors, 'GREEN')
    assert hasattr(Colors, 'BLUE')

    print("✅ Setup wizard initializes correctly")


def test_wizard_methods():
    """Test that wizard has expected methods."""
    from classroom_pilot.assignments.setup import AssignmentSetup

    wizard = AssignmentSetup()

    # Test that methods exist
    assert hasattr(wizard, 'run_wizard')
    assert hasattr(wizard, 'validators')
    assert hasattr(wizard, 'url_parser')
    assert hasattr(wizard, 'input_handler')

    # Test validators methods
    assert hasattr(wizard.validators, 'validate_url')
    assert hasattr(wizard.validators, 'validate_organization')

    print("✅ Wizard methods are available")


if __name__ == "__main__":
    test_setup_wizard_import()
    test_wizard_methods()
    print("✅ All setup wizard tests passed!")
